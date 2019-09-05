from json import loads, dumps
from core.utils import load, exist, dump
from logging import getLogger

logger = getLogger(__name__)


class Ranger:
    _stop_url = None
    _range_path = None
    _step = 1

    def __init__(self, crawler, parser):
        self._crawler = crawler
        self._parser = parser

    async def range(self):
        page = await self._crawler.get_text(self._stop_url)
        stop = self._parser.parse_stop(page)
        segment = (
            range(1, 1 + self._step) if stop is None
            else await self.__dump_and_range(stop)
        )
        logger.info(f'index range is [{segment.start}; {segment.stop})')
        return segment

    async def __dump_and_range(self, stop):
        start, new_start = await self.__load_start(), 1
        if start + self._step < stop:
            stop = start + self._step
            new_start = stop
        await dump(self._range_path, dumps({'start': new_start}))
        return range(start, stop)

    async def __load_start(self):
        if not exist(self._range_path):
            return 1
        contents = await load(self._range_path)
        return loads(contents)['start']


class OlxFlatRanger(Ranger):
    _stop_url = 'https://www.olx.ua/nedvizhimost/kvartiry' \
                '-komnaty/prodazha-kvartir-komnat/?page=1'
    _range_path = 'resources/olx_flat_reaper/range.json'
    _step = 5


class DomRiaFlatRanger(Ranger):
    _stop_url = 'https://dom.ria.com/uk/prodazha-kvartir/?page=1'
    _range_path = 'resources/dom_ria_flat_reaper/range.json'
    _step = 15
