
""" Module for making requests and scraping urban dictionary pages """

import requests
from requests.exceptions import InvalidURL, ReadTimeout, HTTPError, ConnectTimeout

from bs4 import BeautifulSoup
from bs4.element import Tag

Tags = list[Tag]

class NoSuchDefinitionException(Exception):
    """ Raised when there is no definition for passed word.  """

def make_request(word : str) -> BeautifulSoup:
    """Make requests and return a BeautifulSoup object of the page."""

    LIMIT = 15
    tries = 0
    error = ConnectTimeout()
    html = ''

    url = "https://www.urbandictionary.com/define.php?term={}".format(word)

    while(type(error) == ConnectTimeout and tries < LIMIT):
        try:
            html = requests.get(url).text
            break
        # except InvalidURL as e:
            # Exception left to be raised for bot to handle

        # except (HTTPError, ReadTimeout) as e:
            # Exception left to be raised for bot to handle

        except ConnectTimeout as e:
            error = e
            tries += 1

    if html:
        soup = BeautifulSoup(html, "html.parser")
    else:
        soup = None

    return soup

def check_word(soup : BeautifulSoup):
    """Checks that the word definition exists"""

    if soup.body.div.find('div', {"class":"shrug space"}) is not None:
        raise NoSuchDefinitionException
    else:
        return True

def scrape_word_defs(soup : BeautifulSoup) -> Tags:
    """Returns word definitions as bs4.element.Tags"""

    return [div for div in soup.find_all('div', {'class' : 'def-panel'})]

def get_word_defs(word : str) -> Tags:
    """Wrapper function for the others functions in this module"""

    soup = make_request(word)
    check_word(soup)
    defs = scrape_word_defs(soup)
    return defs
