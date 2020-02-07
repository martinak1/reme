#!/usr/bin/env python3
"""
Entry - An intermediary object used to pass information between reme and the
DB. Entry objects can be composed from either output from the DB or from a
series of capture groups made when the msg_regex is used to parse a
discord.Message.
"""

from datetime import datetime, timedelta
from discord import Member, Message  # , User
import logging
import re


class Entry:
    """
    Entry - An object that is created by parsing messages reme recieves. Using
    regular expressions, it extracts the message content, they date the
    reminder should be sent, and the users who should receive the reminder.
    """

    msg_regex = re.compile(
        r"!reme[ ]*(?P<message>.*)[ ]*((@[ ]*(?P<month>\d{1,2})[-\/](?P<day>\d{1,2}){0,1})[ ]*(?P<hour>\d{1,2}):(?P<min>\d{1,2})|\+(?P<offset>[ ]*\d+[ ]*[DdHhMm]))"
    )

    def __init__(self, uid=None, msg="", users=None, channel=None, created=None, 
                executed=None):
        self.uid = uid
        self.msg = msg
        self.users = users
        self.channel = channel
        self.created = created
        self.executed = executed

    # end __init__


    def __str__(self):
        return """
        uid         : {}
        msg         : {}
        users       : {}
        channel     : {}
        created     : {}
        executed    : {}
        """.format(self.uid, self.msg, self.users, self.channel, self.created, self.executed)

    # end __str__

# end Entry


#TODO add support for adding mentions, so they will be alerted as well
def from_msg(message: Message) -> Entry:
    """
    Sets the Entry attributes of the entry by collecting information
    from a message
    :param message discord.Message - A message object sent by discord
    :return ent Entry or None
    """

    ent = Entry()
    matches = Entry.msg_regex.match(message.content)

    if matches:
        ent.msg = matches.group('message')
        ent.users = users_to_string(message) 
        ent.channel = message.channel
        ent.created = datetime.now()
        ent.executed = convert_date(matches)

        print(message.author.id)

        logging.info(
            "entry.py:from_msg - Entry created from message successfully"
        )
        return ent

    logging.warning(
        "entry.py:from_msg - Message does not match the required format"
    )
    return None

# end from_msg


def convert_date(matches: re.Match) -> datetime:
    """
    Takes the matches from msg_regex and creates a Datetime from
    the groups found
    :param matches re.Matches: Capture groups returned by entry.msg_regex when
    parsing a messgage
    :return datetime.datetime: Datetime object composed with the catpure groups
    present
    """
    converted_date: datetime = datetime.today()
    if matches.group('month'):
        converted_date = converted_date.replace(month=int(matches.group('month')))
        converted_date = converted_date.replace(day=int(matches.group('day')))

    if matches.group('hour'):
        converted_date = converted_date.replace(hour=int(matches.group('hour')))
        converted_date = converted_date.replace(minute=int(matches.group('min')))

    # TODO: Fix this; seems to convert everything to minutes instead of respecting
    #       day||hour indicator
    if matches.group('offset'):
        # Match the given offset unit and adjust the time
        if re.match(r'\d+[Dd]{1}', matches.group('offset')):
            converted_date += timedelta(days=int(matches.group('offset')[:-1]))
        if re.match(r'\d+[Hh]{1}', matches.group('offset')):
            converted_date += timedelta(hours=int(matches.group('offset')[:-1]))
        if re.match(r'\d+[Mm]{1}', matches.group('offset')):
            converted_date += timedelta(minutes=int(matches.group('offset')[:-1]))

    # floor to the given minute
    converted_date = converted_date.replace(second=0, microsecond=0)

    return converted_date

# end convert_date


def from_db(sql_output: tuple) -> Entry:
    """
    Create an Entry object from the results of a database query
    :param sql_output tuple - A tuple representation of a row in the DB
    :return Entry or None
    """
    logging.debug(
        "entry.py:from_db - Attempting to create an Entry object from DB \
        output row={}".format(sql_output[0])
    )

    return Entry(
        uid=sql_output[0],
        msg=sql_output[1],
        users=sql_output[2],
        channel=sql_output[3],
        created=sql_output[4],
        executed=sql_output[5]
    )

# end from_db


# TODO might not need to do this; use user = client.get_user(<USER_ID>) to get the user then send them 
#   the message: https://discordpy.readthedocs.io/en/latest/faq.html#how-do-i-send-a-dm
#   user.send(msg)
def to_msg(ent: Entry) -> Message:
    """
    Converts an entry object back into a Discord Message object
    :param Entry
    :return discord.Message
    """
    pass

# end to_msg


#TODO Figure out how to handle when @everyone is mentioned
def users_to_string(message: Message) -> str:
    """
    Collects the message author and mentioned user's ids and combines them into a csv string
    :param message: discord.Message
    :return str
    """
    users: str = "{}".format(message.author.id)

    for m in message.mentions:
        users += ",{}".format(m.id)

    logging.info("entry:users_to_string - Users string generated {}".format(users))
    return users

# end users_to_string


def users_from_string(user_string: str) -> list:
    """
    Converts a csv string into a list of discord users ids
    :param user_string: str
    :return list
    """
    return list(map(int, user_string.split(',')))

# end users_from_string