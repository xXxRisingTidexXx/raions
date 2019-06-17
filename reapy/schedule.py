#!/bin/env python3
from crontab import CronTab
from core import USER, BASE_DIR
from os.path import join

CRON = CronTab(user=USER)


def run_reaper(reaper, **kwargs):
    job = CRON.new(
        f'python {join(BASE_DIR, "reap.py")} {reaper}',
        f'This\'s the {reaper}\'s schedule'
    )
    job.minute.on(*kwargs['minutes'])
    job.hour.on(*kwargs['hours'])
    return job


def run_sweeper(sweeper, **kwargs):
    job = CRON.new(
        f'python {join(BASE_DIR, "sweep.py")} {sweeper}',
        f'This\'s the {sweeper}\'s schedule'
    )
    job.minute.on(*kwargs['minutes'])
    job.hour.on(*kwargs['hours'])
    return job


run_reaper('OlxFlatReaper', minutes=(0, 15, 30, 45), hours=(23, 0, 1, 2, 3, 4))
run_reaper('DomRiaFlatReaper', minutes=(8, 23, 38, 53), hours=(23, 0, 1, 2, 3, 4))
run_sweeper('OlxFlatSweeper', minutes=(40,), hours=(22,))
run_sweeper('DomRiaFlatSweeper', minutes=(50,), hours=(22,))
CRON.write()
