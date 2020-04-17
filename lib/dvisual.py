#!/usr/bin/env python

import sqlite3
from lib.shout import Shout

class DVisual:
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
        with sqlite3.connect(self.config['db_filename']) as self.conn:
            self.cur = self.conn.cursor()

    def get_data(self):
        """
        Get the data from the DB

        Returns:
        list: Scores data
        """

        self.cur.execute('SELECT year, sex, education, score from vocabulary_scores;')
        scores = dict()
        education = dict()
        count = dict()

        for row in self.cur :
            if row[0] in scores:
                if row[1] in scores[row[0]]:
                    scores[row[0]][row[1]] += int(row[3])
                    education[row[0]][row[1]] += int(row[2])
                    count[row[0]][row[1]] += 1
                else:
                    scores[row[0]][row[1]] = int(row[3])
                    education[row[0]][row[1]] = int(row[2])
                    count[row[0]][row[1]] = 1
            else:
                # scores[year] = {gender: score}
                scores[row[0]] = {row[1]: int(row[3])}
                education[row[0]] = {row[1]: int(row[2])}
                count[row[0]] = {row[1]: 1}

        scores, education = self.average_scores(scores, education, count)

        return scores, education

    def average_scores(self, scores, education, count):
        """
        Calculate the average of all the scores between genders across years

        Parameters:
        scores (list): The scores list
        education (list): The education list
        count (list): The number of scores per year per gender

        Returns:
        list: The averaged out scores
        """

        for key in scores.keys():
            for k in scores[key].keys():
                scores[key][k] = round(scores[key][k] / count[key][k], 1)
                education[key][k] = round(education[key][k] / count[key][k], 1)

        return scores, education

    def visualise(self):
        """
        A pretty API call that writes the data to a .js object

        Returns:
        bool: Returns True (doesn't check data)
        """

        scores, education = self.get_data()
        self.write_data(scores, education)

        return True

    def write_data(self, scores, education):
        """
        Write the data to .js objects to be visualised with Google

        parameters:
        scores (list): The scores data from the DB
        education (list): The education data from the DB
        """

        vocabulary_data = "vocabularyData = [['Year'"
        education_data = "educationData = [['Year'"

        for gender in ['Male', 'Female']:
            vocabulary_data += ",'" + gender + "'"
            education_data += ",'" + gender + "'"
        vocabulary_data += ']'
        education_data += ']'

        for key in scores.keys():
            vocabulary_data += ",\n['" + key + "', " + str(scores[key]['Male']) + ", " + str(scores[key]['Female']) + "]"
            education_data += ",\n['" + key + "', " + str(education[key]['Male']) + ", " + str(education[key]['Female']) + "]"

        vocabulary_data += '];\n'
        education_data += '];\n'

        with open(self.config['js_filename'], 'w+') as fd:
            fd.write(vocabulary_data)
            fd.write(education_data)

if __name__ == '__main__':
    dvisual = DVisual()
    result = dvisual.visualise()

    if result:
        print('Success.')
    else:
        print('Failed.')
