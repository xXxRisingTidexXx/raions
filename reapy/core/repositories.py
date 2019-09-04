from logging import getLogger
from typing import Any, Optional, List, Dict
from asyncpg import UniqueViolationError, create_pool, Connection, Record
from core.decorators import transactional
from core.scribblers import Scribbler
from core.structs import Flat

logger = getLogger(__name__)


class Repository:
    """
    Main DB abstraction, which encapsulates all interactions withe data
    source. All final derivatives are specialized on the concrete estate
    objects, providing succinct and reusable interface. All repositories
    have something in common with ORM.

    Class properties:
        _max_pool_size: maximal number of concurrent DB connections

    Instance properties:
        _scribbler: statistician, which counts all logical actions
        (insertions, duplicates, etc)
        _pool: low-level collection of DB connections
    """
    _max_pool_size = 45

    def __init__(self, scribbler: Scribbler):
        self._scribbler = scribbler
        self._pool = None

    async def prepare(self, dsn: str):
        """
        Acquires DB connection pool.

        :param dsn: DB server's url
        """
        self._pool = await create_pool(dsn, max_size=self._max_pool_size)

    @transactional('couldn\'t distinct struct')
    async def distinct(
        self, connection: Connection, struct: Any
    ) -> Optional[Any]:
        """
        Tries to recognize the duplicate. If the struct's been in the
        DB, then tries to update the existing row.

        :param connection: DB connection
        :param struct: target entity to be checked
        :return: struct if record with provided values exists
        and None otherwise
        """
        record = await self._find_record(connection, struct)
        if record is None:
            return struct
        await self._update_record(connection, record, struct)

    async def _find_record(
        self, connection: Connection, struct: Any
    ) -> Optional[Record]:
        """
        Tries to find a duplicate of the provided struct.

        :param connection: DB connection
        :param struct: target entity to be checked
        :return: duplicated record or None
        """
        pass

    async def _update_record(
        self, connection: Connection, record: Record, struct: Any
    ):
        """
        Tries to update the existing row according to some rules.
        They concern price minification, profit maximization, etc.

        :param connection: DB connection
        :param record: target DB row to be updated
        :param struct: possible data replacer
        """
        pass

    @transactional('creation failed')
    async def create(self, connection: Connection, struct: Any):
        """
        Stores the validated data structure into the DB and
        updates the progress.

        :param connection: DB connection
        :param struct: target entity to be saved
        """
        await self._create_record(connection, struct)
        await self._scribbler.add('inserted')

    async def _create_record(self, connection: Connection, struct: Any):
        """
        Inserts the target struct into the DB.

        :param connection: DB connection
        :param struct: target entity to be saved
        """
        pass

    async def spare(self):
        """
        Releases DB connection pool.
        """
        await self._pool.close()


