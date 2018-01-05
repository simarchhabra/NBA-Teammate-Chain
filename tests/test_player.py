#!/usr/bin/python

import sys, os
sys.path.insert(0, os.path.abspath('..'))

import nbateammatechain.players.player as pl
import unittest2 as unittest

JORDAN_URL = "https://www.basketball-reference.com/players/j/jordami01/splits/"
KOBE_URL = "https://www.basketball-reference.com/players/b/bryanko01/splits/"
SIM_URL = "https://www.basketball-reference.com/players/b/bhullsi01/splits/"

class testPlayer(unittest.TestCase):
    def setUp(self):
        self.jordan = pl.create_player(JORDAN_URL)
        self.kobe = pl.create_player(KOBE_URL) 
        self.sim = pl.create_player(SIM_URL)

    def test_name(self):
        """
        Check name attribute is correct
        """
        self.assertTrue(self.kobe._name == "Kobe Bryant")

    def test_height(self):
        """
        Check height attribute is correct
        """
        self.assertTrue(self.sim._height == 89)

    def test_weight(self):
        """
        Check weight attribute is correct
        """
        self.assertTrue(self.jordan._weight == 195)

    def test_career_stats(self):
        """
        Check stats dictionary is correct
        """
        self.assertTrue(self.jordan._career_stats['pts_per_g'] == 30.1)
        self.assertTrue(self.kobe._career_stats['pts'] == 33643)
        self.assertIs(self.sim._career_stats['fg3_pct'], 
                self.sim._career_stats['ft_pct'])

    def test_achievements(self):
        self.assertTrue(self.jordan._achievements['All Star'] == 14)
        self.assertIsNone(self.sim._achievements.get('NBA Champ'))
        self.assertTrue(self.kobe._achievements.get('All NBA') == 15)

if __name__ == '__main__':
    unittest.main()
