#!/usr/bin/env python

import sys

class Shout:
    def shout(self, msg='No error message specified.'):
        print(msg)
        sys.exit(1)

if __name__ == '__main__':
    print("You shouldn't be using this class like this o_O")
