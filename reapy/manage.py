#!/bin/env python3
from sys import argv
from importlib import import_module

MODULES = (import_module('core.reapers'), import_module('core.sweepers'))

if __name__ == '__main__':
    for module in MODULES:
        if hasattr(module, argv[1]):
            getattr(module, argv[1])().work()
            break
    else:
        print(f'worker \'{argv[1]}\' wasn\'t found; try again')
