#!/usr/bin/python3
"""This module instantiates an object of class FileStorage
or DBstorage
"""
from models.base_model import storage_Type

if storage_Type == "db":
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()

storage.reload()
