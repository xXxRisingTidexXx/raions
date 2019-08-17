"""
This module describes a bunch of "geographic" classes

One of the most important step of the data flow is position determination.
Objects are situated all over the territory and the service has to know
their coordinates. The classes below use the public API to carry out
geocoding & reversing.
"""
from asyncio import Semaphore, get_event_loop
from concurrent.futures import Executor
from re import compile
from typing import Dict, Any, Tuple, Union, List, Optional
from core.crawlers import Crawler
from core.scribblers import Scribbler


class Geolocator:
    """
    Initial asynchronous geo researcher. It leverages an HTTP client
    to perform geocoding & reversing requests and an executor to fulfil
    CPU bound calculations.

    Class properties:
        _geocoding_url: URL template to perform geocoding requests
        _reversing_url: URL template to perform reversing requests
        _limit: a number of concurrent HTTP requests to the API
        _timeout: default HTTP request timeout
        _headers: API request headers, like User-Agent, etc.
        _shaft_class: an inner class, which wraps all
        synchronous calculations (to be able to call them in the executor)

    Instance properties:
        _crawler: asynchronous HTTP client
        _executor: CPU bound problems' calculator
        _scribbler: statistics entity which writes success & failure shapes
        _semaphore: HTTP connection "restriction frame"
        _loop: asyncio event loop
        _shaft: synchronous functions' wrapper

    """
    _geocoding_url = None
    _reversing_url = None
    _limit = 1
    _timeout = 4.5
    _headers = {'User-Agent': 'reapy/1.0'}

    class _Shaft:
        """
        An inner class, which covers CPU bound calculations. Asynchronous
        context requires CPU bound problems to be done in an executor,
        that's why :class:`concurrent.futures.ProcessPoolExecutor` is used
        in :class:`core.converters.Converter`. But multiprocessing classes
        use :mod:`pickles`, which causes problems with serialization. That's
        why converter can't pass its methods to the executor and why it
        requires extra object with synchronous methods.
        """
        def parse(self, location: Dict[str, Any]) -> Dict[str, Any]:
            """
            Performs JSON validation, then returns None if it failed and
            renovated dict otherwise.

            :param location: placement description (point, address, etc.)
            :return: None or location dictionary
            """
            return None if not self._check(location) else {
                'point': self._get_point(location),
                'state': self._get_state(location),
                'locality': self._get_locality(location),
                'county': self._get_county(location),
                'neighbourhood': self._get_neighbourhood(location),
                'road': self._get_road(location),
                'house_number': self._get_house_number(location)
            }

        def _check(self, location: Dict[str, Any]) -> bool:
            """
            Performs location's structure validating.

            :param location: geoposition's dictionary
            :return: whether location is valid or not
            """
            pass

        def _get_point(self, location: Dict[str, Any]) -> Tuple[float, float]:
            """
            Extracts 2D point from the "raw" JSON location

            :param location: geoposition's dictionary
            :return: 2D point in (longitude, latitude) format
            """
            pass

        def _get_state(self, location: Dict[str, Any]) -> str:
            """
            Extracts location's state (region, "oblast" or None in case of Kyiv)

            :param location: geoposition's dictionary
            :return: point's state
            """
            pass

        def _get_locality(self, location: Dict[str, Any]) -> str:
            """
            Extracts location's locality (city, town or village)

            :param location: geoposition's dictionary
            :return: point's locality
            """
            pass

        def _get_county(self, location: Dict[str, Any]) -> str:
            """
            Extracts location's county (district or "raion")

            :param location: geoposition's dictionary
            :return: point's administrative division unit
            """
            pass

        def _get_neighbourhood(self, location: Dict[str, Any]) -> str:
            """
            Extracts location's neighbourhood (suburb)

            :param location: geoposition's dictionary
            :return: point's historical area
            """
            pass

        def _get_road(self, location: Dict[str, Any]) -> str:
            """
            Extracts location's road (street, hwy, blw or ave)

            :param location: geoposition's dictionary
            :return: point's road
            """
            pass

        def _get_house_number(self, location: Dict[str, Any]) -> str:
            """
            Extracts location's house number

            :param location: geoposition's dictionary
            :return: point's house number
            """
            pass

    _shaft_class = _Shaft

    def __init__(self, crawler: Crawler, executor: Executor, scribbler: Scribbler):
        self._crawler = crawler
        self._executor = executor
        self._scribbler = scribbler
        self._semaphore = Semaphore(self._limit)
        self._loop = get_event_loop()
        self._shaft = self._shaft_class()

    async def locate(self, geodict: Dict[str, Any]) -> Dict[str, Any]:
        """
        Performs geoposition's fetching, validation and parsing.

        :param geodict: structure containing 'address' or 'point' values
        :return: geolocation's dict if the parsing succeeds and None otherwise
        """
        location = await self.__get_location(geodict)
        geolocation = await self._loop.run_in_executor(
            self._executor, self._shaft.parse, location
        )
        if geolocation is not None:
            return geolocation
        await self._scribbler.add('unlocated')

    async def __get_location(self, geodict: Dict[str, Any]) -> Dict[str, Any]:
        """
        Tries to parse the input geodict. Fulfills geocoding request if
        'point' value is present and reversing one otherwise.

        :param geodict: structure containing 'address' or 'point' values
        :return: location's dict
        """
        point = geodict.get('point')
        if point is None:
            json = await self.__get_json(
                self._geocoding_url.format(geodict.get('address'))
            )
            return None if json is None or len(json) == 0 else json[0]
        return await self.__get_json(
            self._reversing_url.format(point[1], point[0])
        )

    async def __get_json(self, url: str) -> Union[List, Dict]:
        """
        Performs JSON request with the geolocator's parameters.

        :param url: request URL
        :return: response's contents in JSON format
        """
        return await self._crawler.get_json(
            url, semaphore=self._semaphore,
            timeout=self._timeout, headers=self._headers
        )


