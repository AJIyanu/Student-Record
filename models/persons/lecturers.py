#!/usr/bin/python3
"""
This module defines the atrributes for lecturers
"""

from .person import Persons, Base


class Lecturer(Persons):
    """Lecturers class"""
    staff_no = ""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
