#!/bin/env python3
"""
*reapy*'s worker manager

This simple script runs a set of workers in parallel via *cron*. Configure
the timings and the worker list if you need.
"""
from typing import Iterable
from crontab import CronTab, CronItem
from core import USER, BASE_DIR
from os.path import join

cron = CronTab(user=USER)
interpreter_path = join(BASE_DIR, 'venv/bin/python')
manage_path = join(BASE_DIR, "manage.py")


def __run_worker(worker: str, **kwargs: Iterable[int]) -> CronItem:
    """
    Runs the worker via cron's job

    :param worker: *reapy*'s working unit
    :param kwargs: job's timings
    :return: configured job
    """
    job = cron.new(f'{interpreter_path} {manage_path} {worker}')
    job.minute.on(*kwargs['minutes'])
    job.hour.on(*kwargs['hours'])
    return job


__run_worker(
    'OlxFlatReaper',
    minutes=[0, 20, 40],
    hours=[22, 23, 0, 1, 2, 3, 4, 5, 6, 7]
)
__run_worker(
    'DomRiaFlatReaper',
    minutes=[7, 14, 27, 34, 47, 54],
    hours=[22, 23, 0, 1, 2, 3, 4, 5, 6, 7]
)
cron.write()
