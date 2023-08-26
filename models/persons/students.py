#!/usr/bin/python3
"""
This module defines the atrributes for students
"""

from .person import Persons, Base


class Student(Persons):
    """Students class"""
    matric_no = ""
    salvation = ""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
