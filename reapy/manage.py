#!/bin/env python3
"""
The entry point of each *reapy* script.

The general purpose of *reapy* is data processing; the main working
units are the subclasses of :class:`core.workers.Worker`. Each launch
of the current file is a single tact of the workflow. Dependently
on their specialization, workers modify the common database. That's
why the most suitable workers' usage is via some task scheduler, like
`cron <https://www.ostechnix.com/a-beginners-guide-to-cron-jobs/>`_.
What's more, there's a module with the 'python-crontab' configuration
- :mod:`schedule`.

As it was mentioned, this file is for a single run of the *reapy*'s
script. In console it looks like:
```
$ python manage.py <worker_name>
```
The full list of workers can be found on top of :mod:`core.workers`.
Inappropriate worker's name causes error.
"""
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
