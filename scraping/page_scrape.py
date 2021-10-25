
""" Module for making requests and scraping urban dictionary pages """

import requests
from bs4 import BeautifulSoup

class NoSuchDefinitionException(Exception):
    """ Raised when there is no definition for passed word.  """

def make_request(word : str):
    """Make requests and return a BeautifulSoup object of the page."""

    url = "https://www.urbandictionary.com/define.php?term={}".format(word)

    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")

    return soup

def check_word(soup : BeautifulSoup):
    """Checks that the word definition exists"""

    if soup.body.div.find('div', {"class":"shrug space"}) is not None:
        raise NoSuchDefinitionException
    else:
        return True

def scrape_word_defs(soup : BeautifulSoup):
    """Returns word definitions as bs4.element.Tags"""

    return [div for div in soup.find_all('div', {'class' : 'def-panel'})]

def get_word_defs(word : str):
    """Wrapper function for the others functions in this module"""

    soup = make_request(word)
    check_word(soup)
    defs = scrape_word_defs(soup)
    return defs
