from typing import List, Tuple
from pytest import mark, raises
from core.clixes import Clix
from asyncio import sleep
from random import uniform
from logging import disable


async def create_int_sequence() -> List[int]:
    await sleep(uniform(0.3, 1))
    return [23, 3, 7, 0, 10, -18]


async def create_empty_sequence() -> Tuple:
    await sleep(uniform(0.3, 0.7))
    return ()


@mark.asyncio
async def test_successful_creation():
    assert [23, 3, 7, 0, 10, -18] == await Clix(create_int_sequence).list()
    assert [] == await Clix(create_empty_sequence).list()


@mark.asyncio
async def test_erroneous_creation():
    with raises(TypeError):
        await Clix(lambda: [3, -4, 0]).list()
    with raises(TypeError):
        await Clix(create_int_sequence).apply(lambda i: i)
    with raises(TypeError):
        await Clix({2, -5, 9}).list()  # noqa


async def create_str_sequence() -> List[str]:
    await sleep(uniform(0.2, 1))
    return ['  Titiyo  ', '  Eminem ', '    Metallica ', ' Madonna', 'Lady Gaga  ']


def strip(value: str) -> str:
    return value.strip()


@mark.asyncio
async def test_successful_map():
    assert await Clix(create_str_sequence).map(strip).list() == [
        'Titiyo', 'Eminem', 'Metallica', 'Madonna', 'Lady Gaga'
    ]


@mark.asyncio
async def test_erroneous_map():
    disable()
    with raises(AttributeError):
        await Clix(create_str_sequence).map(lambda i: len(i)).list()
