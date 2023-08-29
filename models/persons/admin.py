#!/usr/bin/python3
"""
This module defines the atrributes for admim
"""

from sqlalchemy import Column, String
from .person import Persons, Base


class Admin(Persons, Base):
    """Admin class"""
    __tablename__ = "administrators"
    __mapper_args__ = {"polymorphic_identity": "admin"}
    admin_no = Column(String(30))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
