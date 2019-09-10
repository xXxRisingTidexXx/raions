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
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
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
    async def wrapper(url: str, *args: Any, **kwargs: Any) -> Any:
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
    """
    Simple wrapper suitable for functions which
    produce errors 'cause of None.

    :param function: target callable
    :return: upgraded callable
    """
    def wrapper(*args: Any, **kwargs: Any):
        try:
            return function(*args, **kwargs)
        except (AttributeError, TypeError):
            return None
    return wrapper


def transactional(message: str) -> Callable:
    """
    Simple repo methods' wrapper, which gracefully open/close connections
    and transactions.

    :param message: logging message in a case of an error
    :return: upgraded callable
    """
    def decorator(function: Callable) -> Callable:
        async def wrapper(repository: Any, *args: Any, **kwargs: Any) -> Any:
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
