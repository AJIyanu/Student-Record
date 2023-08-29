#!/usr/bin/python3
"""
This module defines the atrributes for lecturers
"""
from sqlalchemy import Column, String, ForeignKey
from .person import Persons, Base


class Lecturer(Persons, Base):
    """Lecturers class"""
    __tablename__ = "lecturers"
    __mapper_args__ = {"polymorphic_identity": "lecturer"}
    id = Column(String(30), ForeignKey("allpersons.id"), unique=True, primary_key=True)
    staff_no = Column(String(15))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def mark_att(self, student_id, session, course_id):
        """mark attendance for student"""
        pass

    def add_assignment(self, course_id, mark=10):
        """finds all score created on the course and adds assignment"""
        pass

    def add_test(self, course_id, mark=20):
        """same as above"""
        pass

    def add_exam(self, course_id, mark=60):
        """same as above"""
        pass
