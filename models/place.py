#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base, storage_Type
from sqlalchemy import Float, ForeignKey, Integer, \
    Column, String, Table
from sqlalchemy.orm import relationship
import models

if storage_Type == "db":
    metadata = Base.metadata
    place_amenity = Table('place_amenity', metadata,
                          Column('place_id', String(60),
                                 ForeignKey('places.id'),
                                 primary_key=True, nullable=False),
                          Column('amenity_id', String(60),
                                 ForeignKey('amenities.id'),
                                 primary_key=True, nullable=False))


class Place(BaseModel, Base):
    """ A place to stay """
    if storage_Type == "db":
        __tablename__ = "places"
        city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, nullable=False, default=0)
        number_bathrooms = Column(Integer, nullable=False, default=0)
        max_guest = Column(Integer, nullable=False, default=0)
        price_by_night = Column(Integer, nullable=False, default=0)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)
        reviews = relationship("Review", backref="place",
                               cascade="all, delete", passive_deletes=True)
        amenities = relationship("Amenity",
                                 secondary=place_amenity, viewonly=False)
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
            """Getter for the review of Place."""
            reviews = models.storage.all(models.review.Review)
            for key in reviews.keys():
                if reviews[key].place_id == self.id:
                    return reviews[key]

        @property
        def amenities(self):
            """Getter for the amenities of Place."""
            amenities = models.storage.all(models.amenity.Amenity)
            list_amenities = []
            for key in amenities.keys():
                if amenities[key].id in self.amenity_ids:
                    list_amenities.append(amenities[key])
            return list_amenities

        @amenities.setter
        def amenities(self, amenity):
            """Setter for the amenities of Place."""
            if isinstance(amenity, models.Amenity):
                self.amenity_ids.append(amenity.id)
