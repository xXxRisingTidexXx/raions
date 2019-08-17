"""
*reapy*'s decorator collection for all occasions
"""
from logging import getLogger
from asyncio import run, TimeoutError
from concurrent.futures import ProcessPoolExecutor
from time import time
from typing import Callable, Any
from unittest import TestCase
from aiohttp import ClientSession, ContentTypeError
from aiohttp.client_exceptions import ClientConnectorError, ClientPayloadError, ClientError
from aiohttp.client import TooManyRedirects
from asyncpg import create_pool
from asyncpg.pool import Pool
from asynctest import MagicMock, CoroutineMock
from uvloop import install
from core import TESTING_DSN

logger = getLogger(__name__)


def measurable(name: str) -> Callable:
    """
    Measures and logs approximate coroutine's working time.

    :param name: stage's name
    :return: wrapper with time measuring
    """
    def decorator(function: Callable) -> Callable:
        async def wrapper(*args, **kwargs) -> Any:
            logger.info(f'{name} has been started')
            start = time()
            result = await function(*args, **kwargs)
            end = time()
            logger.info(f'{name} has been finished, it took {end - start:.2f} sec')
            return result
        return wrapper
    return decorator


def networking(function: Callable) -> Callable:
    """
    Handles web & networking errors.

    :param function: target callable
    :return: wrapper with `aiohttp` errors' handling
    """
    async def wrapper(url, *args, **kwargs) -> Any:
        try:
            return await function(url, *args, **kwargs)
        except (
            TimeoutError, TooManyRedirects, ContentTypeError,
            ClientPayloadError, ClientConnectorError
        ) as e:
            logger.error(e)
        except ClientError:
            logger.exception(f'{url} crawling failed')
    return wrapper


def dbtest(function: Callable) -> Callable:
    """
    Asynchronous database testing decorator.

    :param function: testing coroutine
    :return: testing wrapper
    """
    def wrapper(test_case: TestCase):
        install()
        run(runner(function, test_case))

    async def runner(test: Callable, test_case: TestCase):
        async with create_pool(TESTING_DSN) as pool:
            scribbler = MagicMock()
            scribbler.add = CoroutineMock()
            await __truncate_tables(pool)
            try:
                await test(test_case, pool, scribbler)
            finally:
                await __truncate_tables(pool)
    return wrapper


async def __truncate_tables(pool: Pool):
    """
    Clears up the testing database's tables.

    :param pool: database connection pool
    """
    async with pool.acquire() as connection:
        await connection.execute('TRUNCATE TABLE core_user_saved_flats CASCADE')
        await connection.execute('TRUNCATE TABLE core_user CASCADE')
        await connection.execute('TRUNCATE TABLE flats_details CASCADE')
        await connection.execute('TRUNCATE TABLE details CASCADE')
        await connection.execute('TRUNCATE TABLE flats CASCADE')
        await connection.execute('TRUNCATE TABLE geolocations CASCADE')


def processtest(function: Callable) -> Callable:
    """
    Asynchronous CPU bound problems' calculator testing decorator.

    :param function: testing coroutine
    :return: testing wrapper
    """
    def wrapper(test_case: TestCase):
        install()
        run(runner(function, test_case))

    async def runner(test: Callable, test_case: TestCase):
        with ProcessPoolExecutor() as executor:
            scribbler = MagicMock()
            scribbler.add = CoroutineMock()
            await test(test_case, executor, scribbler)
    return wrapper


def webtest(function: Callable) -> Callable:
    """
    Asynchronous web client&processor testing decorator.

    :param function: testing coroutine
    :return: testing wrapper
    """
    def wrapper(test_case: TestCase):
        install()
        run(runner(function, test_case))

    async def runner(test: Callable, test_case: TestCase):
        async with ClientSession() as session:
            with ProcessPoolExecutor() as executor:
                scribbler = MagicMock()
                scribbler.add = CoroutineMock()
                await test(test_case, session, executor, scribbler)
    return wrapper
