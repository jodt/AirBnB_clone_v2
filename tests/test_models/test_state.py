#!/usr/bin/python3
""" """
from tests.test_models.test_base_model import test_basemodel
from models.base_model import storage_Type
from models.state import State
import unittest


class test_state(test_basemodel):
    """ """

    def __init__(self, *args, **kwargs):
        """ """
        super().__init__(*args, **kwargs)
        self.name = "State"
        self.value = State

    def test_name3(self):
        """ """
        new = self.value()
        if storage_Type == "db":
            self.assertEqual(new.name, None)
        else:
            self.assertEqual(type(new.name), str)
