#!/usr/bin/env python

import sys
import sqlite3
from lib.shout import Shout
from lib.csvreader import CsvReader

class DSlurpy:
    config = ''

    def __init__(self, config=None):
        """
        Parameters:
        config (dict): A dictionary containing the config
        """

        self.err = Shout()

        if config is None:
            self.err.shout('No config specified.')

        self.config = config
        try:
            self.conn = sqlite3.connect(self.config['db_filename'])
        except:
            print('Could not connect to database.')

        self.cur = self.conn.cursor()
        self.create_db()

    def slurp(self):
        """
        Use the CsvReader class to retrieve the data and send it to the DB write method

        Returns:
        bool: Whether or not the method succeeded
        """

        if self.config['data_format'] == 'csv':
            data_reader = CsvReader(self.config['data_filename'])
            data = data_reader.read()
        else:
            self.err.shout('No data format specified.')

        result = self.write_db(data)

        return result

    def write_db(self, data):
        """
        Write the data from the CsvReader class to a SQLite DB

        Parameters:
        data (list(dict)): The .csv data in list form to be written to the DB

        Returns:
        bool: Returns True i.e. an empty DB table if there is no data
        """

        count = 0

        for d in data:
            self.cur.execute('INSERT OR IGNORE INTO vocabulary_scores (year, sex, education, score) VALUES (?, ?, ?, ?)',
                    (d['year'], d['sex'], d['education'], d['vocabulary']))

            if count == 100:
                self.conn.commit()

            count += 1

        self.conn.commit()

        return True

    def create_db(self):
        """
        Create the DB and truncate the table
        """

        self.cur.executescript('''
        DROP TABLE IF EXISTS vocabulary_scores;

        CREATE TABLE vocabulary_scores (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            year TEXT,
            sex TEXT,
            education INTEGER,
            score INTEGER
        );
        ''')

if __name__ == '__main__':
    dslurpy = DSlurpy()
    result = dslurpy.slurp()

    if result:
        print('Success.')
    else:
        print('Failed.')
