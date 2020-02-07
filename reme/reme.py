#!/usr/bin/env python3

"""
reme.py
A Discord bot that reminds you of things.

[Exit Codes]

1 - No token found
2 - Invalid token
"""

import asyncio
from db import DB
import discord
import entry
import logging
import os
import re

class Reme(discord.Client):
    """
    A wrapper class extending discord.client
    """

    # Create the client object
    #client = discord.Client()

    # The database object created by db.py
    db: DB = None
    # The bot token id needed to authenticate on discord
    token: str = None


    def help(self) -> str:
        """
        Returns the help docstring
        :return str
        """
    
        return """
        # Reme - A Discord bot that will send you reminders
        # Author: martinak1
        # Source: https://github.com/martinak1/reme
        # License: BSD-3-Clause

        NOTE: Reme uses a 24 hour clock in order to simplify datetimes

        [Flags]

        -d, debug - Reme echos what you send it after converting it to an Entry object
        -h, help  - Prints this usage docstring

        [Formating]
    
        !reme <Flag> <Message> @ mm/dd/yyyy hh:mm
        !reme <Flag> <Message> @ hh:mm
        !reme <Flag> <Message> +<Delta>[DdHhMm]

        [Examples]
    
        Print this help docstring
            !reme -h || !reme help

        Send a reminder 30 minutes from now
            !reme Take the pizza out of the oven +30m

        Send a reminder at 5:30 pm 
            !reme Go grocery shopping @ 17:30

        Send a reminder on October 30th at 4:30 pm
            !reme DND Session @ 10/30 16:30
    
        """
    # end help

    # TODO possibly delete
    #def add_entry(ent: Entry, database: db.DB) -> bool:
        """
        A wrapper for db.add_entry
        """

        #database.add_entry(ent)

    # end add_entry


    async def check_entries(self):
        """
        Checks the DB for upcoming execution times and calls a function to send the reminders, if it is
        the scheduled time. 
        """
        while(True):
            # TODO Add logic to check the db and add it to a queue.
            #      Then send the reminders
            await asyncio.sleep(60)
    
    # end check_entries

    def set_db(self):
        """
        Initialize a connection to the database
        """
        self.db = DB()

    def set_token(self):       
        #Token filelocation
        token_file: str = 'token.id'
        token: str = None

        try:
            token = os.environ['REME_TOKEN'] 

        except KeyError:
            logging.warning(
                "reme.py:Reme.set_token - REME_TOKEN environment variable not set"
            )

        # If token environment variable is not set, look for a token file
        if not token:
            try:
                with open(token_file) as tf:
                    token = tf.readline()
                    tf.close()

            except FileNotFoundError:
                logging.error(
                    "reme.py:Reme.set_token - REME_TOKEN variable is not set and the token file can not be found"
                )
                exit(1)

        self.token = token

    # end get_token



    ###########################################################################
    ## Discord.py Events
    ###########################################################################

    #@client.event
    async def on_ready(self):
        logging.info(
            'Reme has logged on to the server as {0.user}'.format(self)
        )


    #@client.event
    async def on_connect(self):
        logging.info('Reme has connected to the server')


    #@client.event
    async def on_disconnect(self):
        logging.warning("Reme has disconnected from the server")


    #@client.event
    async def on_resume(self):
        logging.info("Reme has resumed it's connection to the server")


    #@client.event
    async def on_message(self, message):
        # ignore messages from reme
        if message.author == self.user:
            return
    
        # Debug message; Converts it to an entry then responds with what it made
        if message.content.startswith('!reme -d') or message.content.startswith('!reme debug'):
            ent = entry.from_msg(message)
            if ent:
                await message.channel.send('Reme Debug {}'.format(ent))
            else:
                await message.channel.send(
                    'Message was not in the correct format. This is what you sent me: \n{}'
                    .format(message.content)
                )
        # Print the help docstring
        elif message.content.startswith('!reme -h') or message.content.startswith('!reme help'):
            await message.channel.send("{}".format(help()))
    
        # Commit to the DB
        else:
            ent: entry.Entry = entry.from_msg(message)
            if ent: 
                self.db.add_entry(ent)
                await message.author.send(
                    "Got your message {}. I will remind you at {}".format(
                        message.author,
                        ent.executed
                    )
                )

# end Reme class