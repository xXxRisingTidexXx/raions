import aiofiles
from decimal import Decimal, ROUND_HALF_EVEN
from json import loads
from os.path import exists, join
from os import mkdir
from re import sub
from asyncio import gather
from . import BASE_DIR


def snake_case(s):
    return sub(r'([a-z])([A-Z])', r'\1_\2', s).lower()


def decimalize(number, exp=Decimal('.001'), rounding=ROUND_HALF_EVEN):
    return Decimal(number).quantize(exp, rounding=rounding)


async def map_filter(iterable, mapper, predicate=(lambda x: x is not None)):
    return filter(predicate, await gather(*map(mapper, iterable)))


def makedir(path):
    abs_path = join(BASE_DIR, path)
    if not exists(abs_path):
        mkdir(abs_path)


def exist(path):
    return exists(join(BASE_DIR, path))


def json(path):
    with open(join(BASE_DIR, path)) as stream:
        return loads(stream.read())


async def load(path):
    async with aiofiles.open(join(BASE_DIR, path)) as stream:
        return await stream.read()


async def dump(path, data):
    async with aiofiles.open(join(BASE_DIR, path), 'w+') as stream:
        await stream.write(data)
