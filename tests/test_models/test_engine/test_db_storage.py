"""
Module for testing db_storage
"""
from models.base_model import BaseModel
from time import sleep
import unittest
from models.base_model import storage_Type
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
