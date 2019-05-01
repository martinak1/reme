from entry import Entry
import logging
import sqlite3
import threading
import time

"""
TODO
Add try blocks to all DB functions
Add error recovery to all functions
Add logging to all transactions
"""

class DB:
    """
    Establishes a connection to the DB and sets a cursor
    """
    def __init__(self):
        logging.info("db.py:__init__ - Attempting to establish a connection to the DB")
        self.connection = sqlite3.connect('reme.db')
        logging.info("db.py:__init__ - Connection established to DB")
        logging.info("db.py:__init__ - Attempting to create a cursor in the DB")
        self.cursor = self.connection.cursor()
        logging.info("db.py:__init__ - Cursor created sucessfully")
    # end __init__


    """
    Creates the entry table if it does not already exist
    """
    def make_table(self):
        try:
            self.cursor.execute(
                """
                CREATE TABLE entries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    msg TEXT,
                    users TEXT,
                    attachments TEXT,
                    created DATETIME,
                    executed DATETIME
                );
                """
            )
        except sqlite3.Warning:
            logging.error("db.py:make_table - Failed to execute the `reme` table creation sql")
            return False

        logging.info("db.py:make_table - New `reme` table created")
        return True


    """
    Insert an Entry object into the DB
    """
    def add_entry(self, entry):
        try:
            self.cursor.execute(
                """
                INSERT INTO entries( msg, users, attachments, created, executed )
                VALUES( ?, ?, ?, ?, ? );
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


    """
    Commits changes to the DB and closes the connection
    TODO:
    Add error handeling and error logging
    """
    def close(self):
        logging.info("db.py:close - Starting to close the connection to the DB")
        self.connection.commit()
        logging.info("db.py:close - Commited transactions to the DB")
        self.connection.close()
        logging.info("db.py:close - Connection to the DB has closed")

        return True


    """
    Collects the entries from the DB
    """
    def collect(self):
        pass


    """
    Remove entries from the DB
    """
    def remove(self, id):
        pass
