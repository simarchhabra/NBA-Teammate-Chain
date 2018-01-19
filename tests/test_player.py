#!/usr/bin/env python

import context
import nbateammatechain.players.player as pl
import unittest2 as unittest

JORDAN_URL = "https://www.basketball-reference.com/players/j/jordami01/splits/"
KOBE_URL = "https://www.basketball-reference.com/players/b/bryanko01/splits/"
SIM_URL = "https://www.basketball-reference.com/players/b/bhullsi01/splits/"

class testPlayer(unittest.TestCase):
    """
    Tests for correct player attribute initialization and parsing
    """
    @classmethod
    def setUpClass(cls):
        """
        Class method to initialize member variables
        """
        cls.jordan = pl.create_player(JORDAN_URL)
        cls.kobe = pl.create_player(KOBE_URL) 
        cls.sim = pl.create_player(SIM_URL)

    def test_name(self):
        """
        Check name attribute is correct
        """
        self.assertTrue(self.kobe.name == "Kobe Bryant")

    def test_height(self):
        """
        Check height attribute is correct
        """
        self.assertTrue(self.sim.height == 89)

    def test_weight(self):
        """
        Check weight attribute is correct
        """
        self.assertTrue(self.jordan.weight == 195)

    def test_year(self):
        """
        Check year attribute is correct
        """
        self.assertTrue(self.jordan.year == 1985)

    def test_career_stats(self):
        """
        Check stats dictionary is correct
        """
        self.assertTrue(self.jordan.career_stats['pts_per_g'] == 30.1)
        self.assertTrue(self.kobe.career_stats['pts'] == 33643)
        self.assertIs(self.sim.career_stats['fg3_pct'], self.sim.career_stats['ft_pct'])

    def test_achievements(self):
        """
        Check achievements dictionary is correct
        """
        self.assertTrue(self.jordan.achievements['All Star'] == 14)
        self.assertIsNone(self.sim.achievements.get('NBA Champ'))
        self.assertTrue(self.kobe.achievements.get('All NBA') == 15)

if __name__ == '__main__':
    unittest.main()
