from typing import List, Tuple, Dict, Any, Optional
from pytest import mark, raises
from core.clixes import Clix
from asyncio import sleep
from random import uniform
from logging import disable


async def create_int_list() -> List[int]:
    await sleep(uniform(0.3, 1))
    return [23, 3, 7, 0, 10, -18]


async def create_empty_tuple() -> Tuple:
    await sleep(uniform(0.3, 0.7))
    return ()


@mark.asyncio
async def test_successful_creation():
    assert [23, 3, 7, 0, 10, -18] == await Clix(create_int_list).list()
    assert [] == await Clix(create_empty_tuple).list()


@mark.asyncio
async def test_erroneous_creation():
    with raises(TypeError):
        await Clix(lambda: [3, -4, 0]).list()
    with raises(TypeError):
        await Clix(create_int_list).apply(lambda i: i)
    with raises(TypeError):
        await Clix({2, -5, 9}).list()  # noqa


async def create_str_list() -> List[str]:
    await sleep(uniform(0.2, 1))
    return ['  Titiyo  ', '  Eminem ', '    Metallica ', ' Madonna', 'Lady Gaga  ']


def strip(value: str) -> str:
    return value.strip()


@mark.asyncio
async def test_successful_map():
    assert await Clix(create_str_list).map(strip).list() == [
        'Titiyo', 'Eminem', 'Metallica', 'Madonna', 'Lady Gaga'
    ]


@mark.asyncio
async def test_erroneous_map():
    disable()
    with raises(AttributeError):
        await Clix(create_str_list).map(lambda i: len(i)).list()


def create_city(
    name: str, state: Optional[str], country: str,
    longitude: float, latitude: float, population: int
) -> Dict[str, Any]:
    return {
        'name': name, 'state': state, 'country': country,
        'point': (longitude, latitude), 'population': population
    }


async def create_city_list() -> List[Dict[str, Any]]:
    await sleep(uniform(0.2, 1))
    return [
        create_city(
            'Київ', None, 'Україна', 45.89, 51.201, 6000000
        ),
        create_city(
            'Черкаси', 'Черкаська область', 'Україна', 46.013, 48.681, 250000
        ),
        create_city(
            'Севастополь', None, 'Россия', 43.45, 44.0388, 400000
        ),
        create_city(
            'Харків', 'Харківська область', 'Україна', 51.041, 52.1904, 1500000
        ),
        create_city(
            'Рівне', 'Рівненська область', 'Україна', 38.9201, 51.4730, 200000
        ),
        create_city(
            'Одеса', 'Одеська область', 'Україна', 41.791, 44.256, 1500000
        )
    ]


async def get_point(city: Dict[str, Any]) -> Tuple[float, float]:
    await sleep(uniform(0.2, 0.7))
    return city['point']


def is_boxed(point: Tuple[float, float]) -> bool:
    return 40 <= point[0] <= 50 and 44 <= point[1] <= 51


@mark.asyncio
async def test_city_to_point_reform():
    assert await Clix(create_city_list).reform(get_point, is_boxed).list() == [
        (46.013, 48.681), (43.45, 44.0388), (41.791, 44.256)
    ]


def get_population(city: Dict[str, Any]) -> int:
    return city['population']


@mark.asyncio
async def test_erroneous_reform():
    with raises(TypeError):
        await Clix(create_city_list).reform(get_population).list()


def get_locality(city: Dict[str, Any]) -> Dict[str, Any]:
    return {
        'name': city['name'],
        'state': city['state'],
        'country': city['country']
    }


def is_ukrainian_stateful_locality(locality: Dict[str, Any]) -> bool:
    return locality['country'] == 'Україна' and locality['state'] is not None


@mark.asyncio
async def test_successful_sieve():
    assert await (
        Clix(create_city_list)
        .sieve(get_locality, is_ukrainian_stateful_locality)
        .list()
    ) == [
        {'name': 'Черкаси', 'state': 'Черкаська область', 'country': 'Україна'},
        {'name': 'Харків', 'state': 'Харківська область', 'country': 'Україна'},
        {'name': 'Рівне', 'state': 'Рівненська область', 'country': 'Україна'},
        {'name': 'Одеса', 'state': 'Одеська область', 'country': 'Україна'}
    ]


@mark.asyncio
async def test_erroneous_sieve():
    pass


@mark.asyncio
async def test_successful_flatten():
    pass


@mark.asyncio
async def test_erroneous_flatten():
    pass
