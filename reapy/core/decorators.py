"""
*reapy*'s decorator collection for all occasions
"""
from logging import getLogger
from asyncio import TimeoutError
from time import time
from typing import Callable, Any
from aiohttp import ContentTypeError
from aiohttp.client import TooManyRedirects
from asyncpg import UniqueViolationError, PostgresError
from aiohttp.client_exceptions import (
    ClientConnectorError, ClientPayloadError, ClientError
)

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
            logger.error(f'HTTP connection failed: {e}')
        except ClientError:
            logger.exception(f'{url} crawling failed')
    return wrapper


def nullable(function: Callable) -> Callable:
    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except (AttributeError, TypeError):
            return None
    return wrapper


def transactional(message: str) -> Callable:
    def decorator(function: Callable) -> Callable:
        async def wrapper(repository: Any, *args, **kwargs) -> Any:
            try:
                async with repository._pool.acquire() as connection:  # noqa
                    async with connection.transaction():
                        return await function(
                            repository, connection, *args, **kwargs
                        )
            except UniqueViolationError:
                await repository._scribbler.add('duplicated')  # noqa
            except PostgresError:
                logger.exception(message)
        return wrapper
    return decorator


def connected(message: str) -> Callable:
    def decorator(function: Callable) -> Callable:
        async def wrapper(*args, **kwargs) -> Any:
            try:
                return await function(*args, **kwargs)
            except PostgresError:
                logger.exception(message)
        return wrapper
    return decorator
