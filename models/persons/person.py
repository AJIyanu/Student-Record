#!/usr/bin/python3
"""
This module forms the base for all persons in the school
This module also has the Base for sqlaclhemy to create tables
"""


from uuid import uuid4
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class Persons(Base):
    """
    This class has all common attributes for all Persons
    """

    id = ""
    created_at = ""
    updated_at = ""
    surname = ""
    firstname = ""
    middlename = ""
    dob = ""
    phone = ""
    address = ""
    church = ""
    occupation = ""
    sex = ""

    def __init__(self, **kwargs):
        """creates the person instance from key word argument"""
        if "id" not in kwargs:
            self.id = str(uuid4())
        if "surname" not in kwargs or "firstname" not in kwargs:
            raise AttributeError("Surname or Firsname missing")
        if "created_at" not in kwargs:
            self.created_at = datetime.now()
            self.updated_at = self.created_at
        else:
            self.created_at = datetime.strptime(kwargs["created_at"],
                                                "%Y-%m-%dT%H:%M:%S.%f")
            try:
                self.updated_at = datetime.strptime(kwargs["updated_at"],
                                                    "%Y-%m-%dT%H:%M:%S.%f")
            except KeyError:
                pass
        if "dob" not in kwargs:
            raise AttributeError("Date of Birth not present")
        else:
            try:
                self.dob = datetime.strptime(kwargs["dob"], "%Y-%m-%d")
            except TypeError:
                self.dob = 
