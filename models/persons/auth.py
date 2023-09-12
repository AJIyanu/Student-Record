#!/usr/bin/python3
"""
This module contains the class to create auth and permissions
to access data by users on the database
"""


import time
from importlib import import_module

# from uuid import uuid4
import json
from datetime import datetime, timedelta
from sqlalchemy import Column, String, ForeignKey, DateTime
from argon2 import PasswordHasher, exceptions
from firebase_token_generator import create_token
import jwt


from .person import Base


hashme = PasswordHasher()


class Auth(Base):
    """
    This class has all common attributes for all Persons
    """

    __tablename__ = "authentications"
    id = Column(String(60), ForeignKey("allpersons.id"), unique=True,
                primary_key=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.utcnow())
    __password = Column(String(128), nullable=False)
    __reset_token = Column(String(256), nullable=False, default="newuser")
    email = Column(String(45))
    username = Column(String(45),  unique=True, nullable=False)

    def __init__(self, **kwargs):
        """creates the person instance from key word argument"""
        if "id" not in kwargs:
            raise AttributeError("please supply user's id")
        else:
            self.id = kwargs.get("id")
        if "created_at" not in kwargs:
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
        else:
            self.created_at = datetime.strptime(kwargs.pop("created_at"),
                                                "%Y-%m-%dT%H:%M:%S.%f")
            self.updated_at = datetime.strptime(kwargs.pop("updated_at"),
                                                "%Y-%m-%dT%H:%M:%S.%f")
        self.email = kwargs.get("email", "none@none.none")
        self.username = kwargs.get("username")
        self.__reset_token = "newuser"
        if self.username is None:
            raise ValueError("Please supply a valid username")
        vault = import_module("models").vault
        vault.new(self)

    def save_me(self):
        """adds update to database"""
        # from models import vault
        self.updated_at = datetime.now()
        vault = import_module("models").vault
        vault.save()

    def to_dict(self):
        """returns a dictionary representation of the class"""
        self_dict = {}
        self_dict.update(self.__dict__)
        self_dict.update({'__class__': str(self.__class__.__name__)})
        self_dict['created_at'] = self.created_at.isoformat()
        self_dict['updated_at'] = self.updated_at.isoformat()
        if '_sa_instance_state' in self_dict:
            self_dict.pop('_sa_instance_state')
        return self_dict

    def json_me(self):
        """returns a json representation of self"""
        return json.dumps(self.to_dict())

    def add_password(self, password):
        """adds password for firstime user"""
        if self.__reset_token == "newuser":
            self.__password = hashme.hash(password)
            expire = datetime.now() + timedelta(minutes=30)
            payload = {"uid": self.id, "username": self.username}
            self.__reset_token = create_token("MESACOT", payload,
                                              options={"expires": expire})
            self.save_me()
            return "success"
        return "not set"

    def reset_password(self, oldpwd_token, new_pwd):
        """resets the password if either old password
        is provided or reset token"""
        try:
            if hashme.verify(self.__password, oldpwd_token):
                self.__reset_token = "newuser"
                status = self.add_password(new_pwd)
        except exceptions.VerifyMismatchError:
            try:
                decoded =jwt.decode(oldpwd_token, "MESACOT",
                                    algorithms=['HS256'], verify=False)
                print(decoded['exp'])
                print(time.time())
                print(decoded['exp'] < time.time())
                payload = decoded['d']
                if payload.get('uid') == self.id and payload.get('username') == self.username:
                    self.__reset_token = "newuser"
                    self.add_password(new_pwd)
                    status = "success"
                else:
                    status = "identity error"
            except jwt.exceptions.DecodeError:
                status = "jwt mismatch"
            except jwt.exceptions.ExpiredSignatureError:
                status = "expired"
        self.save_me()
        return status

    def generate_token(self):
        """generates reset token"""
        expire = datetime.now() + timedelta(minutes=1)
        payload = {"uid": self.id, "username": self.username}
        self.__reset_token = create_token("MESACOT", payload,
                                          options={"expires": expire})
        self.save_me()
        return self.__reset_token

    def validate_password(self, password):
        """validates user password
        returns True if verified otherwise false

        important - in future work a way to destroy bruteforce
        attack"""
        try:
            return hashme.verify(self.__password, password)
        except exceptions.VerifyMismatchError:
            return False

    @classmethod
    def find_me(cls, id=None, username=None):
        """returns class object based on username or id
        otherwise returns none"""
        if id is None and username is None:
            return
        # from models import vault
        vault = import_module("models").vault
        if id:
            try:
                return vault.find(cls, id=id)[0]
            except IndexError:
                if username:
                    try:
                        return vault.find(cls, username=username)[0]
                    except IndexError:
                        return
        else:
            try:
                return vault.find(cls, username=username)[0]
            except IndexError:
                return
        return
