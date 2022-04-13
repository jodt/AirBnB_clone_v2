#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base, storage_Type
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
if storage_Type == "db":
    from models.place import place_amenity


class Amenity(BaseModel, Base):
    if storage_Type == "db":
        __tablename__ = "amenities"
        name = Column(String(128), nullable=False)
    else:
        name = ""
