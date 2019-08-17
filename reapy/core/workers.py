from logging import basicConfig, getLogger, INFO
from asyncio import run
from concurrent.futures.process import ProcessPoolExecutor
from os.path import join
from aiohttp import ClientSession
from asyncpg import create_pool
from uvloop import install
from core import BASE_DIR, DEFAULT_DSN
from core.crawlers import Crawler
from core.parsers import Parser
from core.repositories import Repository
from core.scribblers import Scribbler
from core.utils import snake_case, makedir

logger = getLogger(__name__)


class Worker:
    _scribbler_class = Scribbler
    _repository_class = Repository
    _crawler_class = Crawler
    _parser_class = Parser
    _max_pool_size = 10

    def __init__(self):
        self._name = snake_case(self.__class__.__name__)

    # noinspection PyBroadException
    def work(self):
        self.__configure_logging()
        self.__configure_scribbling()
        try:
            install()
            run(self.__run())
            self._scribbler.scribble_row()
        except KeyboardInterrupt:
            logger.info(f'{self._name} was terminated')
        except Exception:
            logger.exception('fatal error occurred')

    def __configure_logging(self):
        makedir('logs')
        basicConfig(
            level=INFO,
            filename=join(BASE_DIR, f'logs/{self._name}.log'),
            filemode='a+',
            format='%(asctime)s - %(name)s - [%(levelname)-8s] - %(message)s'
        )
        getLogger('asyncio').setLevel('CRITICAL')

    def __configure_scribbling(self):
        makedir('scribbles')
        self._scribbler = self._scribbler_class(
            join(BASE_DIR, f'scribbles/{self._name}.csv')
        )
        self._scribbler.scribble_header()

    async def __run(self):
        async with create_pool(DEFAULT_DSN, max_size=self._max_pool_size) as pool:
            async with ClientSession() as session:
                with ProcessPoolExecutor() as executor:
                    await self._prepare(pool, session, executor)
                    await self._work()

    async def _prepare(self, pool, session, executor):
        self._crawler = self._crawler_class(session, self._scribbler)
        self._parser = self._parser_class(executor, self._scribbler)
        self._repository = self._repository_class(pool, self._scribbler)

    async def _work(self):
        pass
