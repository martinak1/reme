#!/usr/bin/env python3

import reme 
import discord
import logging
import asyncio

def main():
    # set log level
    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)

    # connect to discord and start the event loop
    try:
        bot = reme.Reme()
        bot.set_token()
        bot.set_db()
        bot.run(bot.token)

        # TODO fill out the logic
        while True:
            entries: list = bot.get_entries()

            for e in entries:
                pass
                #msg: discord.Message =

    except discord.errors.LoginFailure:
        logging.error(
            "__init__.py:main - Invalid token passed to discord client"
        )
        exit(2)
    except Exception as e:
        logging.error(
            "__init__.py:main - An error occurred. {}".format(e)
        )

if __name__ == "__main__":
    main()