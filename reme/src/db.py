"""
DB.py
This handels the interaction between reme and the database. It can convert
Entry objects to SQL statements and vice versa.
"""

import sqlite3
import logging
from datetime import datetime, timedelta
from entry import Entry
# import threading
# import time

###############################################################################
# TODO
# Add try blocks to all DB functions
# Add error recovery to all functions
# Add logging to all transactions
##############################################################################


class DB:
    """
    An object that handels interaction between reme and the DB
    """

    def __init__(self):
        logging.info(
            "db.py:__init__ - Attempting to establish a connection to the DB"
        )
        self.connection = sqlite3.connect('reme.db')
        logging.info("db.py:__init__ - Connection established to DB")

        self.make_table()

    def make_table(self) -> bool:
        """
j       Creates the entry table if it does not already exist
        """
        try:
            for row in self.connection.execute(
                "select name from sqlite_master where type='table' \
                and name not like 'sqlite_%';"):

                if 'entries' in row:
                    logging.info(
                        "db.py:make_table - Entries table already exists"
                    )
                    return True

            self.connection.execute(
                """
                CREATE TABLE entries (
                    uid INTEGER PRIMARY KEY AUTOINCREMENT,
                    msg TEXT NOT NULL,
                    users TEXT NOT NULL,
                    attachments TEXT,
                    created DATETIME,
                    executed DATETIME NOT NULL
                );
                """
            )

        except sqlite3.Warning:
            logging.error(
                "db.py:make_table [sqlite3.Warning] - Failed to execute the \
                entries table creation sql"
            )
            return False
        except sqlite3.OperationalError:
            logging.error(
                "db.py:make_table [sqlite3.OperationalError] - Failed to \
                create the entries table. Table might already exist"
            )

        logging.info("db.py:make_table - New entries table created")
        return True

    def add_entry(self, entry: Entry) -> bool:
        """
        Insert an Entry object into the DB
        """
        try:
            self.connection.execute(
                """
                INSERT INTO entries(msg, users, attachments, created, executed)
                VALUES(?, ?, ?, ?, ?);
                """,
                entry.msg(),
                entry.flatten_users(),
                entry.flatten_attachments(),
                entry.created().as_str(),
                entry.executed().as_str()
            )
        except sqlite3.Warning:
            logging.error("db.py:add_entry - Failed to add an entry to the DB")
            return False

        logging.info("db.py:add_entry - Added an entry to the DB")
        return True

    def close(self) -> bool:
        """
        Commits changes to the DB and closes the connection
        TODO:
        Add error handeling and error logging
        """
        logging.info(
            "db.py:close - Starting to close the connection to the DB"
        )
        try:
            self.connection.commit()
            logging.info("db.py:close - Commited transactions to the DB")
            self.connection.close()
            logging.info("db.py:close - Connection to the DB has closed")

        except sqlite3.Warning:
            logging.info(
                "db.py:close - Error occured while trying to close the \
                connection to the DB"
            )
            return False

        return True

    def collect(self, timestamp: datetime):
        """
        Collects the entries from the DB
        :param timestamp datetime.datetime: A datetime to compare against the
        executed column
        :return collection list: The DB entries that match the given datetime
        """
        logging.info(
            "db.py:collect - Collecting entries from the DB \
            with timestamp {}".format(timestamp)
        )
        try:
            return [row for row in self.connection.execute(
                "SELECT * FROM entries WHERE executed=?", timestamp)]
        except sqlite3.Warning:
            logging.error(
                "db.py:collect - Failed to retrieve entries from the DB"
            )
            return []

    def remove(self, uid: int) -> bool:
        """
        Remove entries from the DB
        """
        print("UID is {}".format(uid))
        try:
            logging.info(
                "db.py:remove - Attempting to remove row with UID: {}".format(
                    uid
                )
            )
            self.connection.execute(
                "delete from entries where uid=?;",
                uid
            )

        except sqlite3.Warning:
            logging.error(
                "db.py:remove - Failed to remove row with UID: {}".format(
                    uid
                )
            )
            return False

        return True

    def gen_demo(self):
        """
        Creates dummy entries in the DB for testing purposes
        """

        created = datetime.now()

        entries = [
            ("Take pizza out of oven", "Jason", None, created,
                created + timedelta(minutes=1)),
            ("Go to the store for milk", "Patrick", None, created,
                created + timedelta(minutes=2)),
            ("Do laundry", "Alex", None, created,
                created + timedelta(minutes=3)),
            ("Workout!", "JB", None, created, created + timedelta(minutes=4)),
            ("Walk around a little bit", "Alex", None, created,
                created + timedelta(minutes=5)),
            ("Smoke break!", "Alex", None, created,
                created + timedelta(minutes=5))
        ]

        for row in entries:
            self.connection.execute(
                """
                insert into entries(msg, users, attachments, created, executed)
                values (?, ?, ?, ?, ?);
                """,
                row
            )
