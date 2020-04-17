#!/usr/bin/env python

import sys
import sqlite3
from shout import Shout
from csvreader import CsvReader

class DSlurpy:
    config = ''

    def __init__(self, config=None):
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
        if self.config['data_format'] == 'csv':
            data_reader = CsvReader(self.config['data_filename'])
            data = data_reader.read()
        else:
            self.err.shout('No data format specified.')

        result = self.write_db(data)

        return result

    def write_db(self, data):
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
