from datetime import date
from decimal import Decimal
from typing import Callable, List
from asyncpg import Connection, Record
from asynctest import CoroutineMock, Mock
from pytest import fixture, mark
from core import TESTING_DSN
from core.repositories import FlatRepository
from core.structs import Flat


@fixture
async def flat_repository() -> FlatRepository:
    try:
        scribbler = Mock()
        scribbler.add = CoroutineMock()
        repository = FlatRepository(scribbler)
        await repository.prepare(TESTING_DSN)
        yield repository
    finally:
        async with repository._pool.acquire() as connection:  # noqa
            await connection.execute('TRUNCATE TABLE flats_details CASCADE')
            await connection.execute('TRUNCATE TABLE details CASCADE')
            await connection.execute('TRUNCATE TABLE flats CASCADE')
            await connection.execute('TRUNCATE TABLE geolocations CASCADE')
        await repository.spare()


def find_flat(function: Callable) -> Callable:
    async def wrapper(flat_repository: FlatRepository):
        async with flat_repository._pool.acquire() as connection:  # noqa
            geolocations = await connection.fetch('''
                INSERT INTO geolocations (point, locality) VALUES 
                (
                    st_setsrid(st_point(44.290987, 32.053208), 4326), 
                    'Sraka'
                ), 
                (
                    st_setsrid(st_point(38.0000345002, 33.0023001), 4326), 
                    'Zalupa'
                )
                RETURNING id
            ''')
            flats = await connection.fetch(
                '''
                INSERT INTO flats (
                    url, avatar, published, price, rate, area, living_area, 
                    kitchen_area, rooms, floor, total_floor, ceiling_height, 
                    geolocation_id, is_visible
                ) VALUES (
                    'xx1', NULL, DATE '2019-04-03', 35000, 500, 
                    70, NULL, NULL, 2, 7, 9, NULL, $1, TRUE
                ),
                (
                    'xx2', 'ava2', DATE '2018-12-18', 50000, 500, 
                    100, 60, 19.5, 3, 8, 9, 2.75, $2, TRUE
                )
                RETURNING id
                ''',
                geolocations[0]['id'], geolocations[1]['id']
            )
            await function(flat_repository, connection, flats, geolocations)
    return wrapper


@mark.asyncio
@find_flat
async def test_find_flat_success(
    flat_repository: FlatRepository, connection: Connection,
    flats: List[Record], geolocations: List[Record]
):
    record = await flat_repository._find_record(  # noqa
        connection,
        Flat(
            url='xx2', geolocation={'point': (38.0000345, 33.0023)},
            area=100, kitchen_area=58.9, living_area=19, rooms=3,
            floor=8, total_floor=9
        )
    )
    assert record['id'] == flats[1]['id']
    assert record['price'] == Decimal('50000.000')
    assert record['geolocation_id'] == geolocations[1]['id']
    record = await flat_repository._find_record(  # noqa
        connection,
        Flat(
            url='xx11', geolocation={'point': (44.29099, 32.05321)},
            area=71.1, kitchen_area=18.3, rooms=2, floor=7, total_floor=9,
            avatar='ava11'
        )
    )
    assert record['id'] == flats[0]['id']
    assert record['price'] == Decimal('35000.000')
    assert record['geolocation_id'] == geolocations[0]['id']
    record = await flat_repository._find_record(  # noqa
        connection, Flat(url='xx1', geolocation={'point': (0, 0)})
    )
    assert record['id'] == flats[0]['id']
    assert record['price'] == Decimal('35000.000')
    assert record['geolocation_id'] == geolocations[0]['id']


