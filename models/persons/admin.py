#!/usr/bin/python3
"""
This module defines the atrributes for admim
"""

from sqlalchemy import Column, String, ForeignKey

from .person import Persons, Base


class Admin(Persons, Base):
    """Admin class"""
    __tablename__ = "administrators"
    __mapper_args__ = {"polymorphic_identity": "admin"}
    id = Column(String(60), ForeignKey("allpersons.id"), unique=True, primary_key=True)

    admin_no = Column(String(30))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
