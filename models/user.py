#!/usr/bin/python3
"""This module defines a class User"""
from models.base_model import BaseModel, Base
from sqlalchemy import Table, MetaData, Column, String
from models.__init__ import storage_Type


class User(BaseModel, Base):
    """This class defines a user by various attributes"""
    if storage_Type == 'db':
        __tablename__ = Table('users', MetaData(bind=None))
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
    else:
        email = ''
        password = ''
        first_name = ''
        last_name = ''