@mark.asyncio
@find_flat
async def test_find_flat_failure(
    flat_repository: FlatRepository, connection: Connection,
    flats: List[Record], geolocations: List[Record]  # noqa
):
    assert None is await flat_repository._find_record(  # noqa
        connection,
        Flat(
            url='xx3', geolocation={'point': (34.23, 35.0765)}, area=50,
            kitchen_area=15.7, rooms=2, floor=4, total_floor=9
        )
    )
    assert None is await flat_repository._find_record(  # noqa
        connection,
        Flat(
            url='xx4', geolocation={'point': (51.3, 52.97)}, area=70,
            kitchen_area=24.9, rooms=2, floor=7, total_floor=9
        )
    )
    assert None is await flat_repository._find_record(  # noqa
        connection,
        Flat(
            url='xx5', geolocation={'point': (44.290986, 32.0532)},
            area=58, kitchen_area=18, rooms=2, floor=7, total_floor=9
        )
    )
    assert None is await flat_repository._find_record(  # noqa
        connection,
        Flat(
            url='xx6', geolocation={'point': (44.290986, 32.0532)},
            area=70, kitchen_area=18, rooms=2, floor=3, total_floor=9
        )
    )
    assert None is await flat_repository._find_record(  # noqa
        connection,
        Flat(
            url='xx7', geolocation={'point': (44.3043, 32.09542)},
            area=69.5, rooms=2, floor=7, total_floor=9
        )
    )


@mark.asyncio
@find_flat
async def test_find_flat_almost_found(
    flat_repository: FlatRepository, connection: Connection,
    flats: List[Record], geolocations: List[Record]  # noqa
):
    assert None is await flat_repository._find_record(  # noqa
        connection,
        Flat(
            url='copy1', avatar='avax', published=date(2019, 9, 5),
            geolocation={'point': (38.0000345, 33.0023001)},
            price=Decimal('50500.000'), rate=Decimal('505.000'), area=100,
            living_area=60, kitchen_area=19, rooms=3, floor=9, total_floor=9
        )
    )


def update_flat(function: Callable) -> Callable:
    async def wrapper(flat_repository: FlatRepository):
        async with flat_repository._pool.acquire() as connection:  # noqa
            geolocations = await connection.fetch('''
                INSERT INTO geolocations (locality, point) VALUES
                ('Kyiv', st_setsrid(st_point(48.0987, 53.5098), 4326)),
                ('Cherkasy', st_setsrid(st_point(48.98765, 51.0987), 4326))
                RETURNING id
            ''')
            details = await connection.fetch('''
                INSERT INTO details (feature, value, "group") VALUES 
                ('f1', 'v1', 'g1'), ('f2', 'v2', 'g2'), ('f3', 'v3', 'g3')
                RETURNING id
            ''')
            flats = await connection.fetch(
                '''
                INSERT INTO flats (
                    url, published, price, rate, area, living_area, 
                    kitchen_area, rooms, floor, total_floor, ceiling_height, 
                    geolocation_id, is_visible
                ) VALUES (
                    'url1', '2019-5-15', 35000, 500, 70, 
                    52.8, 13.54, 3, 7, 10, 3, $1, TRUE
                ),
                (
                    'url2', '2019-04-30', 38400, 600, 64.3, 
                    NULL, 14.6, 2, 4, 9, NULL, $2, TRUE
                )
                RETURNING id, price
                ''',
                geolocations[0]['id'], geolocations[1]['id']
            )
            await connection.execute(
                '''
                INSERT INTO flats_details (flat_id, detail_id) 
                VALUES ($1, $2), ($3, $4), ($5, $6)
                ''',
                flats[0]['id'], details[0]['id'], flats[1]['id'],
                details[0]['id'], flats[1]['id'], details[1]['id']
            )
            await function(flat_repository, connection, flats)
    return wrapper


