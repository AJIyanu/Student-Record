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
    date = ""
    student_id = ""
    status = ""
    offering = ""


    def __init__(self, **kwargs):
        """intitializes attendance"""
        if "id" not in kwargs:
            self.id = str(uuid4())
        else:
            self.id = kwargs.pop("id")
        if "date" not in kwargs:
            self.date = datetime.now()
        else:
            date = kwargs.pop("date")
            try:
                self.date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%f")
            except TypeError:
                self.date = date
        kwargs.pop("status", None)
        self.status = False
        for key, value in kwargs.items():
            setattr(self, key, value)

    def to_dict(self):
        """returns a dictionary representation of the class"""
        self_dict = {}
        self_dict.update(self.__dict__)
        self_dict.update({'__class__': self.__class__.__name__})
        self_dict['created_at'] = self.date.isoformat()
        return self_dict

    def json_me(self):
        """returns a json representation of self"""
        return json.dumps(self.to_dict())

    def mark_att(self):
        """Changes attendance status to present"""
        self.status = True
