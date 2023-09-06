"""
brings all routes in a place
"""
from flask import Blueprint

app_views = Blueprint("app_views", __name__)

# from models.persons.person import Persons
from .forms import *
