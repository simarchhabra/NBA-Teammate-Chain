#!/usr/bin/python

import sys, os
sys.path.insert(0, os.path.abspath('..'))

from nbateammatechain.players import build_players, player
import unittest2 as unittest
import time

def build_mini_player_dict():
    """
    Builds a mini player dictionary to test player dictionary creation
    """
    # same format as build_player_dict, but ten values max
    player_dict = {}
    pages = build_players.store_alphabetical_URLs()
    for i in range(2):
        UIDs = build_players.store_UIDs(pages[i])
        for j in range(5):
            player_URL = pages[i] + UIDs[j] + "/splits/"
            player_dict[UIDs[j]] = player.create_player(player_URL)
            time.sleep(1)

    return player_dict

class testPlayerDict(unittest.TestCase):
    
    def setUp(self):
        """
        Override default setUp method
        """
        self.player_dict = build_mini_player_dict()

    def test_keys(self):
        """
        Ensures keys of player_dict are correct
        """
        self.assertIsInstance(self.player_dict['abdelal01'], player.Player)
        self.assertIsNone(self.player_dict.get('abdulka01'))
        self.assertIsInstance(self.player_dict['bagarda01'], player.Player)
    
    def test_values(self):
        """
        Ensures values of player_dict are correct
        """
        a = 'All Star'
        ast = 'ast'
        self.assertTrue(self.player_dict['abdursh01'].achievements[a] == 1)
        self.assertTrue(self.player_dict['babbilu01'].career_stats[ast] == 
                215)
        self.assertTrue(self.player_dict['babbch01'].height == 77)

if __name__ == '__main__':
    unittest.main()
