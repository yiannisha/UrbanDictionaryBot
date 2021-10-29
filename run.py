#!/usr/bin/env python3

""" Start runnning bot. """

from scraping import page_scrape, process_data
from bot import bot

if __name__ == '__main__':
    bot.run()