class NominatimGeolocator(Geolocator):
    """
    "Geographic class" which leverages Nominatim API (based on OSM).
    'Cause *raions* concern Ukrainian real estate, all results of HTTP
    requests belongs to the Ukrainian territory.
    """
    _geocoding_url = 'https://nominatim.openstreetmap.org/search' \
                     '?format=json&q={}&addressdetails=1&limit=1'
    _reversing_url = 'https://nominatim.openstreetmap.org/reverse' \
                     '?format=json&lat={}&lon={}&addressdetails=1'

    class _Shaft(Geolocator._Shaft):
        """
        Nominatim's synchronous helper, specialized on the Ukrainian topology.

        Class properties:
            _county_pattern: RegExp for Ukrainian administrative division
            unit parsing and templating
        """
        _county_pattern = compile(r'([\w\-’\']+ район)\W*')

        def _check(self, location: Dict[str, Any]) -> bool:
            return (
                location is not None and
                location.get('address', {}).get('country') == 'Україна'
            )

        def _get_point(self, location: Dict[str, Any]) -> Tuple[float, float]:
            return float(location['lon']), float(location['lat'])

        def _get_state(self, location: Dict[str, Any]) -> str:
            state = location['address'].get('state')
            if state is not None and len(state) <= 30:
                return state

        def _get_locality(self, location: Dict[str, Any]) -> str:
            address = location['address']
            return next(filter(
                lambda l: not (
                    l is None or l.endswith(' рада') or l.endswith(' район')
                ),
                (address.get('city'), address.get('town'), address.get('village'))
            ), None)

        def _get_county(self, location: Dict[str, Any]) -> str:
            county = self.__search_county(location['address'].get('county'))
            if county is not None:
                return county
            return self.__search_county(location.get('display_name'))

        def __search_county(self, string: str) -> Optional[str]:
            """
            Tries to extract location's county from the address string.

            :param string: a row which contains city, district, suburb, etc.
            :return: location's county
            """
            try:
                county = self._county_pattern.search(string).groups()[0]
                if county[0].isupper():
                    return county
            except (AttributeError, TypeError):
                return None

        def _get_neighbourhood(self, location: Dict[str, Any]) -> str:
            address = location['address']
            return address.get('neighbourhood', address.get('suburb'))

        def _get_road(self, location: Dict[str, Any]) -> str:
            address = location['address']
            return address.get('road', address.get('pedestrian'))

        def _get_house_number(self, location: Dict[str, Any]) -> str:
            house_number = location['address'].get('house_number')
            if house_number is not None and len(house_number) <= 20:
                return house_number

    _shaft_class = _Shaft
