#!/usr/bin/python3

import PyMySQL

class db:
    __init__(self):
        # Open database connection
        self.db = PyMySQL.connect("140.138.152.207","blazing93","metoer95188","house" )

        # prepare a cursor object using cursor() method
        self.cursor = self.db.cursor()

    execute(self, query):
        # execute SQL query using execute() method.
        self.cursor.execute("SELECT VERSION()")

        # Fetch a single row using fetchone() method.
        data = self.cursor.fetchone()

        return data

    close(self):
        # disconnect from server
        self.db.close()