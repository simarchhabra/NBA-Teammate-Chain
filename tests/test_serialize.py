#!/usr/bin/env python

import context
import nbateammatechain.utils.serialize as serialize
import nbateammatechain.players.player as player
import unittest2 as unittest
import test_build_players

class testSerialize(unittest.TestCase):
    """
    Tests for proper serialization of complex objects
    """
    @classmethod
    def setUpClass(cls):
        """
        Initialize creation of serialized dictionary
        """
        filename = "test_serialize.pickle"
        cls.dict = test_build_players.build_mini_player_dict()
        serialize.create_pickle(filename, cls.dict)
        cls.dict2 = serialize.load_pickle(filename)

    def test_key_loaded_dict(self):
        """
        Tests that the keys of the loaded dict are correct
        """
        self.assertIsNone(self.dict2.get('abdulka01'))
        self.assertIsInstance(self.dict2['bagarda01'], player.Player)
    
    def test_basic_loaded_dict(self):
        """
        Tests that the basic values of the loaded dict are equivalent to the
        original
        """
        self.assertEqual(self.dict['babbch01'].height,
                self.dict2['babbch01'].height)
        self.assertEqual(self.dict['abdulma02'].name,
                self.dict2['abdulma02'].name)
        self.assertEqual(self.dict['babbilu01'].weight,
                self.dict2['babbilu01'].weight)

    def test_advanced_loaded_dict(self):
        """
        Tests that the advanced values (instances within instances) of the 
        loaded dict are equivalent to the original
        """
        self.assertEqual(self.dict['abdulma02'].career_stats['pts_per_g'],
                self.dict2['abdulma02'].career_stats['pts_per_g'])
        self.assertEqual(self.dict['bagarda01'].career_stats['g'],
                self.dict2['bagarda01'].career_stats['g'])
        self.assertIs(self.dict['babbilu01'].achievements.get('All NBA'),
                self.dict2['babbilu01'].achievements.get('All NBA'))

if __name__ == '__main__':
    unittest.main()

