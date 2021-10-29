
"""Unit testing module for scraping/page_scrape.py"""

from bs4 import BeautifulSoup
from bs4.element import Tag

import unittest

from __main__ import page_scrape

class Test(unittest.TestCase):

    def setUp(self):
        self.test_case = page_scrape.make_request('bruh')

    def test_make_request(self):
        """ Tests make_request """

        # Test return type
        result = self.test_case
        self.assertEqual(type(result), BeautifulSoup)

    def test_check_word(self):
        """ Tests check_word """

        # check if right error is raised
        test_case = page_scrape.make_request('sgfw')
        self.assertRaises(page_scrape.NoSuchDefinitionException, page_scrape.check_word, test_case)

    def test_scrape_word_defs(self):
        """ Tests scrape_word_defs """

        # check if list is returned
        test_case = page_scrape.scrape_word_defs(self.test_case)
        self.assertEqual(type(test_case), list)

        # check if items have correct types
        for test in test_case:
            self.assertEqual(type(test), Tag)

    def test_get_word_defs(self):
        """ Tests get_word_defs """

        # check exceptions raised
        self.assertRaises(page_scrape.NoSuchDefinitionException, page_scrape.get_word_defs, 'sfgw')

        # check if list is returned
        test_case = page_scrape.get_word_defs('bruh')
        self.assertEqual(type(test_case), list)

        # check if items have correct types
        for test in test_case:
            self.assertEqual(type(test), Tag)
