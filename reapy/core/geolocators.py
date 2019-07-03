from asyncio import Semaphore, get_event_loop
from re import compile


class Geolocator:
    _geocoding_url = None
    _reversing_url = None
    _limit = 1
    _timeout = 4.5
    _headers = {'User-Agent': 'reapy/1.0'}

    class _Shaft:
        def parse(self, location):
            if self._check(location):
                return {
                    'point': self._get_point(location),
                    'state': self._get_state(location),
                    'locality': self._get_locality(location),
                    'county': self._get_county(location),
                    'neighbourhood': self._get_neighbourhood(location),
                    'road': self._get_road(location),
                    'house_number': self._get_house_number(location)
                }

        def _check(self, location):
            pass

        def _get_point(self, location) -> tuple:
            pass

        def _get_state(self, location) -> str:
            pass

        def _get_locality(self, location) -> str:
            pass

        def _get_county(self, location) -> str:
            pass

        def _get_neighbourhood(self, location) -> str:
            pass

        def _get_road(self, location) -> str:
            pass

        def _get_house_number(self, location) -> str:
            pass

    _shaft_class = _Shaft

    def __init__(self, crawler, executor, scribbler):
        self._crawler = crawler
        self._executor = executor
        self._scribbler = scribbler
        self._loop = get_event_loop()
        self._shaft = self._shaft_class()
        self._semaphore = Semaphore(self._limit)

    async def locate(self, geodict):
        geolocation = await self._loop.run_in_executor(
            self._executor, self._shaft.parse,
            await self.__get_location(geodict)
        )
        if geolocation is not None:
            return geolocation
        await self._scribbler.add('unlocated')

    async def __get_location(self, geodict):
        point = geodict.get('point')
        if point is None:
            json = await self.__get_json(
                self._geocoding_url.format(geodict.get('address'))
            )
            return None if json is None or len(json) == 0 else json[0]
        return await self.__get_json(
            self._reversing_url.format(point[1], point[0])
        )

    async def __get_json(self, url):
        return await self._crawler.get_json(
            url, semaphore=self._semaphore,
            timeout=self._timeout, headers=self._headers
        )


class NominatimGeolocator(Geolocator):
    _geocoding_url = 'https://nominatim.openstreetmap.org/search' \
                     '?format=json&q={}&addressdetails=1&limit=1'
    _reversing_url = 'https://nominatim.openstreetmap.org/reverse' \
                     '?format=json&lat={}&lon={}&addressdetails=1'

    class _Shaft(Geolocator._Shaft):
        _county_pattern = compile(r'([\w\-’\']+ район)\W*')

        def _check(self, location):
            return (
                location is not None and
                'address' in location and
                location['address'].get('country') == 'Україна'
            )

        def _get_point(self, location):
            return float(location['lon']), float(location['lat'])

        def _get_state(self, location):
            state = location['address'].get('state')
            if state is not None and len(state) <= 30:
                return state

        def _get_locality(self, location):
            address = location['address']
            return next(filter(
                lambda l: not (
                    l is None or l.endswith(' рада') or l.endswith(' район')
                ),
                (address.get('city'), address.get('town'), address.get('village'))
            ), None)

        def _get_county(self, location):
            county = self.__search_county(location['address'].get('county'))
            if county is not None:
                return county
            return self.__search_county(location.get('display_name'))

        def __search_county(self, string):
            try:
                county = self._county_pattern.search(string).groups()[0]
                if county[0].isupper():
                    return county
            except (AttributeError, TypeError):
                pass

        def _get_neighbourhood(self, location):
            address = location['address']
            return address.get('neighbourhood', address.get('suburb'))

        def _get_road(self, location):
            address = location['address']
            return address.get('road', address.get('pedestrian'))

        def _get_house_number(self, location):
            house_number = location['address'].get('house_number')
            if house_number is not None and len(house_number) <= 20:
                return house_number

    _shaft_class = _Shaft
