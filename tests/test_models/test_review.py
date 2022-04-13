#!/usr/bin/python3
""" """
from tests.test_models.test_base_model import test_basemodel
from models.review import Review
import unittest
from models.base_model import storage_Type


class test_review(test_basemodel):
    """ """

    def __init__(self, *args, **kwargs):
        """ """
        super().__init__(*args, **kwargs)
        self.name = "Review"
        self.value = Review

    @unittest.skipIf(storage_Type == 'db', "do not test with dbstorage")
    def test_place_id(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.place_id), str)

    @unittest.skipIf(storage_Type == 'db', "do not test with dbstorage")
    def test_user_id(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.user_id), str)

    @unittest.skipIf(storage_Type == 'db', "do not test with dbstorage")
    def test_text(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.text), str)
