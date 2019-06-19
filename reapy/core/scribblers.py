from datetime import datetime
from asyncio import Lock
from csv import DictWriter
from os.path import join, exists
from . import BASE_DIR


class Scribbler:
    _fields = None
    _defaults = None

    def __init__(self, scribble_path):
        self._scribble_path = join(BASE_DIR, scribble_path)
        self._row = {
            self._fields[i]: self._defaults[i]
            for i in range(len(self._fields))
        }
        self._lock = Lock()

    def scribble_header(self):
        if not exists(self._scribble_path):
            with open(self._scribble_path, 'w+') as stream:
                DictWriter(stream, fieldnames=self._fields).writeheader()

    async def add(self, field, value=1):
        async with self._lock:
            self._row[field] += value

    def scribble_row(self):
        self._row['written'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(self._scribble_path, 'a') as stream:
            DictWriter(stream, fieldnames=self._fields).writerow(self._row)


class ReaperScribbler(Scribbler):
    _fields = (
        'inserted', 'updated', 'duplicated', 'unlocated',
        'unresponded', 'invalidated', 'unparsed', 'written'
    )
    _defaults = (0, 0, 0, 0, 0, 0, 0, None)


class SweeperScribbler(Scribbler):
    _fields = ('deleted', 'unresponded', 'written')
    _defaults = (0, 0, None)
