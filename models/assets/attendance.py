#!/usr/bin/python3
"""
This module defines class for attendance
"""

from uuid import uuid4
import json
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey
from sqlalchemy import CheckConstraint

from ..persons.person import Base


class Attendance(Base):
    """Attendance class"""

    __tablename___ = "attendance"
    id = Column(String(30), primary_key=True, unique=True, nullable=False)
    session = Column(String(10))
    created_at = Column(DateTime, default=datetime.utcnow())
    student_id = Column(String(30), ForeignKey("students.id"))
    course_code = Column(String(10))
    status = Column(Integer, CheckConstraint("status IN (0, 10)"))
    offering = Column(Integer)


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
        from models import vault
        vault.new(self)

    def to_dict(self):
        """returns a dictionary representation of the class"""
        self_dict = {}
        self_dict.update(self.__dict__)
        self_dict.update({'__class__': self.__class__.__name__})
        self_dict['created_at'] = self.created_at.isoformat()
        return self_dict

    def save_me(self):
        """adds update to database"""
        from models import vault
        # self.updated_at = datetime.now()
        vault.save()

    def json_me(self):
        """returns a json representation of self"""
        return json.dumps(self.to_dict())

    def mark_att(self):
        """Changes attendance status to present"""
        self.status = True
