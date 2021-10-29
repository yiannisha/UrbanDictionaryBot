#!/usr/bin/env python3

from scraping.page_scrape import get_word_defs
from scraping.process_data import scrape_def_data

import os
from dotenv import load_dotenv
from discord.ext import commands

Tag_data = dict[str]

# Load Bot's token
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Bot Commands

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print('Bot Connected!')

@bot.command(name='define', help="Quotes the word's definition from Urban Dictionary.")
async def define(ctx, word : str):
    """ Prints definition of word from Urban Dictionary """

    message = _format_message(_get_definition(word))
    await ctx.send(message)


# Functions for getting needed data from scraping

def _get_definition(word : str) -> Tag_data:
    """ Returns a dict with needed data using the scraping module """
    try:
        # get only first definition
        defs = get_word_defs(word)[0]
    except Exception as e:
        # debug
        print(e)
        # TODO: Add exception handling and redirection to on_error event if needed
        pass
    try:
        defs = scrape_def_data([defs])
    except Exception as e:
        # debug
        print(e)
        # TODO: Add exception handling and redirection to on_error event if needed
        pass

    return defs[0]

def _format_message(tag_data : Tag_data) -> str:
    """ Returns string of definition to be used as a message  """

    format_str = ""\
        f"Word: {tag_data['word'].capitalize()}\n\n"\
        f"Meaning: {tag_data['meaning']}\n\n"\
        "Example:\n"\
        f"{tag_data['example']}\n"

    return format_str

# Functions for run.py to interact with

def run():
    bot.run(TOKEN)
