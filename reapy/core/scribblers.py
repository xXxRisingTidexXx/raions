"""
This module describes *scribblers* - vigilant *reapy*'s statisticians

Generally, each worker needs an auxiliary entity whose main purpose is to
write all worker's numeric achievements. :class:`core.scribblers.Scribbler`
and its successors are *.csv* file writers. This text format is very simple
and suitable for table comprehensions, that's why *scribblers* dump all their
reports into comma-separated-values files.
"""
from datetime import datetime
from asyncio import Lock
from csv import DictWriter
from os.path import join, exists
from . import BASE_DIR


class Scribbler:
    """
    The parent of the statisticians' hierarchy

    Rewrites all important worker's shapes into appropriate .csv file.
    Shapes' set and their defaults depend on the worker. Each *reapy*'s
    tact requires worker to dump its results, that's why each tact
    produces 1 row in the 'scribble' file. Basically, any scribble's line
    contains a few numeric params and the record's date&time.
    """
    _fields = None
    _defaults = None

    def __init__(self, scribble_path):
        """
        Defines target file's path and fills the default data

        :param scribble_path: scribble file's relative path
        """
        self._scribble_path = join(BASE_DIR, scribble_path)
        self._row = {
            self._fields[i]: self._defaults[i]
            for i in range(len(self._fields))
        }
        self._lock = Lock()

    def scribble_header(self):
        """
        Defines .csv headers and creates the scribble's file if it's absent
        """
        if not exists(self._scribble_path):
            with open(self._scribble_path, 'w+') as stream:
                DictWriter(stream, fieldnames=self._fields).writeheader()

    async def add(self, field, value=1):
        """
        Asynchronously increases the filed's value

        :param field: numeric field to be increased
        :param value: increasing value
        """
        async with self._lock:
            self._row[field] += value

    def scribble_row(self):
        """
        Rewrites another line to the scribble's file, pointing
        the date&time of the record
        """
        self._row['written'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(self._scribble_path, 'a') as stream:
            DictWriter(stream, fieldnames=self._fields).writerow(self._row)


class ReaperScribbler(Scribbler):
    """
    This scribbler is specialized on the :class:`core.reapers.Reaper`'s
    statistics. Generally, reapers add new and update existing data,
    that's why their reports contain many shapes concernedly
    inserted/duplicated/invalid data.
    """
    _fields = (
        'inserted', 'updated', 'duplicated', 'unlocated',
        'unresponded', 'invalidated', 'unparsed', 'written'
    )
    _defaults = (0, 0, 0, 0, 0, 0, 0, None)


class SweeperScribbler(Scribbler):
    """
    This scribbler is specialized on the :class:`core.sweepers.Sweeper`'s
    statistics. Mainly, sweepers delete junk and expired data so that their
    scribbles contain mainly data concernedly deletions.
    """
    _fields = ('deleted', 'unresponded', 'written')
    _defaults = (0, 0, None)
