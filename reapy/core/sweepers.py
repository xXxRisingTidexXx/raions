from datetime import timedelta
from .scribblers import SweeperScribbler
from .crawlers import OlxFlatCrawler, DomRiaFlatCrawler
from .parsers import OlxFlatParser, DomRiaFlatParser
from .repositories import FlatRepository
from .workers import Worker
from .decorators import measurable


class Sweeper(Worker):
    _scribbler_class = SweeperScribbler
    _expiration = timedelta(days=210)
    _url_prefix = None
    _timeout = 10

    @measurable('sweep')
    async def _work(self):
        await self._repository.delete_all_expired(self._expiration)
        await self._repository.delete_all_junks(self._url_prefix, self.__sieve)

    async def __sieve(self, records):
        urls = await self._parser.parse_junks(
            await self._crawler.get_offers(
                map(lambda r: {'url': r['url']}, records),
                timeout=self._timeout
            )
        )
        return (r for r in records if r['url'] in urls)


class OlxFlatSweeper(Sweeper):
    _repository_class = FlatRepository
    _crawler_class = OlxFlatCrawler
    _parser_class = OlxFlatParser
    _url_prefix = '^https://www.olx.ua/'


class DomRiaFlatSweeper(Sweeper):
    _repository_class = FlatRepository
    _crawler_class = DomRiaFlatCrawler
    _parser_class = DomRiaFlatParser
    _url_prefix = '^https://dom.ria.com/uk/'
    _timeout = 14
