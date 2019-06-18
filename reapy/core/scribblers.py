import aiofiles
from datetime import datetime
from asyncio import Lock
from csv import DictWriter
from os.path import join, exists
from . import BASE_DIR


class Scribbler:
    _fields = None

    def __init__(self, scribble_path):
        self._scribble_path = join(BASE_DIR, scribble_path)
        self._row = dict.fromkeys(self._fields, 0)
        self._lock = Lock()

    def write_header(self):
        if not exists(self._scribble_path):
            with open(self._scribble_path, 'w+') as stream:
                DictWriter(stream, fieldnames=self._fields).writeheader()

    async def write(self, field, value):
        if field not in self._fields:
            raise RuntimeError(f'{field} is an inappropriate option')
        async with self._lock:
            current = self._row[field]
            self._row[field] = value if current is None else current + value

    async def scribble(self):
        self._row['written'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        async with aiofiles.open(self._scribble_path, 'ab') as stream:
            DictWriter(stream, fieldnames=self._fields).writerow(self._row)


class ReaperScribbler(Scribbler):
    _fields = (
        'inserted', 'updated', 'duplicated', 'unlocated',
        'unresponded', 'invalidated', 'unparsed', 'written'
    )


class SweeperScribbler(Scribbler):
    _fields = ('junks', 'expired', 'unresponded', 'written')
