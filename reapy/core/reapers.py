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
    _scribbler_class = ReaperScribbler
    _ranger_class = Ranger
    _validator_class = Validator

    async def _prepare(self):
        await super()._prepare()
        self._ranger = self._ranger_class(self._crawler, self._parser)
        self._validator = self._validator_class()


class EstateReaper(Reaper):
    _crawler_class = EstateCrawler
    _geolocator_class = NominatimGeolocator
    _geomapper_class = NominatimGeomapper

    async def _prepare(self):
        await super()._prepare()
        self._geolocator = self._geolocator_class(self._scribbler, self._crawler)
        self._geomapper = self._geomapper_class()

    @staticmethod
    def _get_url(offer: Dict[str, Any]) -> str:
        return offer['url']

    @staticmethod
    def _filter_offer(offer: Any) -> bool:
        return notnull(offer['markup'])

    async def _set_geolocation(self, struct: Any) -> Any:
        struct.geolocation = await self._geolocator.locate(struct.geolocation)
        return struct

    @staticmethod
    def _filter_geolocation(struct: Any) -> bool:
        return notnull(struct.geolocation)

    def _map_geolocation(self, struct: Any) -> Any:
        struct.geolocation = self._geomapper.map(struct.geolocation)
        return struct


class OlxEstateReaper(EstateReaper):
    _converter_class = NBUConverter

    async def _prepare(self):
        await super()._prepare()
        self._converter = self._converter_class(self._crawler)
        await self._converter.prepare()

    def _set_shapes(self, struct: Any) -> Any:
        struct.price = self._converter.convert_to_usd(
            struct.currency, struct.price
        )
        if struct.price is not None:
            struct.rate = decimalize(struct.price / decimalize(struct.area))
            struct.currency = '$'
            return struct

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
            .sieve(self._set_shapes, self._validator.validate)
            .reform(self._repository.distinct)
            .reform(self._set_geolocation, self._filter_geolocation)
            .reform(self._map_geolocation, self._filter_geolocation)
            .apply(self._repository.create)
        )


class OlxFlatReaper(OlxEstateReaper):
    _ranger_class = OlxFlatRanger
    _crawler_class = OlxFlatCrawler
    _parser_class = OlxFlatParser
    _validator_class = FlatValidator
    _repository_class = FlatRepository


class DomRiaEstateReaper(EstateReaper):
    @measurable('reap')
    async def _work(self):
        await (
            Clix(self._ranger.range)
            .reform(self._crawler.get_page)
            .map(self._parser.parse_page)
            .flatten()
            .distinct(self._get_url)
            .reform(self._crawler.get_offer, self._filter_offer)
            .sieve(self._parser.parse_offer, self._validator.validate)
            .reform(self._set_geolocation, self._filter_geolocation)
            .reform(self._map_geolocation, self._filter_geolocation)
            .reform(self._repository.distinct)
            .apply(self._repository.create)
        )


class DomRiaFlatReaper(DomRiaEstateReaper):
    _ranger_class = DomRiaFlatRanger
    _crawler_class = DomRiaFlatCrawler
    _parser_class = DomRiaFlatParser
    _validator_class = FlatValidator
    _repository_class = FlatRepository
