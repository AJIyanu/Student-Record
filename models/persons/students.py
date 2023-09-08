#!/usr/bin/python3
"""
This module defines the atrributes for students
"""

from sqlalchemy import Column, CheckConstraint, ForeignKey, String, Text
from .person import Persons, Base


class Student(Persons, Base):
    """Students class"""
    __tablename__ = "students"
    __mapper_args__ = {"polymorphic_identity": "student"}
    id = Column(String(60), ForeignKey("allpersons.id"), unique=True, primary_key=True)
    matric_no = Column(String(20))
    salvation = Column(Text)
    level = Column(String(15),
                   CheckConstraint("level IN ('Certificate', 'Diploma', 'Advanced')"))
    status = Column(String(15),
                    CheckConstraint("status IN\
('Prospective', 'Saved', 'Admitted', 'Withdrawn', 'Reactivated', 'Graduated')"))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def calc_score(self, course=None):
        """returns a list of student score"""
        pass

    def course_registration(self, course, session, semester):
        """creates score for student based on regiserred course"""
        pass

    def change_status(self):
        """"Changes students status and returns new status"""
        pass

    def calc_cgpa(self):
        """returns current cgpa"""
        pass
