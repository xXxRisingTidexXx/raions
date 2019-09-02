"""
This module describes a bunch of "geographic" classes

One of the most important step of the data flow is position determination.
Objects are situated all over the territory and the service has to know
their coordinates. The classes below use the public API to carry out
geocoding & reversing.
"""
from asyncio import Semaphore
from typing import Dict, Any, Union, List, Tuple
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

    Instance properties:
        _scribbler: statistics entity which writes success & failure shapes
        _crawler: asynchronous HTTP client
        _semaphore: HTTP connection "restriction frame"
    """
    _geocoding_url = None
    _reversing_url = None
    _limit = 1
    _timeout = 4.5
    _headers = {'User-Agent': 'reapy/1.0'}

    def __init__(self, scribbler: Scribbler, crawler: Crawler):
        self._scribbler = scribbler
        self._crawler = crawler
        self._semaphore = Semaphore(self._limit)

    async def locate(self, geodict: Dict[str, Any]) -> Dict[str, Any]:
        point, address = geodict.get('point'), geodict.get('address')
        location = await (
            self._geocode(address) if point is None else self._reverse(point)
        )
        if location is None:
            await self._scribbler.add('unlocated')
        return location

    async def _geocode(self, address: str) -> Dict[str, Any]:
        pass

    async def _reverse(self, point: Tuple[float, float]) -> Dict[str, Any]:
        pass

    async def _get_json(self, url: str) -> Union[List[Any], Dict[str, Any]]:
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
    """
    _geocoding_url = 'https://nominatim.openstreetmap.org/search' \
                     '?format=json&q={}&addressdetails=1&limit=1'
    _reversing_url = 'https://nominatim.openstreetmap.org/reverse' \
                     '?format=json&lat={}&lon={}&addressdetails=1'

    async def _geocode(self, address: str) -> Dict[str, Any]:
        json = await self._get_json(self._geocoding_url.format(address))
        return None if json is None or len(json) == 0 else json[0]

    async def _reverse(self, point: Tuple[float, float]) -> Dict[str, Any]:
        return await self._get_json(
            self._reversing_url.format(point[1], point[0])
        )
