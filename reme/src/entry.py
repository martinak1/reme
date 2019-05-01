#!/usr/bin/python3

from datetime import datetime, timedelta
from discord import Members, Message, User
import logging
import re

"""
Takes the matches from msg_regex and creates a Datetime from
the groups found
"""
def convert_date(matches):
    converted_date = datetime.toady()
    if matches.group('month'):
        converted_date.replace(month=matches.group('month'))
        converted_date.replace(day=matches.group('day'))

    if matches.group('hour'):
        converted_date.replace(hour=matches.group('hour'))
        converted_date.replace(minute=matches.group('min'))

    if matches.group('offset'):
        if 'd' in matches.group('offset')[:1] or 'D' in matches.group('offset'):
            converted_date += timedelta(days=matches.group('offset')[:-1])
        if 'h' in matches.group('offset')[:1] or 'H' in matches.group('offset'):
            converted_date += timedelta(hours=matches.group('offset')[:-1])
        if 'm' in matches.group('offset')[:1] or 'M' in matches.group('offset'):
            converted_date += timedelta(minutes=matches.group('offset')[:-1])

    return converted_date

# end convert_time

class Entry:

    msg_regex = re.compile(
        r"!reme[ ]*(?P<message>.*)[ ]*((@[ ]*(?P<day>\d{1,2}[-\/]\d{1,2}){0,1}[ ]*(?P<time>\d{1,2}:\d{1,2}))|(?P<offset>\+[ ]*\d+[ ]*[DdHhMm]))"
    )

    def __init__(self):
        id = None
        msg = ""
        users = ()
        attachments = ()
        created = None
        executed = None
    # end __init__


    """
    Return id
    """
    def id(self):
        return self.id
    # end id


    """
    Return msg
    """
    def msg(self):
        return self.msg
    # end msg


    """
    Return users
    """
    def users(self):
        return self.users
    # end users


    """
    Return users flattened
    """
    def flatten_users(self):
        pass


    """
    Return attachments
    """
    def attachments(self):
        return self.attachments
    # end attachments


    """
    Return attachments flattened
    """
    def flatten_attachments(self):
        pass


    """
    Return created
    """
    def created(self):
        return self.created
    # end created


    """
    Return exectuted
    """
    def executed(self):
        return self.executed
    # end executed


    """
    Create an Entry object from the results of a database query
    """
    def from_db(self):
        pass
    # end from_db


    """
    Sets the Entry attributes of the entry by collecting information
    from a message
    """
    def from_msg(self, message):
        matches = Entry.msg_regex.match(message.content)

        if matches:
            self.msg = matches.group('message')
            self.users = message.author + message.mentions
            self.attachments = message.attachments
            self.created = message.created_at
            self.executed = convert_date(matches)

            logging.info("entry.py:from_msg - Entry created from message successfully")
            return True

        else:
            logging.warning("entry.py:from_msg - Message does not match the required format")
            return False
    # end from_msg
