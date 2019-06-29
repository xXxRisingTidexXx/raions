#!/bin/env python3
from crontab import CronTab
from core import USER, BASE_DIR, INTERPRETER_PATH
from os.path import join

CRON = CronTab(user=USER)


def run_worker(worker, **kwargs):
    job = CRON.new(f'{INTERPRETER_PATH} {join(BASE_DIR, "manage.py")} {worker}')
    job.minute.on(*kwargs['minutes'])
    job.hour.on(*kwargs['hours'])
    return job


run_worker('OlxFlatReaper', minutes=(0, 15, 30, 45), hours=(23, 0, 1, 2, 3, 4))
run_worker('DomRiaFlatReaper', minutes=(8, 23, 38, 53), hours=(23, 0, 1, 2, 3, 4))
run_worker('OlxFlatSweeper', minutes=(40,), hours=(22,))
run_worker('DomRiaFlatSweeper', minutes=(50,), hours=(22,))
CRON.write()
