#!/usr/bin/env python

import json
from lib.shout import Shout
from lib.dslurpy import DSlurpy
from lib.dvisual import DVisual

err = Shout()

def read_config(filename='config.json'):
    """
    Open and parse the config file

    Parameters:
    filename (string): The filename to open
    """

    with open(filename) as fd:
        config = json.load(fd)

    return config

def print_header(config):
    """
    Print the welcome header
    """

    print('-----------------------------------------------------')
    print(' Welcome to Data Slurpy.')
    print('')
    print(' Defaults for the data to be used and how it is used')
    print(' can be found in config.py')
    print('-----------------------------------------------------')
    print('')
    print('Press any key to start parsing', config['data_filename'], '...')
    input()

def main():
    """
    The program entry point
    """

    config = read_config()
    print_header(config)

    dslurpy = DSlurpy(config)
    result = dslurpy.slurp()

    if result:
        dvisual = DVisual(config)
        result = dvisual.visualise()

        print('You can view the data from the', config['html_filename'], 'file.')

        if result:
            print('Success.')
        else:
            err.shout('Failure.')
    else:
        err.shout('Failure.')

main()
