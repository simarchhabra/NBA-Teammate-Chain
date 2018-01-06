import sys, os
sys.path.insert(0, os.path.abspath('..'))

import player as pl
import nbateammatechain.utils.soup_opt as soup
import string
import time

SOURCE_URL = "https://basketball-reference.com/players/"
ADD_ON = "/splits/"
MIN_YEAR_DRAFTED = 1984

def store_alphabetical_URLs():
    """
    Returns a list of all possible name urls needed for crawling
    """
    return [SOURCE_URL+letter+'/' for letter in string.lowercase]

def store_UIDs(URL):
    """
    Returns a list of player UID for a URL, where the URL is a name url
    """
    page = soup.soup_streamline(URL) # create a soup for page
    
    # finds a players UID if they entered the league from a minimum year
    # where stats for the players splits are fully accurate
    
    return [str(i.th['data-append-csv']) for i in page.tbody.children if str(i)
            != '\n' and int(str(i.td.string)) >= MIN_YEAR_DRAFTED]

def create_player_dict():
    """
    Creates and returns a dictionary of player objects
    """
    player_dict = {}
    pages = store_alphabetical_URLs() # get a list of player pages to crawl
    for page in pages: # for each name page
        # get a filtered list of player UIDs for each particular name page
        UIDs = store_UIDs(page)
        # for each UID
        for UID in UIDs:
            # store player page URL
            player_URL = page + UID + ADD_ON
            # create player and add to player dictionary
            player_dict[UID] = pl.create_player(player_URL)
            time.sleep(1) # ease up on requests, sleep

    return player_dict