@mark.asyncio
@update_flat
async def test_update_flat_no_update(
    flat_repository: FlatRepository,
    connection: Connection,
    flats: List[Record]
):
    await flat_repository._update_record(  # noqa
        connection,
        flats[0],
        Flat(
            url='durl1', published=date(2019, 5, 17),
            geolocation={'point': (48.0987, 53.5098)},
            price=Decimal('37400.000'), rate=Decimal('534.290'),
            area=70, rooms=3, floor=7, total_floor=10
        )
    )
    record = await connection.fetchrow('''
        SELECT f.id, price FROM flats f
        JOIN flats_details fd ON f.id = fd.flat_id
        JOIN details d ON fd.detail_id = d.id
        JOIN geolocations g ON f.geolocation_id = g.id
        WHERE locality = 'Kyiv' AND feature = 'f1' AND value = 'v1' AND
        url = 'url1' AND rooms = 3 AND floor = 7 AND total_floor = 10 AND
        price = 35000 AND rate = 500
    ''')
    assert record['id'] == flats[0]['id']


@mark.asyncio
@update_flat
async def test_update_flat_success(
    flat_repository: FlatRepository,
    connection: Connection,
    flats: List[Record]
):
    await flat_repository._update_record(  # noqa
        connection,
        flats[1],
        Flat(
            url='url2', published=date(2019, 4, 30),
            geolocation={'point': (48.98765, 51.0987)},
            price=Decimal('36480.000'), rate=Decimal('570.000'),
            area=64, living_area=43, kitchen_area=14.5, rooms=2,
            floor=4, total_floor=9, ceiling_height=2.7, details=['v3']
        )
    )
    record = await connection.fetchrow('''
        SELECT f.id, price FROM flats f
        JOIN flats_details fd ON f.id = fd.flat_id
        JOIN details d ON fd.detail_id = d.id
        JOIN geolocations g ON f.geolocation_id = g.id
        WHERE locality = 'Cherkasy' AND feature = 'f3' AND 
        value = 'v3' AND url = 'url2' AND rooms = 2 AND floor = 4 AND 
        total_floor = 9 AND area = 64 AND living_area = 43 AND 
        kitchen_area = 14.5 AND ceiling_height = 2.7 AND 
        price = 36480 AND rate = 570
    ''')
    assert record['id'] == flats[1]['id']


def distinct_flat(function: Callable) -> Callable:  # TODO
    async def wrapper(flat_repository: FlatRepository):
        async with flat_repository._pool.acquire() as connection:  # noqa

            await function(flat_repository, connection)
    return wrapper


@mark.asyncio
@distinct_flat
async def test_distinct_flat_success(  # TODO
    flat_repository: FlatRepository, connection: Connection
):
    pass


@mark.asyncio
@distinct_flat
async def test_distinct_flat_failure(  # TODO
    flat_repository: FlatRepository, connection: Connection
):
    pass


@mark.asyncio
@distinct_flat
async def test_distinct_flat_update(  # TODO
    flat_repository: FlatRepository, connection: Connection
):
    pass


def create_flat(function: Callable) -> Callable:
    async def wrapper(flat_repository: FlatRepository):
        async with flat_repository._pool.acquire() as connection:  # noqa
            geolocations = await connection.fetch('''
                INSERT INTO geolocations (point) VALUES
                (st_setsrid(st_point(44.0672520115, 43.0985213187), 4326)),
                (st_setsrid(st_point(41.000820002, 39.065000001), 4326))
                RETURNING id
            ''')
            details = await connection.fetch('''
                INSERT INTO details (feature, value, "group") VALUES
                ('state', 'excellent state', 'interior'),
                ('wall_type', 'brick', 'building'),
                ('bathrooms', '2 bathrooms', 'supplies')
                RETURNING id
            ''')
            flats = await connection.fetch(
                '''
                INSERT INTO flats (
                    url, avatar, published, price, rate, area, living_area, 
                    kitchen_area, rooms, floor, total_floor, ceiling_height, 
                    geolocation_id, is_visible
                ) VALUES (
                    'url1', 'ava1', DATE '2019-05-10', 35000, 
                    500, 70, 58, 10, 2, 3, 5, NULL, $1, TRUE
                ),
                (
                    'url2', 'ava2', DATE '2019-03-18', 50000, 
                    556, 90, 60, 24, 3, 10, 12, 2.85, $2, TRUE
                )
                RETURNING id
                ''',
                geolocations[0]['id'], geolocations[1]['id']
            )
            await connection.execute(
                '''
                INSERT INTO flats_details (detail_id, flat_id) 
                VALUES ($1, $2), ($3, $4), ($5, $6)
                ''',
                details[1]['id'], flats[0]['id'], details[1]['id'],
                flats[1]['id'], details[0]['id'], flats[1]['id']
            )
            await function(flat_repository, connection)
    return wrapper


