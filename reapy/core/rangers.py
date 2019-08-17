from json import loads, dumps
from core.decorators import measurable
from core.utils import load, exist, dump


class Ranger:
    _stop_url = None
    _range_path = None
    _step = 1

    def __init__(self, crawler, parser):
        self._crawler = crawler
        self._parser = parser

    @measurable('ranging')
    async def range(self):
        stop = await self._parser.parse_stop(
            await self._crawler.get_text(self._stop_url)
        )
        return (
            range(1, 1 + self._step) if stop is None
            else await self.__range(await self.__load_pair(), stop)
        )

    async def __load_pair(self):
        return (
            loads(await load(self._range_path))
            if exist(self._range_path) else [1, 1 + self._step]
        )

    async def __range(self, pair, stop):
        start, stop = (pair[1], pair[1]) if pair[1] < stop else (1, stop + 1)
        await dump(self._range_path, dumps([start, start + self._step]))
        return range(pair[0], stop)


class OlxFlatRanger(Ranger):
    _stop_url = 'https://www.olx.ua/nedvizhimost/kvartiry' \
                '-komnaty/prodazha-kvartir-komnat/?page=1'
    _range_path = 'resources/olx_flat_reaper/range.json'
    _step = 5


class DomRiaFlatRanger(Ranger):
    _stop_url = 'https://dom.ria.com/uk/prodazha-kvartir/?page=1'
    _range_path = 'resources/dom_ria_flat_reaper/range.json'
    _step = 15
