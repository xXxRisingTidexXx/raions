from typing import List, Tuple, Dict, Any, Optional
from pytest import mark, raises
from core.clixes import Clix
from logging import disable


async def create_int_list() -> List[int]:
    return [23, 3, 7, 0, 10, -18]


async def create_empty_tuple() -> Tuple:
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
    disable()
    with raises(TypeError):
        await (
            Clix(create_city_list)
            .sieve(get_population, is_ukrainian_stateful_locality)
            .list()
        )
    with raises(AttributeError):
        await Clix(create_city_list).sieve(lambda c: c['population']).list()


async def create_nested_str_list() -> List[List[str]]:
    return [
        ['New menace', 'Killgore', 'Dead island & Co'], [], [],
        ['Alembic', 'Alchemy', 'Asyncio', 'DB'], ['Regnant']
    ]


async def create_people_list() -> List[Dict[str, Any]]:
    return [
        {
            'name': 'Danylo',
            'friends': ['Helga', 'Andrew', 'Michael', 'Andryi', 'Alex']
        },
        {
            'name': 'Voloshyn',
            'friends': []
        },
        {
            'name': 'Andryi',
            'friends': ['Danylo', 'Ann', 'Olya', 'Timur']
        },
        {
            'name': 'Alex',
            'friends': ['Danylo', 'Eugene', 'Cinnamon', 'Andryi', 'Olya']
        }
    ]


@mark.asyncio
async def test_successful_flatten():
    assert await Clix(create_empty_tuple).flatten().list() == []
    assert await Clix(create_nested_str_list).flatten().list() == [
        'New menace', 'Killgore', 'Dead island & Co',
        'Alembic', 'Alchemy', 'Asyncio', 'DB', 'Regnant'
    ]
    assert await (
        Clix(create_people_list)
        .flatten(lambda p: p['friends'])
        .list()
    ) == [
        'Helga', 'Andrew', 'Michael', 'Andryi', 'Alex', 'Danylo', 'Ann',
        'Olya', 'Timur', 'Danylo', 'Eugene', 'Cinnamon', 'Andryi', 'Olya'
    ]


async def create_nullable_nested_list() -> List[Optional[List]]:
    return [['airbnb', 'commode'], [], None, []]


@mark.asyncio
@mark.filterwarnings('ignore')
async def test_erroneous_flatten():
    with raises(TypeError):
        await Clix(create_nullable_nested_list).flatten().list()
    with raises(KeyError):
        await Clix(create_people_list).flatten(lambda p: p['enemies']).list()


def add_last_name(first_name: str) -> str:
    length = len(first_name)
    if length <= 3:
        return f'{first_name} Coolant'
    if length <= 5:
        return f'{first_name} Jerico'
    if length <= 7:
        return f'{first_name} Anduine'
    return f'{first_name} Astarot'


@mark.asyncio
async def test_friend_clix_flow():
    assert await (
        Clix(create_people_list)
        .flatten(lambda p: p['friends'])
        .distinct(lambda fn: fn)
        .map(add_last_name)
        .list()
    ) == [
        'Helga Jerico', 'Andrew Anduine', 'Michael Anduine', 'Andryi Anduine',
        'Alex Jerico', 'Danylo Anduine', 'Ann Coolant', 'Olya Jerico',
        'Timur Jerico', 'Eugene Anduine', 'Cinnamon Astarot'
    ]


def to_int(value: str) -> int:
    return int(value)


@mark.asyncio
async def test_erroneous_clix_flow():
    with raises(ValueError):
        await (
            Clix(create_people_list)
            .flatten(lambda p: p['friends'])
            .sieve(to_int)
            .list()
        )
