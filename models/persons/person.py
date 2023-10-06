#!/usr/bin/python3
"""
This module forms the base for all persons in the school
This module also has the Base for sqlaclhemy to create tables
"""


from importlib import import_module

from uuid import uuid4
import json
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Text, DateTime, CheckConstraint


Base = declarative_base()

class Persons(Base):
    """
    This class has all common attributes for all Persons
    """

    __tablename__ = "allpersons"
    __mapper_args__ = {'polymorphic_identity': 'allpersons',
                       'polymorphic_on': 'personality'}
    personality = Column(String(15))
    id = Column(String(60), unique=True, primary_key=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, unique=datetime.utcnow())
    surname = Column(String(20), nullable=False)
    firstname = Column(String(20), nullable=False)
    middlename = Column(String(20))
    dob = Column(DateTime, nullable=False)
    phone = Column(String(30))
    address = Column(Text)
    church = Column(String(30))
    state = Column(String(30))
    lga = Column(String(30))
    occupation = Column(String(20))
    sex = Column(String(10),
                 CheckConstraint("sex IN ('Male', 'Female', 'none')"))
    image = Column(String(30))

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
        dob = kwargs.pop("dob")
        try:
            self.dob = datetime.strptime(dob, "%Y-%m-%d")
        except TypeError:
            self.dob = dob
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.image = "default.png"
        vault = import_module("models").vault
        vault.new(self)

    def save_me(self):
        """adds update to database"""
        vault = import_module("models").vault
        self.updated_at = datetime.now()
        vault.save()

    def to_dict(self):
        """returns a dictionary representation of the class"""
        self_dict = {}
        self_dict.update(self.__dict__)
        self_dict.update({'__class__': str(self.__class__.__name__)})
        self_dict['created_at'] = self.created_at.isoformat()
        self_dict['updated_at'] = self.updated_at.isoformat()
        self_dict['dob'] = self.dob.isoformat()
        if '_sa_instance_state' in self_dict:
            self_dict.pop('_sa_instance_state')
        return self_dict

    def json_me(self):
        """returns a json representation of self"""
        return json.dumps(self.to_dict())

    def update(self, **data):
        """Updates user data and save to database"""
        for name, value in data.items():
            if name != "dob":
                setattr(self, name, value)
            else:
                setattr(self, "dob", datetime.fromisoformat(value))
        self.save_me()

    @classmethod
    def find_me(cls, id):
        """returns the user class"""
        vault = import_module("models").vault
        try:
            me = vault.find(cls, id=id)[0]
        except IndexError:
            return
        return me
