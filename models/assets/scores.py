#!/usr/bin/python3
"""
This module defines class for score
"""

from uuid import uuid4
import json
from datetime import datetime

from ..persons.person import Base


class Score:
    """Score class"""
    id = ""
    session = ""
    semester = ""
    created_at = ""
    updated_at = ""
    lecturer_id = ""
    student_id = ""
    course_code = ""
    level = ""
    __unit = ""
    __attendance = 10
    __assignment = [{"mark obtained": 0, "mark obtainable": 10}]
    __test = [{"mark obtained": 0, "mark obtainable": 10}]
    __cont_assess = [{"mark obtained": 0, "mark obtainable": 10}]
    __exam = {"mark obtained": 0, "mark obtainable": 60}
    __total = {"mark obtained": 0, "mark obtainable": 100}
    __point = "F"


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
            update = kwargs.pop("update_at")
            try:
                self.created_at = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%f")
                self.updated_at = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%f")
            except TypeError:
                self.created_at = date
                self.updated_at = update
        for key, value in kwargs.items():
            setattr(self, key, value)

    def to_dict(self):
        """returns a dictionary representation of the class"""
        self_dict = {}
        self_dict.update(self.__dict__)
        self_dict.update({'__class__': self.__class__.__name__})
        self_dict['created_at'] = self.created_at.isoformat()
        self_dict['updated_at'] = self.created_at.isoformat()
        return self_dict

    def json_me(self):
        """returns a json representation of self"""
        return json.dumps(self.to_dict())

    def save(self):
        """fetches unit from course code and sets then saves"""

    def add_assignment(self, ass_no: 0, mkobtnble: 'N', mkobtnd: 0):
        """adds assignment"""
