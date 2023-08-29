#!/usr/bin/python3
"""
This module forms the base for all persons in the school
This module also has the Base for sqlaclhemy to create tables
"""


from uuid import uuid4
import json
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class Persons():
    """
    This class has all common attributes for all Persons
    """

    __tablename__ = "allpersons"
    __mapper_args__ = {'polymorphic_identity': 'allpersons',
                       'polymorphic_on': 'personality'}
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
    image = ""

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
            self.created_at = datetime.strptime(kwargs.pop("created_at"),
                                                "%Y-%m-%dT%H:%M:%S.%f")
            try:
                self.updated_at = datetime.strptime(kwargs.pop("updated_at"),
                                                    "%Y-%m-%dT%H:%M:%S.%f")
            except KeyError:
                pass
        if "dob" not in kwargs:
            raise AttributeError("Date of Birth not present")
        else:
            dob = kwargs.pop("dob")
            try:
                self.dob = datetime.strptime(dob, "%Y-%m-%d")
            except TypeError:
                self.dob = dob
        for key, value in kwargs.items():
            setattr(self, key, value)
        from models import vault
        vault.new(self)

    def save_me(self):
        """adds update to database"""
        from models import vault
        self.updated_at = datetime.now()
        vault.save()

    def to_dict(self):
        """returns a dictionary representation of the class"""
        self_dict = {}
        self_dict.update(self.__dict__)
        self_dict.update({'__class__': self.__class__.__name__})
        self_dict['created_at'] = self.created_at.isoformat()
        self_dict['updated_at'] = self.updated_at.isoformat()
        self_dict['dob'] = self.dob.isoformat()
        return self_dict

    def json_me(self):
        """returns a json representation of self"""
        return json.dumps(self.to_dict())
