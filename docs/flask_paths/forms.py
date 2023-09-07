#!/usr/bin/env python3
""" Module of Index views
"""
# import base64
# from datetime import datetime
import sys
import json
from importlib import import_module

from flask_paths import app_views
from flask import render_template, request, redirect, jsonify
from flask import make_response

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
        return jsonify({"error": "Invalid username or passowrd"})
    userdata = json.loads(user.json_me())
    # return jsonify(user=userdata, status="succesful log in", check=user.to_dict())
    response = make_response(redirect("/register/certificate"))
    response.set_cookie("check", "cookie-set")
    return response


@app_views.route("/register/<level>", methods=['GET', 'POST'])
def registeration_form(level):
    """returns registration form"""
    return render_template(f"{level}-sign-up.html")


@app_views.route("/get-started", methods=["POST"])
def register_new_user():
    """registers a new user"""
    details = request.form
    return jsonify(received=details)
