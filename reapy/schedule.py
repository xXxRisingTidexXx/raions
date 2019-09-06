#!/bin/env python3
"""
*reapy*'s worker manager

This simple script runs a set of workers in parallel via *cron*. Configure
the timings and the worker list if you need.
"""
from typing import Tuple
from crontab import CronTab, CronItem
from core import USER, BASE_DIR, INTERPRETER_PATH
from os.path import join

cron = CronTab(user=USER)


def __run_worker(worker: str, **kwargs: Tuple) -> CronItem:
    """
    Runs the worker via cron's job

    :param worker: *reapy*'s working unit
    :param kwargs: job's timings
    :return: configured job
    """
    job = cron.new(f'{INTERPRETER_PATH} {join(BASE_DIR, "manage.py")} {worker}')
    job.minute.on(*kwargs['minutes'])
    job.hour.on(*kwargs['hours'])
    return job


__run_worker('OlxFlatReaper', minutes=(0, 15, 30, 45), hours=(23, 0, 1, 2, 3, 4))
__run_worker('DomRiaFlatReaper', minutes=(8, 23, 38, 53), hours=(23, 0, 1, 2, 3, 4))
cron.write()
