#!/usr/bin/env python

import context
import nbateammatechain.utils.serialize as serialize
import nbateammatechain.players.build_teammates as build_teammates
import unittest2 as unittest

class testSerialize(unittest.TestCase):
    """
    Tests for proper serialization of objects within objects
    """
    @classmethod
    def setUpClass(cls):
        """
        Initialize dictionary objects
        """
        filename = "test_serialize_teammates.pickle"
        cls.dict = build_teammates.full_teammates()
        serialize.create_pickle(filename, cls.dict)
        cls.dict2 = serialize.load_pickle(filename)

    def test_obj_within_dict(self):
        """
        Tests that the teammate objects are correct
        """
        self.assertTrue(cmp(self.dict['thornma01'].teammates, 
            self.dict2['thornma01'].teammates) == 0)

        self.assertIsNone(self.dict['landrca01'].teammates.get('rodrise01'))
        self.assertIsNotNone(self.dict['landrca01'].teammates.get('dorsejo01'))

if __name__ == '__main__':
    unittest.main()
