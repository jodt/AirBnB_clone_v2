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
    if storage_Type == 'db':
        db = MySQLdb.connect(
            host=host_test,
            user=user_test,
            passwd=pwd_test,
            db=db_test,
            charset="utf8")
        cur = db.cursor()

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

    @unittest.skipIf(storage_Type != "db", "don't test with filestorage")
    def test_count_row(self):
        self.cur.execute("SELECT COUNT(*) FROM states")
        row = self.cur.fetchone()
        new_state = State(name="California")
        new_state.save()
        self.cur.execute("SELECT * FROM states")
        rows = self.cur.fetchall()
        for row in rows:
            print(row)
        self.cur.close()
        self.db.close()
