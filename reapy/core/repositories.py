import logging
from asyncio import gather
from asyncpg import UniqueViolationError, PostgresError
from .utils import map_filter
from .decorators import measurable


class Repository:
    _portion = 400

    def __init__(self, pool, scribbler):
        self._pool = pool
        self._scribbler = scribbler

    async def delete_all_expired(self, expiration):
        try:
            async with self._pool.acquire() as connection:
                async with connection.transaction():
                    cursor = await self._get_expired_cursor(connection, expiration)
                    records = await cursor.fetch(self._portion)
                    while len(records) > 0:
                        await self._delete_records(connection, records)
                        records = await cursor.fetch(self._portion)
        except PostgresError:
            logging.exception('expired item deletion failed')

    async def _get_expired_cursor(self, connection, expiration):
        pass

    async def _delete_records(self, connection, records):
        pass

    async def delete_all_junks(self, prefix, sieve):
        try:
            async with self._pool.acquire() as connection:
                async with connection.transaction():
                    cursor = await self._get_prefixed_cursor(connection, prefix)
                    records = await cursor.fetch(self._portion)
                    while len(records) > 0:
                        await self._delete_records(
                            connection, await sieve(records)
                        )
                        records = await cursor.fetch(self._portion)
        except PostgresError:
            logging.exception('junk item deletion failed')

    async def _get_prefixed_cursor(self, connection, prefix):
        pass

    @measurable('distinction')
    async def distinct_all(self, structs):
        return await map_filter(structs, self.__distinct)

    async def __distinct(self, struct):
        try:
            async with self._pool.acquire() as connection:
                async with connection.transaction():
                    record = await self._find_record(connection, struct)
                    if record is None:
                        return struct
                    await self._update_record(connection, record, struct)
        except UniqueViolationError:
            pass
        except PostgresError:
            logging.exception(f'couldn\'t distinct struct: {struct.url}')

    async def _find_record(self, connection, struct):
        pass

    async def _update_record(self, connection, record, struct):
        pass

    @measurable('storing')
    async def create_all(self, structs):
        await gather(*map(self.__create, structs))

    async def __create(self, struct):
        try:
            async with self._pool.acquire() as connection:
                async with connection.transaction():
                    await self._create_record(connection, struct)
                    await self._scribbler.write('inserted', 1)
        except UniqueViolationError:
            pass
        except PostgresError:
            logging.exception(f'{struct.url} storing failed')

    async def _create_record(self, connection, struct):
        pass


class EstateRepository(Repository):
    async def _delete_records(self, connection, records):
        try:
            ids = [r['id'] for r in records]
            async with connection.transaction():
                await self._delete_estates_details(connection, ids)
                await self._delete_estates(connection, ids)
        except PostgresError:
            logging.exception('records\' deletion failed')

    async def _delete_estates_details(self, connection, ids):
        pass

    async def _delete_estates(self, connection, ids):
        pass

    async def _create_record(self, connection, struct):
        await self._set_estate_details(
            connection,
            await self._create_estate(
                connection, struct, await self.__get_geolocation(
                    connection, struct.geolocation
                )
            ),
            struct.details
        )

    async def __get_geolocation(self, connection, geodict):
        try:
            async with connection.transaction():
                return await self.__create_geolocation(connection, geodict)
        except UniqueViolationError:
            return await self.__find_geolocation(connection, geodict)

    @staticmethod
    async def __create_geolocation(connection, geodict):
        return await connection.fetchrow(
            '''
            INSERT INTO geolocations (
            state, locality, county, neighbourhood, road, house_number, point
            ) VALUES (
            $1, $2, $3, $4, $5, $6, st_setsrid(st_point($7, $8), 4326)
            ) RETURNING id
            ''',
            geodict['state'], geodict['locality'], geodict['county'],
            geodict['neighbourhood'], geodict['road'], geodict['house_number'],
            geodict['point'][0], geodict['point'][1]
        )

    @staticmethod
    async def __find_geolocation(connection, geodict):
        return await connection.fetchrow(
            '''
            SELECT id FROM geolocations 
            WHERE point = st_setsrid(st_point($1, $2), 4326)
            ''',
            geodict['point'][0], geodict['point'][1]
        )

    async def _create_estate(self, connection, struct, geolocation):
        pass

    async def _set_estate_details(self, connection, estate, details_values):
        await self._create_estate_details(
            connection, estate, await self.__find_details(
                connection, details_values
            )
        )

    @staticmethod
    async def __find_details(connection, details_values):
        details = await connection.fetch(
            'SELECT id FROM details WHERE value = ANY ($1)', details_values
        )
        if len(details) != len(details_values):
            logging.warning(
                f'some of these details are absent in the DB:\n{details_values}'
            )
        return details

    async def _create_estate_details(self, connection, estate, details):
        pass


