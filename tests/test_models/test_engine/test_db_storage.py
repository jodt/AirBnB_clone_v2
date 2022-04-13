"""
Module for testing db_storage
"""
from models.base_model import BaseModel
from time import sleep
import unittest
from models.base_model import storage_Type
from models.engine.db_storage import DBStorage
from models.state import State
import MySQLdb
import os


user_test = os.getenv("HBNB_MYSQL_USER")
host_test = os.getenv("HBNB_MYSQL_HOST")
db_test = os.getenv("HBNB_MYSQL_DB")
pwd_test = os.getenv("HBNB_MYSQL_PWD")


class test_db_storage(unittest.TestCase):
    """
    Class to test the db storage methods
    """

    def test_doc(self):
        """
        Check all the doc of the Amenity Class
        """
        # module documentation
        module = len(DBStorage.__doc__)
        self.assertGreater(module, 0)

        # class documentation
        module_class = len(DBStorage.__doc__)
        self.assertGreater(module_class, 0)

        module_class = len(DBStorage.new.__doc__)
        self.assertGreater(module_class, 0)

        module_class = len(DBStorage.save.__doc__)
        self.assertGreater(module_class, 0)

        module_class = len(DBStorage.delete.__doc__)
        self.assertGreater(module_class, 0)

        module_class = len(DBStorage.reload.__doc__)
        self.assertGreater(module_class, 0)

        module_class = len(DBStorage.all.__doc__)
        self.assertGreater(module_class, 0)

        module_class = len(DBStorage.__init__.__doc__)
        self.assertGreater(module_class, 0)
