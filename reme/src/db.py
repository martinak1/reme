from entry import Entry
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
        self.connection = sqlite3.connect('reme.db')
        self.cursor = self.connection.cursor()
    # end __init__


    """
    Creates the entry table if it does not already exist
    """
    def make_table(self):
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
        # Add logging statement

    """
    Insert an Entry object into the DB
    """
    def add_entry(self, entry):
        self.cursor.execute(
            """
            INSERT INTO entries
            """
        )


    """
    Commits changes to the DB and closes the connection
    """
    def close(self):
        self.connection.commit()
        self.connection.close()
