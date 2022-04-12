#!/usr/bin/python3
""" City Module for HBNB project """
from models.base_model import BaseModel, Base, storage_Type
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship
from models.__init__ import storage_Type

class City(BaseModel, Base):
    """ The city class, contains state ID and name """
    if storage_Type == "db":
        __tablename__ = "cities"
        name = Column(String(128), nullable=False)
        state_id = Column(String(60), ForeignKey("states.id"), nullable=False)
        places = relationship("Place", back_populates="cities",
                              cascade="all, delete", passive_deletes=True)
    else:
        state_id = ""
        name = ""
