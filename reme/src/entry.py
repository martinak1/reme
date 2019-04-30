#!/usr/bin/python3

from datetime import datetime, timedelta
from discord import Message, User
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


            return (True, "Entry created from message successfully")
        else:
            return (False, "Message does not match the required format")
    # end from_msg
