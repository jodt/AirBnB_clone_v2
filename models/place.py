#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base, Review
from sqlalchemy import Float, ForeignKey, Integer, \
    Table, MetaData, Column, String
from sqlalchemy.orm import relationship
from models.__init__ import storage_Type
import engine


class Place(BaseModel, Base):
    """ A place to stay """
    if storage_Type == 'db':
        __tablename__ = Table('places', MetaData(bind=None))
        city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, nullable=False, default=0)
        number_bathrooms = Column(Integer, nullable=False, default=0)
        max_guest = Column(Integer, nullable=False, default=0)
        price_by_night = Column(Integer, nullable=False, default=0)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)
        reviews = relationship("Review", backref="user",
                               cascade="all, delete", passive_deletes=True)
    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

        @property
        def reviews(self):
            reviews = engine.FileStorage.all(Review)
            for key in reviews.keys():
                if reviews[key].place_id == self.id:
                    return reviews[key]
