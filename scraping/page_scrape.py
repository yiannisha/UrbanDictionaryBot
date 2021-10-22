
""" Module for making requests and scraping urban dictionary pages """

import requests
from bs4 import BeautifulSoup

class NoSuchDefinitionException(Exception):
    """ Raised when there is no definition for passed word.  """

def make_request(term : str):
    """Make requests and return a BeautifulSoup object of the page."""

    url = "https://www.urbandictionary.com/define.php?term={}".format(term)

    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")

    return soup

def check_word(soup : BeautifulSoup, word : str):
    """Checks that the word definition exists"""

    if soup.body.div.find('div', {"class":"shrug space"}) is not None:
        raise NoSuchDefinitionException