@mark.asyncio
@create_flat
async def test_create_flat_and_new_geolocation(
    flat_repository: FlatRepository, connection: Connection
):
    await flat_repository.create(
        Flat(
            url='url5',
            published=date(2019, 5, 11),
            geolocation={
                'point': (51.342123403, 47.345045433),
                'state': 'Одеська область',
                'locality': 'Одеса',
                'county': 'Приморський район',
                'neighbourhood': 'Ланжерон',
                'road': None,
                'house_number': None
            },
            price=Decimal('35000.000'),
            rate=Decimal('500.000'),
            area=70,
            living_area=51,
            kitchen_area=12,
            rooms=2,
            floor=8,
            total_floor=9,
            ceiling_height=2.75,
            details=['brick']
        )
    )
    assert None is not await connection.fetchrow('''
        SELECT f.id FROM flats f 
        JOIN geolocations g on f.geolocation_id = g.id
        JOIN flats_details fd on fd.flat_id = f.id 
        JOIN details d on d.id = fd.detail_id 
        WHERE locality = 'Одеса' AND 
        county = 'Приморський район' AND
        state = 'Одеська область' AND
        neighbourhood = 'Ланжерон' AND
        point = st_setsrid(
            st_point(51.342123403, 47.345045433), 4326
        ) AND 
        url = 'url5' AND
        price = 35000 AND
        rate = 500 AND
        area = 70 AND
        living_area = 51 AND
        kitchen_area = 12 AND
        rooms = 2 AND
        floor = 8 AND
        total_floor = 9 AND
        value IN ('brick')
    ''')


@mark.asyncio
@create_flat
async def test_create_flat_and_reuse_geolocation(
    flat_repository: FlatRepository, connection: Connection
):
    await flat_repository.create(
        Flat(
            url='url4',
            avatar='ava4',
            published=date(2019, 5, 11),
            geolocation={
                'point': (44.0672520115, 43.0985213187), 'state': None,
                'locality': None, 'county': None, 'neighbourhood': None,
                'road': None, 'house_number': None
            },
            price=Decimal('56000.000'),
            rate=Decimal('800.000'),
            area=70,
            living_area=58,
            kitchen_area=10,
            rooms=2,
            floor=4,
            total_floor=5,
            details=['3 passenger elevators', '2 bathrooms']
        )
    )
    assert None is not await connection.fetchrow('''
        SELECT f.id FROM flats f 
        JOIN geolocations g on f.geolocation_id = g.id 
        JOIN flats_details fd on fd.flat_id = f.id 
        JOIN details d on d.id = fd.detail_id 
        WHERE point = st_setsrid(
            st_point(44.0672520115, 43.0985213187), 4326
        ) AND 
        url = 'url4' AND
        price = 56000 AND
        rate = 800 AND
        area = 70 AND
        living_area = 58 AND
        kitchen_area = 10 AND
        rooms = 2 AND
        floor = 4 AND
        total_floor = 5 AND 
        value IN ('2 bathrooms')
    ''')


@mark.asyncio
@create_flat
async def test_create_failure(
    flat_repository: FlatRepository, connection: Connection
):
    await flat_repository.create(
        Flat(
            url='url1',
            avatar='outstanding duplicate',
            geolocation={
                'point': (44.0672520115, 43.0985213187), 'state': None,
                'locality': None, 'county': None, 'neighbourhood': None,
                'road': None, 'house_number': None
            }
        )
    )
    assert None is await connection.fetchrow('''
        SELECT id FROM flats WHERE url = 'outstanding duplicate'
    ''')
