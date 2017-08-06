#!/usr/bin/python3

import pymysql

class db:
    def __init__(self):
        # Open database connection
        self.db = pymysql.connect("localhost","mikey","2gjixdjl3155","bd_captcha" )

    def execute(self, query):
        # connection is not autocommit by default. So you must commit to save
        # your changes.
        self.db = pymysql.connect("localhost","mikey","2gjixdjl3155","bd_captcha" )
        self.db.commit()

        # prepare a cursor object using cursor() method
        cursor = self.db.cursor()
        # execute SQL query using execute() method.
        cursor.execute(query)
        
        # Fetch a single row using fetchone() method.
        data = cursor.fetchone()

        return data

    def close(self):
        # disconnect from server
        self.db.close()