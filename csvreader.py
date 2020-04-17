#!/usr/bin/env python

import csv
from shout import Shout

class CsvReader:
    def __init__(self, filename=None):
        self.err = Shout()

        if filename is None:
            self.err.shout('No .csv file specified')

        self.filename = filename

    def read(self):
        data = list()

        with open(self.filename) as fd:
            dialect = csv.Sniffer().sniff(fd.read(1024))
            fd.seek(0)
            reader = csv.reader(fd, dialect)
            headers = []

            for row in reader:
                if len(headers) == 0:
                    data = list()
                    headers = row
                    continue

                data_row = dict()

                for i, field in enumerate(headers):
                    data_row[field] = row[i]

                data.append(data_row)

        return data

if __name__ == '__main__':
    data_reader = CsvReader('vocab.csv')
    data = data_reader.read();

    print(data)