class FlatRepository(EstateRepository):
    __area_tolerance = 1.5
    __distance_tolerance = 4500

    async def _get_expired_cursor(self, connection, expiration):
        return await connection.cursor(
            '''
            SELECT id FROM flats 
            WHERE current_date >= published + $1::INTERVAL AND
            id NOT IN (SELECT flat_id FROM core_user_saved_flats)
            ''',
            expiration
        )

    async def _delete_estates_details(self, connection, ids):
        await connection.execute(
            'DELETE FROM flats_details WHERE flat_id = ANY ($1)', ids
        )

    async def _delete_estates(self, connection, ids):
        await connection.execute(
            'DELETE FROM flats WHERE id = ANY ($1)', ids
        )

    async def _get_prefixed_cursor(self, connection, prefix):
        return await connection.cursor(
            '''
            SELECT id, url FROM flats
            WHERE url ~ $1 AND 
            id NOT IN (SELECT flat_id FROM core_user_saved_flats)
            ''',
            prefix
        )

    async def _find_record(self, connection, struct):
        return await connection.fetchrow(
            '''
            SELECT f.id, price, geolocation_id 
            FROM flats f JOIN geolocations g ON geolocation_id = g.id
            WHERE url = $1 OR rooms = $2 AND floor = $3 AND 
            total_floor = $4 AND abs(area - $5) <= $6 AND 
            st_distance_sphere(point, st_setsrid(st_point($7, $8), 4326)) <= $9
            ''',
            struct.url, struct.rooms, struct.floor, struct.total_floor,
            struct.area, self.__area_tolerance, struct.geolocation['point'][0],
            struct.geolocation['point'][1], self.__distance_tolerance
        )

    async def _update_record(self, connection, flat, struct):
        if flat['price'] > struct.price:
            await self.__delete_flat_details(connection, flat)
            await self._set_estate_details(connection, flat, struct.details)
            await self.__update_flat(connection, flat, struct)

    @staticmethod
    async def __delete_flat_details(connection, flat):
        await connection.execute(
            'DELETE FROM flats_details WHERE flat_id = $1', flat['id']
        )

    @staticmethod
    async def __update_flat(connection, flat, struct):
        await connection.execute(
            '''
            UPDATE flats SET 
            url = $1, avatar = $2, published = $3, price = $4, rate = $5, 
            area = $6, living_area = $7, kitchen_area = $8, ceiling_height = $9 
            WHERE id = $10
            ''',
            struct.url, struct.avatar, struct.published, struct.price,
            struct.rate, struct.area, struct.living_area, struct.kitchen_area,
            struct.ceiling_height, flat['id']
        )

    async def _create_estate(self, connection, struct, geolocation):
        return await connection.fetchrow(
            '''
            INSERT INTO flats (
            url, avatar, published, price, rate, area, living_area, 
            kitchen_area, rooms, floor, total_floor, ceiling_height, 
            geolocation_id
            ) VALUES (
            $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13
            ) RETURNING id
            ''',
            struct.url, struct.avatar, struct.published, struct.price,
            struct.rate, struct.area, struct.living_area,
            struct.kitchen_area, struct.rooms, struct.floor,
            struct.total_floor, struct.ceiling_height, geolocation['id']
        )

    async def _create_estate_details(self, connection, estate, details):
        await connection.executemany(
            '''
            INSERT INTO flats_details (flat_id, detail_id) VALUES ($1, $2)
            ''',
            [(estate['id'], d['id']) for d in details]
        )
