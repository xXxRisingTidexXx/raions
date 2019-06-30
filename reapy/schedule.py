#!/bin/env python3
"""
*reapy*'s worker manager

This simple script runs a set of workers in parallel via *cron*. Configure
the timings and the worker list if you need.
"""
from crontab import CronTab
from core import USER, BASE_DIR, INTERPRETER_PATH
from os.path import join

CRON = CronTab(user=USER)


def __run_worker(worker, **kwargs):
    job = CRON.new(f'{INTERPRETER_PATH} {join(BASE_DIR, "manage.py")} {worker}')
    job.minute.on(*kwargs['minutes'])
    job.hour.on(*kwargs['hours'])
    return job


__run_worker('OlxFlatReaper', minutes=(0, 15, 30, 45), hours=(23, 0, 1, 2, 3, 4))
__run_worker('DomRiaFlatReaper', minutes=(8, 23, 38, 53), hours=(23, 0, 1, 2, 3, 4))
__run_worker('OlxFlatSweeper', minutes=(40,), hours=(22,))
__run_worker('DomRiaFlatSweeper', minutes=(50,), hours=(22,))
CRON.write()
