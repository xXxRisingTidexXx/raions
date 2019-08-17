"""
Basic helping tools and instruments
"""
from typing import Iterable, Callable, Iterator, Union, List, Dict
from aiofiles import open as aioopen
from decimal import Decimal, ROUND_HALF_EVEN
from json import loads
from os.path import exists, join
from os import mkdir
from re import sub
from asyncio import gather
from core import BASE_DIR


def snake_case(string: str) -> str:
    """
    Converters string in CamelCase into snake_case.

    :param string: a string in CamelCase
    :return: a string in snake_case
    """
    return sub(r'([a-z])([A-Z])', r'\1_\2', string).lower()


def decimalize(
    number: float, exp: Decimal = Decimal('.001'), rounding: str = ROUND_HALF_EVEN
) -> Decimal:
    """
    Rounds the input float number.

    :param number: float number to be rounded
    :param exp: rounding tolerance
    :param rounding: rounding type
    :return: rounded :class:`decimal.Decimal` value
    """
    return Decimal(number).quantize(exp, rounding=rounding)


async def filter_map(
    iterable: Iterable, mapper: Callable, predicate: Callable = (lambda x: x is not None)
) -> Iterator:
    """
    Asynchronously converts and then filters the input sequence.

    :param iterable: the target sequence
    :param mapper: coroutine-converter
    :param predicate: synchronous filtering function
    :return: mapped and filtered iterable
    """
    flow = await gather(*map(mapper, iterable))
    return filter(predicate, flow)


def makedir(path: str):
    """
    Creates the folder by the provided relative path if it doesn't exist.

    :param path: folder's relative path concernedly the project's root
    """
    abs_path = join(BASE_DIR, path)
    if not exists(abs_path):
        mkdir(abs_path)


def exist(path: str):
    """
    Checks the existence of the provided directory or file.

    :param path: file's relative path concernedly the project's root
    :return: file's existence
    """
    return exists(join(BASE_DIR, path))


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
