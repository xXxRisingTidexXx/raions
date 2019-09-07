from core.scribblers import SweeperScribbler
from core.crawlers import OlxFlatCrawler, DomRiaFlatCrawler
from core.parsers import OlxFlatParser, DomRiaFlatParser
from core.repositories import FlatRepository
from core.workers import Worker
from core.decorators import measurable


class Sweeper(Worker):
    _scribbler_class = SweeperScribbler
    _url_prefix = None
    _timeout = 10

    @measurable('sweep')
    async def _work(self):
        pass


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
