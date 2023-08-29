#!/usr/bin/python3
"""
This module contains the class to create auth and permissions
to access data by users on the database
"""


from uuid import uuid4
import json
from datetime import datetime
from sqlalchemy import Column, String, ForeignKey, DateTime, CheckConstraint

from .person import Base, Persons

class Auth(Base):
    """
    This class has all common attributes for all Persons
    """

    __tablename__ = "authentications"
    id = Column(String(60), ForeignKey("allpersons.id"), unique=True,
                primary_key=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow())
    __password = Column(String(128), nullable=False)
    __reset_token = Column(String(128), nullable=False)
    email = Column(String(30))
    username = Column(String(15),  unique=True, nullable=False)

    def __init__(self, **kwargs):
        """creates the person instance from key word argument"""
        if "id" not in kwargs:
            self.id = str(uuid4())
        if "created_at" not in kwargs:
            self.created_at = datetime.now()
        else:
            self.created_at = datetime.strptime(kwargs.pop("created_at"),
                                                "%Y-%m-%dT%H:%M:%S.%f")
        self.email = kwargs.get("email")
        self.username = kwargs.get("username")
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
        self_dict.update({'__class__': str(self.__class__.__name__)})
        self_dict['created_at'] = self.created_at.isoformat()
        if '_sa_instance_state' in self_dict:
            self_dict.pop('_sa_instance_state')
        return self_dict

    def json_me(self):
        """returns a json representation of self"""
        return json.dumps(self.to_dict())
