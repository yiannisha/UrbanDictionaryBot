
"""Unit testing module for scraping/process_data.py"""

import unittest

from __main__ import (page_scrape, process_data)

class Test(unittest.TestCase):

    def setUp(self):
        self.test_case = page_scrape.get_word_defs('bruh')

    def test_scrape_def_data(self):

        # check return types
        results = process_data.scrape_def_data(self.test_case)
        #print(results[:3])
        self.assertEqual(type(results), list)
        for result in results:
            self.assertEqual(type(result), dict)
            for key, value in result.items():
                self.assertEqual(type(value), str)

        # check that correct data is scraped
        known_values = [
                {
                    'word' : 'Bruh',
                    'meaning' : 'The best answer to literally anything',
                    'example' : ''.join(['Joe: my mom died yesterday',
                                'John: bruuhh',
                                'Joe: Yo my mom just won million dollars',
                                'John: bRuHhh',
                                'Joe: my mom made dinner for us',
                                'John: bruh']),
                },
                {
                    'word' : 'Bruh',
                    'meaning' : ''.join(['1 Word you say when someone says something stupid.',
                                         '2 Greeting']),
                    'example' : ''.join(["Friend: What's Obama's last name.",
                                         'You: Bruh.']),
                },
        ]

        for known, test in zip(known_values, results):
            for key in known.keys():
                # print(test[key].replace('\n', '').replace('\r',''))
                # print(known[key])
                self.assertEqual(test[key].replace('\n', '').replace('\r',''), known[key])
