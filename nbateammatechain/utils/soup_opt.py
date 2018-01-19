import requests
from bs4 import BeautifulSoup

def soup_streamline(url):
    """
    This function streamlines the soup object creation process
    """
    try:
        r = requests.get(url)
    except:
        return None

    return BeautifulSoup(r.text, "lxml")
