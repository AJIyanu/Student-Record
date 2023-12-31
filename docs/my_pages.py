#!/usr/bin/env python3
"""
Route module for web pages
"""
from datetime import timedelta, datetime, timezone
from os import getenv, name

from flask_jwt_extended import JWTManager, get_jwt, create_access_token
from flask_jwt_extended  import set_access_cookies, get_jwt_identity
from flask import Flask, jsonify, send_file, render_template, request
from flask import session

from flask_paths import app_views


app = Flask(__name__)
app.register_blueprint(app_views)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SECRET_KEY'] = 'roseismysecretkey'
app.config["JWT_TOKEN_LOCATION"] = ["cookies", "headers"]
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=2)
# app.config['JWT_CSRF_METHODS'] = ['PUT', 'PATCH', 'DELETE']
app.config['FOLLOW_SYMLINKS'] = True
app.config['JWT_SECRET_KEY'] = 'roseismysecretekey'
jwt = JWTManager(app)

print(name)

@app.after_request
def refresh_expiring_jwts(response):
    """refreshes the jwt token in the browser"""
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            # this wont work because former expiry was added to new
            access_token = create_access_token(identity=get_jwt_identity(),
                                               additional_claims=get_jwt())
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        # Case where there is not a valid JWT. Just return the original response
        return response


@app.route("/favicon.ico", methods=["GET"])
def favicon():
    """returns favicon"""
    return send_file("favicon_light.ico")

@app.route("/", methods=["GET"])
def index_page():
    """returns the index page"""
    error = session.get('error', "")
    session.clear()
    if name == "nt":
        return render_template("index_win.html", msg=error)
    return render_template("index.html")

@app.before_request
def handle_before():
    """handles stuff before request is made"""
    csrf = request.form.get("csrf_token")
    if csrf:
        request.headers['X-CSRF-Token'] = csrf

@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found", "err": str(error)}), 404


@app.errorhandler(401)
def not_authorized(error) -> str:
    """handling unauthorized shits"""
    return jsonify({"error": "Unauthorized", "err": str(error)}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """authorized but not aloowed"""
    return jsonify({"error": "Forbidden", "err": str(error)}), 403

if __name__ == "__main__":
    host = getenv("WEBDOC_HOST", "0.0.0.0")
    port = getenv("WEBDOC_PORT", "5000")
    app.run(host=host, port=port, debug=True)
