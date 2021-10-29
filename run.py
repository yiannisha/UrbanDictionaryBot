#!/usr/bin/env python3

""" Start runnning bot. """

import sys

from scraping import page_scrape, process_data
from bot import bot

# Run tests
from scraping.tests import page_scrape_unit_test, process_data_unit_test
import unittest

def run_tests(tests):
    """ Run unit tests for all passed unittest.TestCase objects. """

    loader = unittest.TestLoader()

    suites_list = []
    for test in tests:
        suite = loader.loadTestsFromTestCase(test)
        suites_list.append(suite)

    big_suite = unittest.TestSuite(suites_list)

    runner = unittest.TextTestRunner()
    results = runner.run(big_suite)

    return results

if __name__ == '__main__':

    if(sys.argv[1] == '-t'):
        test_list = [page_scrape_unit_test.Test,
                     process_data_unit_test.Test,]
        run_tests(test_list)

    else:
        bot.run()
