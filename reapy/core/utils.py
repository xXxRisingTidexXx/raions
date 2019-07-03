"""
Basic helping tools and instruments
"""
import aiofiles
from decimal import Decimal, ROUND_HALF_EVEN
from json import loads
from os.path import exists, join
from os import mkdir
from re import sub
from asyncio import gather
from . import BASE_DIR


def snake_case(s):
    """
    Converters string in CamelCase into snake_case

    >>> snake_case('SpringBootBeanPostProcessor')
    'spring_boot_bean_post_processor'
    >>> snake_case('URL')
    'url'

    :param s: a string in CamelCase
    :return: a string in snake_case
    """
    return sub(r'([a-z])([A-Z])', r'\1_\2', s).lower()


def decimalize(number, exp=Decimal('.001'), rounding=ROUND_HALF_EVEN):
    """
    Rounds the input float number

    >>> decimalize('23.4353')
    Decimal('23.435')
    >>> decimalize(0.0019)
    Decimal('0.002')

    :param number: float number to be rounded
    :param exp: rounding tolerance
    :param rounding: rounding type
    :return: rounded :class:`decimal.Decimal` value
    """
    return Decimal(number).quantize(exp, rounding=rounding)


async def map_filter(iterable, mapper, predicate=(lambda x: x is not None)):
    """
    Asynchronously converts and then filters the input sequence

    :param iterable: the target sequence
    :param mapper: coroutine-converter
    :param predicate: synchronous filtering function
    :return: mapped and filtered iterable
    """
    return filter(predicate, await gather(*map(mapper, iterable)))


def makedir(path):
    """
    Creates the folder by the provided relative path if it doesn't exist

    :param path: folder's relative path concernedly the project's root
    """
    abs_path = join(BASE_DIR, path)
    if not exists(abs_path):
        mkdir(abs_path)


def exist(path):
    """
    Checks the existence of the provided directory or file

    :param path: file's relative path concernedly the project's root
    :return: file's existence
    """
    return exists(join(BASE_DIR, path))


def json(path):
    """
    Converts the provided .json file into Python objects

    :param path: file's relative path concernedly the project's root
    :return: file's content
    """
    with open(join(BASE_DIR, path)) as stream:
        return loads(stream.read())


async def load(path):
    """
    Asynchronous file loader

    :param path: file's relative path concernedly the project's root
    :return: file's content
    """
    async with aiofiles.open(join(BASE_DIR, path)) as stream:
        return await stream.read()


async def dump(path, data):
    """
    Asynchronous file dumper

    :param path: file's relative path concernedly the project's root
    :param data: string data to be written
    """
    async with aiofiles.open(join(BASE_DIR, path), 'w+') as stream:
        await stream.write(data)
