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

    def test_place_id(self):
        """ """
        new = self.value()
        if storage_Type == "db":
            self.assertEqual(new.place_id, None)
        else:
            self.assertEqual(type(new.place_id), str)

    def test_user_id(self):
        """ """
        new = self.value()
        if storage_Type == "db":
            self.assertEqual(new.user_id, None)
        else:
            self.assertEqual(type(new.user_id), str)

    def test_text(self):
        """ """
        new = self.value()
        if storage_Type == "db":
            self.assertEqual(new.text, None)
        else:
            self.assertEqual(type(new.text), str)
