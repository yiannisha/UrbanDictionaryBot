
"""Module for processing data scraped from UrbanDictionary"""

from scraping.page_scrape import Tags

from bs4 import BeautifulSoup
from bs4.element import (Tag, NavigableString)

def _get_div_text(tag : Tag, class_name : str) -> str:
    """Returns a string of the tag's text."""
    return tag.find('div', {'class' : class_name}).get_text()

def _get_div_long_text(tag : Tag, class_name : str) -> str:
    """Returns a string of the tag's text with line breaks."""

    f_string = ''

    parent = tag.find('div', {'class' : class_name})

    for child in parent.children:
        if type(child) == NavigableString:
            f_string += str(child)
        elif type(child) == Tag and str(child) == '<br/>':
            f_string += '\n'
        else:
            f_string += child.get_text()

    return f_string

def scrape_def_data(defs : Tags) ->  list[dict]:

    class_names = {
        'word' : 'def-header',
        'meaning' : 'meaning',
        'example' : 'example',
    }

    definition_list = []
    for definition in defs:
        dic = {
            'word' : _get_div_text(definition, class_names['word']),
            'meaning' : _get_div_text(definition, class_names['meaning']),
            'example' : _get_div_long_text(definition, class_names['example']),
        }

        definition_list.append(dic)

    return definition_list
