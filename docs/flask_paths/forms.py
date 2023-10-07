#!/usr/bin/env python3
""" Module of Index views
"""
# import base64
import sys
import json
from datetime import date, datetime
from importlib import import_module


try:
    from flask_paths import app_views
except ModuleNotFoundError:
    from docs.flask_paths import app_views
from flask import render_template, request, redirect, jsonify, url_for
from flask import session
from flask import make_response
from flask_jwt_extended import (set_access_cookies, create_access_token,
                                get_jwt_identity, jwt_required)

from .methods import add_student_info



# print(sys.path)
sys.path.insert(0, 'C:\\Users\\adere\\Documents\\GitHub\\AJIyanu\\Mesacot\\Student Record')
sys.path.insert(0, '/home/ajiyanu/aj_project/Student-Record/')
Auth = import_module("models.persons.auth").Auth
Persons = import_module("models.persons.person").Persons
Student = import_module("models.persons.students").Student
Lecturer = import_module("models.persons.lecturers").Lecturer
Admin = import_module("models.persons.admin").Admin


Persons_dict = {
                "student": Student,
                "lecturer": Lecturer,
                "admin": Admin
                }

@app_views.route('/signin', methods=['POST'])
def login():
    """verifies user details and redirects to dashboard"""
    username = request.form["username"]
    pwd = request.form["password"]
    user = Auth.find_me(username=username)
    if user is not None:
        if user.validate_password(pwd):
            user = Persons.find_me(user.id)
    else:
        session['error'] = "Invalid Username or Password"
        return redirect(url_for('index_page'))
    userdata = json.loads(user.json_me())
    access_token = create_access_token(identity=user.id)
    if user.status is None or user.status == "Prospective":
        response = make_response(redirect("/register/certificate"))
        set_access_cookies(response, access_token)
        return response
    return jsonify(user=userdata, status="succesful log in",
                   check=user.to_dict())


@app_views.route("/register/<level>", methods=['GET', 'POST'])
@jwt_required()
def registeration_form(level):
    """returns registration form"""
    user_id = get_jwt_identity()
    student = Student.find_me(user_id)
    if request.method == "GET":
        return render_template(f"{level}-sign-up.html", user=json.dumps(student.to_dict()))
    details = request.form
    print(student)
    try:
        student.dob = datetime.fromisoformat(details['dob'])
    except KeyError:
        pass
    student.update(**details)
    print(student.to_dict())
    user_dp = request.files.get("dp_image")
    if user_dp:
        user_dp.save(f"docs/static/images/passports/{student.surname}_{user_id}.png")
        student.update(image=f"{student.surname}_{user_id}.png")
    add_student_info("2023", details['level'], {"id": user_id, "studentData": details})
    return jsonify(details=details)


@app_views.route("/get-started", methods=["POST"])
def register_new_user():
    """registers a new user"""
    details = request.form
    print(details)
    error_list = []
    for key, check in details.items():
        if check == "":
            error_list.append(f"{key} is empty")
    if len(error_list) > 0:
        return jsonify(error=error_list)
    new_student = Student(dob=date.today(), **details)
    new_student.status = "Prospective"
    new_student.save_me()
    logmein = Auth(id=new_student.id, email=details.get("email"),
                   username=details.get("email"))
    logmein.add_password(details.get("password"))
    access_token = create_access_token(identity=new_student.id)
    response = make_response(redirect(f"/register/{new_student.level}"))
    set_access_cookies(response, access_token)
    print("saved, now redirecting")
    return response
