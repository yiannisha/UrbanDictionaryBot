
from bs4 import BeautifulSoup
import unittest

from __main__ import page_scrape

class Test(unittest.TestCase):

    def test_make_request(self):
        """ Tests make_request """

        # Test return type
        test_case = 'bruh'
        result = page_scrape.make_request(test_case)
        self.assertEqual(type(result), BeautifulSoup)

    def test_check_word(self):
        """ Tests check_word """

        # check if right error is raised
        test_case = page_scrape.make_request("sfgw")
        self.assertRaises(page_scrape.NoSuchDefinitionException, page_scrape.check_word, test_case, "sfgw")
