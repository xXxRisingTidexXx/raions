"""
This module describes main *reapy*'s workers - reapers

Reapers are in charge of data mining in general - they orchestrate all
low-level operations like scraping, DB connectivity, HTML parsing, etc.
Reapers leverage Clix API to imitate RX programming techniques.
"""
from typing import Dict, Any
from core.clixes import Clix
from core.decorators import measurable
from core.geomappers import NominatimGeomapper
from core.scribblers import ReaperScribbler
from core.repositories import FlatRepository
from core.workers import Worker
from core.converters import NBUConverter
from core.crawlers import OlxFlatCrawler, DomRiaFlatCrawler, EstateCrawler
from core.geolocators import NominatimGeolocator
from core.parsers import OlxFlatParser, DomRiaFlatParser
from core.rangers import OlxFlatRanger, DomRiaFlatRanger, Ranger
from core.utils import decimalize, notnull
from core.validators import FlatValidator, Validator


class Reaper(Worker):
    """
    Data mining's conductor, which joins separate components into united
    assembler. Generally, working stages look like this:
     - Ranging: initial pagination indices' sequence generation;
     - Page crawling: pagination pages' fetching;
     - Page parsing: pagination pages' HTML processing;
     - Offer crawling: offer pages' fetching;
     - Offer parsing: offer pages' HTML processing;
     - (Optional) Currency conversion: prices' conversion (into USD);
     - Validation: structs' numeric inspections;
     - Geocoding & reversing: objects' positioning;
     - Geomapping: GIS responses' processing;
     - Distinction: duplicates' deletion or updating;
     - Storing: resulting object's insertion to the DB;
    Reapers' data flow may change from instance to instance but generally
    stages' positions are stable and ordered.

    Class properties:
        _ranger_class: index segment generator's class
        _validator_class: numeric range checker's class

    Instance properties:
        _ranger: index segment generator
        _validator: numeric range checker
    """
    _scribbler_class = ReaperScribbler
    _ranger_class = Ranger
    _validator_class = Validator

    async def _prepare(self):
        await super()._prepare()
        self._ranger = self._ranger_class(self._crawler, self._parser)
        self._validator = self._validator_class()


class EstateReaper(Reaper):
    """
    Data collector which is aware of the main estate's feature
    - geolocation.

    Class properties:
        _geolocator_class: GIS API client class
        _geomapper_class: location json processing class

    Instance properties:
        _geolocator: GIS API client
        _geomapper: location json processor
    """
    _crawler_class = EstateCrawler
    _geolocator_class = NominatimGeolocator
    _geomapper_class = NominatimGeomapper

    async def _prepare(self):
        await super()._prepare()
        self._geolocator = self._geolocator_class(
            self._scribbler, self._crawler
        )
        self._geomapper = self._geomapper_class()

    @staticmethod
    def _get_url(offer: Dict[str, Any]) -> str:
        """
        Fetches offer's url.

        :param offer: target dict with 'markup', 'url' and some other fields
        :return: offer's url
        """
        return offer['url']

    @staticmethod
    def _filter_offer(offer: Any) -> bool:
        """
        Checks whether offer's markup is None or not.

        :param offer: target entity to be checked
        :return: is offer's markup None or not
        """
        return notnull(offer['markup'])

    @staticmethod
    def _set_rate(struct: Any) -> Any:
        """
        Configures estate's rate.

        :param struct: target entity to be configured
        :return: modified estate
        """
        struct.rate = decimalize(struct.price / decimalize(struct.area))
        return struct

    async def _set_geolocation(self, struct: Any) -> Any:
        """
        Configures estate's location dict.

        :param struct: target entity to be configured
        :return: modified estate
        """
        struct.geolocation = await self._geolocator.locate(struct.geolocation)
        return struct

    @staticmethod
    def _filter_geolocation(struct: Any) -> bool:
        """
        Checks whether estate's location is None or not.

        :param struct: target entity to be checked
        :return: is estate's geolocation None or not
        """
        return notnull(struct.geolocation)

    async def _map_geolocation(self, struct: Any) -> Any:
        """
        Processes estate's location dict.

        :param struct: target entity to be configured
        :return: modified estate with fully set location
        """
        struct.geolocation = self._geomapper.map(struct.geolocation)
        return struct


class OlxEstateReaper(EstateReaper):
    """
    Estate's data miner which is specialized on www.olx.ua estate.
    'Cause this resource allows different currencies, data flow
    requires currency conversion unit.

    Class properties:
        _converter_class: currency conversion entity's class

    Instance properties:
        _converter: currency conversion entity
    """
    _converter_class = NBUConverter

    async def _prepare(self):
        await super()._prepare()
        self._converter = self._converter_class(self._crawler)
        await self._converter.prepare()

    async def _set_price(self, struct: Any) -> Any:
        """
        Configures estate's price.

        :param struct: target entity to be configured
        :return: modified estate
        """
        struct.price = self._converter.convert_to_usd(
            struct.currency, struct.price
        )
        struct.currency = '$'
        return struct

    @staticmethod
    def _filter_price(struct: Any) -> Any:
        """
        Checks whether estate's price is None or not.

        :param struct: target entity to be checked
        :return: is estate's price None or not
        """
        return notnull(struct.price)

    @measurable('reap')
    async def _work(self):
        await (
            Clix(self._ranger.range)
            .reform(self._crawler.get_page)
            .map(self._parser.parse_page)
            .flatten()
            .distinct(self._get_url)
            .reform(self._crawler.get_offer, self._filter_offer)
            .sieve(self._parser.parse_offer)
            .reform(self._set_price, self._filter_price)
            .sieve(self._set_rate, self._validator.validate)
            .reform(self._repository.distinct)
            .reform(self._set_geolocation, self._filter_geolocation)
            .reform(self._map_geolocation, self._filter_geolocation)
            .apply(self._repository.create)
        )


class OlxFlatReaper(OlxEstateReaper):
    """
    Estate's data miner which is specialized on www.olx.ua
    flats' processing.
    """
    _ranger_class = OlxFlatRanger
    _crawler_class = OlxFlatCrawler
    _parser_class = OlxFlatParser
    _validator_class = FlatValidator
    _repository_class = FlatRepository


class DomRiaEstateReaper(EstateReaper):
    """
    Estate's data miner which is specialized on dom.ria.com estate.
    """
    @measurable('reap')
    async def _work(self):
        await (
            Clix(self._ranger.range)
            .reform(self._crawler.get_page)
            .map(self._parser.parse_page)
            .flatten()
            .distinct(self._get_url)
            .reform(self._crawler.get_offer, self._filter_offer)
            .sieve(self._parser.parse_offer)
            .sieve(self._set_rate, self._validator.validate)
            .reform(self._set_geolocation, self._filter_geolocation)
            .reform(self._map_geolocation, self._filter_geolocation)
            .reform(self._repository.distinct)
            .apply(self._repository.create)
        )


class DomRiaFlatReaper(DomRiaEstateReaper):
    """
    Estate's data miner which is specialized on dom.ria.com
    flats' processing.
    """
    _ranger_class = DomRiaFlatRanger
    _crawler_class = DomRiaFlatCrawler
    _parser_class = DomRiaFlatParser
    _validator_class = FlatValidator
    _repository_class = FlatRepository
