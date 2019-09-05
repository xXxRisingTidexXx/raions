"""
This module describes the highest *reapy*'s abstractions - workers

Worker - it's a generalization which can be launched via Cron to
fulfil some data processing. They describe the common facade and
each derivative implements the job contract.
"""
from logging import basicConfig, getLogger, INFO
from asyncio import run
from os.path import join
from uvloop import install
from core import BASE_DIR, DEFAULT_DSN
from core.crawlers import Crawler
from core.parsers import Parser
from core.repositories import Repository
from core.scribblers import Scribbler
from core.utils import snake_case

logger = getLogger(__name__)


class Worker:
    """
    General entity which performs data collection/extraction/insertion.
    Defines general interface and fulfills basic stages - logging,
    scribbling, preparation, work, sparing.

    Class properties:
        _scribbler_class: statistician's class
        _crawler_class: networker's class
        _parser_class: HTML processor's class
        _repository_class: DB accessor's class

    Instance properties:
        _name: worker's name
        _scribbler: shapes' statistician
        _crawler: networker
        _parser: HTML processor
        _repository: DB accessor
    """
    _scribbler_class = Scribbler
    _crawler_class = Crawler
    _parser_class = Parser
    _repository_class = Repository

    def __init__(self):
        self._name = snake_case(self.__class__.__name__)
        self._scribbler = self._scribbler_class(
            join(BASE_DIR, f'scribbles/{self._name}.csv')
        )

    # noinspection PyBroadException
    def work(self):
        """
        Defines basic facade and job interface; gradually performs all
        working stages.
        """
        basicConfig(
            level=INFO,
            filename=join(BASE_DIR, f'logs/{self._name}.log'),
            filemode='a+',
            format='%(asctime)s - [%(name)-16s] - [%(levelname)-8s] - %(message)s'
        )
        getLogger('asyncio').setLevel('CRITICAL')
        self._scribbler.scribble_header()
        try:
            install()
            run(self.__run())
            self._scribbler.scribble_row()
        except KeyboardInterrupt:
            logger.info(f'{self._name} was terminated')
        except Exception:
            logger.exception('fatal error occurred')

    async def __run(self):
        """
        Event loop's entry point.
        """
        await self._prepare()
        await self._work()
        await self._spare()

    async def _prepare(self):
        """
        Creates all working units and opens some resources if needed.
        """
        self._crawler = self._crawler_class()
        await self._crawler.prepare()
        self._parser = self._parser_class()
        self._repository = self._repository_class(self._scribbler)
        await self._repository.prepare(DEFAULT_DSN)

    async def _work(self):
        """
        Executes main data flow.
        """
        raise NotImplementedError()

    async def _spare(self):
        """
        Gracefully closes all opened resources.
        """
        await self._crawler.spare()
        await self._repository.spare()
