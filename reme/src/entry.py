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
        r"!reme[ ]*(?P<message>.*)[ ]*((@[ ]*(?P<day>\d{1,2}[-\/]\d{1,2}){0,1}[ ]*(?P<time>\d{1,2}:\d{1,2}))|(?P<offset>\+[ ]*\d+[ ]*[DdHhMm]))"
    )

    def __init__(self, uid=None, msg="", users=None, attachments=None,
                 created=None, executed=None):
        self.uid = uid
        self.msg = msg
        self.users = users
        self.attachments = attachments
        self.created = created
        self.executed = executed
    # end __init__

    def __str__(self):
        return """
        uid:            {}
        msg:            {}
        users:          {}
        attachments:    {}
        created:        {}
        executed:       {}
        """.format(self.uid, self.msg, self.users, self.attachments,
                   self.created, self.executed)


    def uid(self) -> int:
        """
        Return uid
        """
        return self.uid
    # end uid

    def msg(self):
        """
        Return msg
        """
        return self.msg
    # end msg

    def users(self) -> list:
        """
        Return users
        :return list(discord.Users)
        """
        return self.users
    # end users

    def flatten_users(self) -> list:
        """
        Return users flattened
        """
        pass

    def attachments(self) -> list:
        """
        Return attachments
        """
        return self.attachments
    # end attachments

    def flatten_attachments(self) -> list:
        """
        Return attachments flattened
        """
        pass

    def created(self) -> datetime:
        """
        Return created
        """
        return self.created
    # end created

    def executed(self) -> datetime:
        """
        Return exectuted
        """
        return self.executed
    # end executed


def from_msg(message: Message) -> bool:
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
        ent.users = message.author + message.mentions
        ent.attachments = message.attachments
        ent.created = message.created_at
        ent.executed = convert_date(matches)

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
    converted_date = datetime.toady()
    if matches.group('month'):
        converted_date.replace(month=matches.group('month'))
        converted_date.replace(day=matches.group('day'))

    if matches.group('hour'):
        converted_date.replace(hour=matches.group('hour'))
        converted_date.replace(minute=matches.group('min'))

    if matches.group('offset'):
        if re.match(r'[Dd]{1}', matches.group('offset')[:1]):
            converted_date += timedelta(days=matches.group('offset')[:-1])
        if re.match(r'[Hh]{1}', matches.group('offset')[:1]):
            converted_date += timedelta(hours=matches.group('offset')[:-1])
        if re.match(r'[Mm]{1}', matches.group('offset')[:1]):
            converted_date += timedelta(minutes=matches.group('offset')[:-1])

    return converted_date


def from_db(sql_output: tuple) -> Entry:
    """
    Create an Entry object from the results of a database query
    :param sql_output tuple - A tuple representation of a row in the DB
    :return Entry or None
    """
    logging.info(
        "entry.py:from_db - Attempting to create an Entry object from DB \
        output row={}".format(sql_output[0])
    )

    return Entry(
        uid=sql_output[0],
        msg=sql_output[1],
        users=sql_output[2],
        attachments=sql_output[3],
        created=sql_output[4],
        executed=sql_output[5]
    )
