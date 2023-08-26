#!/usr/bin/python3
"""
This module defines the atrributes for admim
"""

from .person import Persons, Base


class Admin(Persons):
    """Admin class"""
    admin_no = ""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