class EstateRepository(Repository):
    """
    Upgraded repository, which supplies low-level methods for estate-based
    entities. Also it's aware of estates' geolocations and details.
    """
    async def _create_record(self, connection: Connection, struct: Any):
        geolocation = await self.__get_geolocation(connection, struct.geolocation)
        estate = await self._create_estate(connection, struct, geolocation)
        await self._set_estate_details(connection, estate, struct.details)

    async def __get_geolocation(
        self, connection: Connection, geodict: Dict[str, Any]
    ) -> Record:
        """
        Inserts if not exists and then returns geolocation record.
        Exception handling is needed for the race condition avoidance.

        :param connection: DB connection
        :param geodict: dictionary with geolocation's attributes
        :return:
        """
        try:
            async with connection.transaction():
                return await self.__create_geolocation(connection, geodict)
        except UniqueViolationError:
            return await self.__find_geolocation(connection, geodict)

    @staticmethod
    async def __create_geolocation(
        connection: Connection, geodict: Dict[str, Any]
    ) -> Record:
        """
        Inserts new geolocation record and returns its id.

        :param connection: DB connection
        :param geodict: dictionary with geolocation's attributes
        :return: geolocation's record with id
        """
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
    async def __find_geolocation(
        connection: Connection, geodict: Dict[str, Any]
    ) -> Record:
        """
        Finds geolocation with the provided location's position.

        :param connection: DB connection
        :param geodict: dictionary with geolocation's attributes
        :return:
        """
        return await connection.fetchrow(
            '''
            SELECT id FROM geolocations 
            WHERE point = st_setsrid(st_point($1, $2), 4326)
            ''',
            geodict['point'][0], geodict['point'][1]
        )

    async def _create_estate(
        self, connection: Connection, struct: Any, geolocation: Record
    ) -> Record:
        """
        Inserts estate object into the DB.

        :param connection: DB connection
        :param struct: target entity to be saved
        :param geolocation: geolocation's record
        :return: newly created estate's record
        """
        pass

    async def _set_estate_details(
        self, connection: Connection, estate: Record, details_values: List[str]
    ):
        """
        Binds estate record to the details' records.

        :param connection: DB connection
        :param estate: newly created estate's record
        :param details_values: estate details' list
        """
        details = await self.__find_details(connection, details_values)
        await self._create_estate_details(connection, estate, details)

    @staticmethod
    async def __find_details(
        connection: Connection, details_values: List[str]
    ) -> List[Record]:
        """

        :param connection:
        :param details_values:
        :return:
        """
        details = await connection.fetch(
            'SELECT id FROM details WHERE value = ANY ($1)', details_values
        )
        if len(details) != len(details_values):
            logger.warning(
                f'some of these details are absent in the DB:\n{details_values}'
            )
        return details

    async def _create_estate_details(
        self, connection: Connection, estate: Record, details: List[Record]
    ):
        """

        :param connection:
        :param estate:
        :param details:
        """
        pass


class FlatRepository(EstateRepository):
    """
    Final estate repository, which is in charge of flats' filling.

    Class properties:
        __area_tolerance: approximate error (in meters) of the offer's
        area to distinct duplicates among flats' offers
        __distance_tolerance: approximate error (in meters) of the
        offer's position to distinct duplicates among flats' offers
        (mainly, connected with floating numbers' errors of www.olx.ua)
    """
    __area_tolerance = 1.5
    __distance_tolerance = 4500

    async def _find_record(
        self, connection: Connection, struct: Flat
    ) -> Record:
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

    async def _update_record(
        self, connection: Connection, flat: Record, struct: Flat
    ):
        if flat['price'] > struct.price:
            await self.__delete_flat_details(connection, flat)
            await self._set_estate_details(connection, flat, struct.details)
            await self.__update_flat(connection, flat, struct)
            await self._scribbler.add('updated')
        else:
            await self._scribbler.add('duplicated')

    @staticmethod
    async def __delete_flat_details(connection: Connection, flat: Record):
        """

        :param connection:
        :param flat:
        """
        await connection.execute(
            'DELETE FROM flats_details WHERE flat_id = $1', flat['id']
        )

    @staticmethod
    async def __update_flat(connection: Connection, flat: Record, struct: Flat):
        """

        :param connection:
        :param flat:
        :param struct:
        """
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

    async def _create_estate(
        self, connection: Connection, struct: Flat, geolocation: Record
    ) -> Record:
        return await connection.fetchrow(
            '''
            INSERT INTO flats (
            url, avatar, published, price, rate, area, living_area, 
            kitchen_area, rooms, floor, total_floor, ceiling_height, 
            geolocation_id, is_visible
            ) VALUES (
            $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14
            ) RETURNING id
            ''',
            struct.url, struct.avatar, struct.published, struct.price,
            struct.rate, struct.area, struct.living_area, struct.kitchen_area,
            struct.rooms, struct.floor, struct.total_floor,
            struct.ceiling_height, geolocation['id'], True
        )

    async def _create_estate_details(
        self, connection: Connection, flat: Record, details: List[Record]
    ):
        await connection.executemany(
            '''
            INSERT INTO flats_details (flat_id, detail_id) VALUES ($1, $2)
            ''',
            [(flat['id'], d['id']) for d in details]
        )
