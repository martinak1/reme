from reme import Reme
import discord
import logging

# connect to discord and start the event loop
try:
    reme = Reme()
    reme.run(reme.token)
    reme .wait_until_ready()

except discord.errors.LoginFailure:
    logging.error(
        "reme.py:__main__ - Invalid token passed to discord client"
    )
    exit(2)