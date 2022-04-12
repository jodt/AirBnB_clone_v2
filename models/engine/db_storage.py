#!/usr/bin/python3
"""
This module define a class to manage the DB storage
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base

import os

user = os.getenv("HBNB_MYSQL_USER")
pwd = os.getenv("HBNB_MYSQL_PWD")
data_base = os.getenv("HBNB_MYSQL_DB")
host = os.getenv("HBNB_MYSQL_HOST")
env = os.getenv("HBNB_ENV")


class DBStorage:
    """
    This class manage the storage in the DB
    """
    __engine = None
    __session = None

    def __init__(self):
        self.__engine = create_engine(
            "mysql+mysqldb://{}:{}@{}/{}".format(
                user, pwd, host, data_base), pool_pre_ping=True)
        if (env == 'test'):
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        #from models.user import User
        from models.state import State
        from models.city import City
        #from models.amenity import Amenity
        #from models.place import Place
        #from models.review import Review
        dict_result = {}
        list_tables = [State, City]
        if(cls):
            for element in self.__session.query(cls).all():
                dict_result[element.__class__.__name__ +
                            "."+element.id] = element
                if "_sa_instance_state" in element.__dict__:
                    element.__dict__.pop("_sa_instance_state")
        else:

            for table in list_tables:
                for row in self.__session.query(table).all():
                    dict_result[row.__class__.__name__ +
                                "."+row.id] = row
                    if "_sa_instance_state" in row.__dict__:
                        row.__dict__.pop("_sa_instance_state")
        return dict_result

    def new(self, obj):
        self.__session.add(obj)

    def save(self):
        self.__session.commit()

    def reload(self):
        #from models.user import User
        from models.state import State
        from models.city import City
        #from models.amenity import Amenity
        #from models.place import Place
        #from models.review import Review
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
            bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()
