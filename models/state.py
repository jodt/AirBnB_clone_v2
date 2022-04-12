#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base, storage_Type
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models import storage


class State(BaseModel, Base):
    """ State class """
    if storage_Type == "db":
        __tablename__ = "states"
        name = Column(String(128), nullable=False)
        cities = relationship('City', cascade="all, delete", backref="state")
    else:
        name = ""
        @property
        def cities(self):
            result = []
            for value in storage.all().values():
                if (value.__class__.__name__ == "City") and value.state_id == self.id:
                    result.append(value)
            return result
