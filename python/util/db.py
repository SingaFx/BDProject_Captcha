#!/usr/bin/python3

import pymysql
from .GetConfig import GetConfig

class db:
    def __init__(self):
        self.config = GetConfig()

        # Open database connection
        self.db = pymysql.connect(self.config.DB_host,self.config.DB_username,self.config.DB_password,self.config.DB_database )

    def execute(self, query):
        # connection is not autocommit by default. So you must commit to save
        # your changes.
        self.db = pymysql.connect(self.config.DB_host,self.config.DB_username,self.config.DB_password,self.config.DB_database )
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