#!/bin/env python3
from importlib import import_module
from sys import argv

if __name__ == '__main__':
    try:
        if argv[1] != 'Reaper':
            getattr(import_module('core.reapers'), argv[1])().work()
        else:
            raise AttributeError()
    except AttributeError:
        raise RuntimeError(f'{argv[1]} is abstract or absent; try again')
