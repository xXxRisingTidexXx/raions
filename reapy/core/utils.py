"""
Basic helping tools and instruments
"""
from asyncio import gather
from typing import Union, List, Dict, Any, Callable, Iterable, Iterator, Optional
from aiofiles import open as aioopen
from decimal import Decimal, ROUND_HALF_EVEN
from json import loads
from os.path import exists, join
from re import sub
from core import BASE_DIR


def snake_case(string: str) -> str:
    """
    Converters string in CamelCase into snake_case.

    :param string: a string in CamelCase
    :return: a string in snake_case
    """
    return sub(r'([a-z])([A-Z])', r'\1_\2', string).lower()


def notnull(value: Any) -> bool:
    """
    The simplest check for emptiness

    :param value: target entity
    :return: is target null or not
    """
    return value is not None


def decimalize(
    number: Union[float, str],
    exp: Decimal = Decimal('.001'),
    rounding: str = ROUND_HALF_EVEN
) -> Decimal:
    """
    Rounds the input float number.

    :param number: float number to be rounded
    :param exp: rounding tolerance
    :param rounding: rounding type
    :return: rounded :class:`decimal.Decimal` value
    """
    return Decimal(number).quantize(exp, rounding=rounding)


def exist(path: str):
    """
    Checks the existence of the provided directory or file.

    :param path: file's relative path concernedly the project's root
    :return: file's existence
    """
    return exists(join(BASE_DIR, path))


async def filter_map(
    iterable: Iterable, mapper: Callable, predicate: Callable
) -> Iterator:
    """
    Asynchronously maps, gathers and filters data sequence.

    :param iterable: data sequence
    :param mapper: asynchronous function-converter
    :param predicate: synchronous filtering function
    :return: mapped & filtered collection
    """
    gathered = await gather(*(map(mapper, iterable)))
    return filter(predicate, gathered)


def find(predicate: Callable, iterable: Iterable) -> Optional[Any]:
    """
    Finds the first value of the sequence which satisfies the conditions
    or returns None otherwise.

    :param predicate: function which accepts scalar and returns bool
    :param iterable: target  sequence
    :return: the first desired value or None
    """
    return next(filter(predicate, iterable), None)


def json(path: str) -> Union[List, Dict]:
    """
    Converts the provided .json file into Python objects.

    :param path: file's relative path concernedly the project's root
    :return: file's content
    """
    with open(join(BASE_DIR, path)) as stream:
        return loads(stream.read())


async def load(path: str) -> str:
    """
    Asynchronous file loader.

    :param path: file's relative path concernedly the project's root
    :return: file's content
    """
    async with aioopen(join(BASE_DIR, path)) as stream:
        return await stream.read()


async def dump(path: str, data: str):
    """
    Asynchronous file dumper.

    :param path: file's relative path concernedly the project's root
    :param data: string data to be written
    """
    async with aioopen(join(BASE_DIR, path), 'w+') as stream:
        await stream.write(data)
