#!/usr/bin/env python

import json
from lib.shout import Shout
from lib.dslurpy import DSlurpy

err = Shout()

def read_config(filename='config.json'):
    with open(filename) as fd:
        config = json.load(fd)

    return config

def print_header(config):
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
    config = read_config()
    print_header(config)

    dslurpy = DSlurpy(config)
    result = dslurpy.slurp()

    if result:
        print('Success.')
    else:
        print('Failure.')

main()
