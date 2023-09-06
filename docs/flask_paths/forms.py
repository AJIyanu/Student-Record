#!/usr/bin/env python3
""" Module of Index views
"""
# import base64
# from datetime import datetime
import json

from flask_paths import app_views
from flask import render_template, request, redirect, jsonify
# from flask import session, make_response


# from models.persons.auth import Auth
from models.persons.person import Persons
# from ..models.persons.students import Student
# from ..models.persons.lecturers import Lecturer
# from ..models.persons.admin import Admin

# Persons_dict = {
#                 "student": Student,
#                 "lecturer": Lecturer,
#                 "admin": Admin
#                 }

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
    return jsonify(user=userdata, status="succesful log in")
