#!/usr/bin/python3
"""
This module defines class for attendance
"""

from uuid import uuid4
import json
from datetime import datetime

from ..persons.person import Base


class Attendance:
    """Attendance class"""
    id = ""
    session = ""
    created_at = ""
    student_id = ""
    status = ""
    offering = ""


    def __init__(self, **kwargs):
        """intitializes attendance"""
        if "id" not in kwargs:
            self.id = str(uuid4())
        else:
            self.id = kwargs.pop("id")
        if "created_at" not in kwargs:
            self.created_at = datetime.now()
        else:
            date = kwargs.pop("created_at")
            try:
                self.created_at = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%f")
            except TypeError:
                self.created_at = date
        kwargs.pop("status", None)
        self.status = False
        for key, value in kwargs.items():
            setattr(self, key, value)

    def to_dict(self):
        """returns a dictionary representation of the class"""
        self_dict = {}
        self_dict.update(self.__dict__)
        self_dict.update({'__class__': self.__class__.__name__})
        self_dict['created_at'] = self.created_at.isoformat()
        return self_dict

    def json_me(self):
        """returns a json representation of self"""
        return json.dumps(self.to_dict())

    def mark_att(self):
        """Changes attendance status to present"""
        self.status = True
