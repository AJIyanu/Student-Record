"""
brings all routes in a place
"""
from flask import Blueprint

app_views = Blueprint("app_views", __name__)

from pathsapp.forms import *
