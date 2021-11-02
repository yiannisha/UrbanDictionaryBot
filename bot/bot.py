#!/usr/bin/env python3

from scraping.page_scrape import get_word_defs, NoSuchDefinitionException
from scraping.process_data import scrape_def_data

import os
import sys
from datetime import datetime
from dotenv import load_dotenv
from discord.ext import commands
from typing import List
# import exceptions
from discord.ext.commands import MissingRequiredArgument, TooManyArguments, UserInputError
from requests.exceptions import InvalidURL, ReadTimeout, HTTPError

Tag_data = dict[str]

# Load Bot's token
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print('Bot Connected!')

# Bot Commands

@bot.command(name='define', help="Quotes the word's definition from Urban Dictionary.")
async def define(ctx: commands.Context, *args) -> None:
    """ Prints definition of word from Urban Dictionary """

    search_term = '%20'.join(args)
    message = _format_message(_get_definition(args))
    await ctx.send(message)


# Functions for getting needed data from scraping

def _get_definition(word : str) -> Tag_data:
    """ Returns a dict with needed data using the scraping module """

    # get only first definition
    defs = get_word_defs(word)[0]
    defs = scrape_def_data([defs])

    return defs[0]

def _format_message(tag_data : Tag_data) -> str:
    """ Returns string of definition to be used as a message  """

    format_str = ""\
        f"**__Word__**: {tag_data['word'].capitalize()}\n\n"\
        f"**__Meaning__**: {tag_data['meaning']}\n\n"\
        "**__Example__**:\n"\
        f"{tag_data['example']}\n"

    return format_str

# Catch and handle errors

@bot.event
async def on_command_error(ctx : commands.Context, error : commands.CommandError) -> None:
    """ Handles exceptions raised """

    message = _get_error_message(error)
    # print(message)

    # TODO: add output to stderr for weird errors
    undefined_error_msg = 'General error occured.'
    if message == undefined_error_msg:
        _log_error(error)

    # respond to user
    await ctx.send(message)

# Helper functions for error handling

def _log_error(error: commands.CommandError) -> None:
    """ Logs error passed """

    with open('err.log', 'a', encoding='utf-8') as f:
        sys.stderr = f
        sys.stderr.write(f'{datetime.today()} [ERROR]: {error}\n')


def _get_error_message(error : commands.CommandError) -> str:
    """ Generates a message to be sent back in case of an error """

    message = ''
    original = None

    try:
        original = error.original
    except AttributeError:
        pass

    if original is not None:
        # Handle errors raised from scraping
        scraping_exceptions = [
        (NoSuchDefinitionException, 'Sorry, no such word exists in Urban Dictionary.'),
        (InvalidURL, 'Sorry, this word creates an invalid URL.'),
        (ReadTimeout, 'Sorry, an error occured while making a request to Urban Dictionary'),
        (HTTPError, 'Sorry, an error occured while making a request to Urban Dictionary'),
        ]

        for exc, mes in scraping_exceptions:
            if isinstance(original, exc):
                message = mes
                break

    # Handle error raised from bot
    if not message:
        bot_exceptions = [
        (MissingRequiredArgument, 'Sorry, you specified no word to search for.'),
        (TooManyArguments, 'Whoah there bucko, try one word at a time.'),
        (UserInputError, 'Sorry, there is something wrong with your input.'),
        ]

        for exc, mes in bot_exceptions:
            if isinstance(error, exc):
                message = mes
                break

    if not message:
        message = 'General error occured.'

    return message

# Functions for run.py to interact with

def run():
    bot.run(TOKEN)
