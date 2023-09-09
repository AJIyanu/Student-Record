#!/usr/bin/env python3
""" Module of Index views
"""
# import base64
import sys
import json
from datetime import date
from importlib import import_module

from flask_paths import app_views
from flask import render_template, request, redirect, jsonify
from flask import make_response
from flask_jwt_extended import (set_access_cookies, create_access_token,
                                get_jwt_identity, jwt_required)


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
    if request.method == "GET":
        return render_template(f"{level}-sign-up.html")
    details = request.form
    from .methods import add_student_info
    add_student_info("2023", "certificate", {"id": "22", "user": details})
    return jsonify(details=details)


@app_views.route("/get-started", methods=["POST"])
def register_new_user():
    """registers a new user"""
    details = request.form
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
    return response
