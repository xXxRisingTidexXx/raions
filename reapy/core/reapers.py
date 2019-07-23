from asyncio import gather
from .scribblers import ReaperScribbler
from .repositories import FlatRepository
from .workers import Worker
from .converters import NBUConverter
from .crawlers import OlxFlatCrawler, DomRiaFlatCrawler
from .decorators import measurable
from .geolocators import NominatimGeolocator
from .parsers import OlxFlatParser, DomRiaFlatParser
from .rangers import OlxFlatRanger, DomRiaFlatRanger, Ranger
from .utils import decimalize, map_filter
from .validators import Validator, FlatValidator


class Reaper(Worker):
    _scribbler_class = ReaperScribbler
    _validator_class = Validator
    _ranger_class = Ranger

    async def _prepare(self, pool, session, executor):
        await super()._prepare(pool, session, executor)
        self._validator = self._validator_class(executor, self._scribbler)
        self._ranger = self._ranger_class(self._crawler, self._parser)


    @measurable('reap')
    async def _work(self):
        await self._repository.create_all(
            await self._sift_all(
                await self._parser.parse_offers(
                    await self._crawler.get_offers(
                        await self._parser.parse_pages(
                            await self._crawler.get_pages(
                                await self._ranger.range()
                            )
                        )
                    )
                )
            )
        )

    async def _sift_all(self, structs):
        pass


class EstateReaper(Reaper):
    _converter_class = NBUConverter
    _geolocator_class = NominatimGeolocator

    async def _prepare(self, pool, session, executor):
        await super()._prepare(pool, session, executor)
        self._converter = self._converter_class(self._crawler, executor)
        await self._converter.prepare()
        self._geolocator = self._geolocator_class(
            self._crawler, executor, self._scribbler
        )

    @measurable('conversion')
    async def _convert_all(self, structs):
        return await gather(*map(self.__convert, structs))

    async def __convert(self, struct):
        struct.price = await self._converter.convert_to_usd(
            struct.currency, struct.price
        )
        if struct.price is not None:
            struct.rate = decimalize(struct.price / decimalize(struct.area))
            struct.currency = '$'
            return struct

    @measurable('location')
    async def _locate_all(self, structs):
        return await map_filter(
            structs, self.__locate, lambda s: s.geolocation is not None
        )

    async def __locate(self, struct):
        struct.geolocation = await self._geolocator.locate(struct.geolocation)
        return struct


class OlxEstateReaper(EstateReaper):
    async def _sift_all(self, structs):
        return await self._locate_all(
            await self._repository.distinct_all(
                await self._validator.validate_all(
                    await self._convert_all(structs)
                )
            )
        )


class OlxFlatReaper(OlxEstateReaper):
    _repository_class = FlatRepository
    _crawler_class = OlxFlatCrawler
    _parser_class = OlxFlatParser
    _ranger_class = OlxFlatRanger
    _validator_class = FlatValidator
    _max_pool_size = 40


class DomRiaEstateReaper(EstateReaper):
    async def _sift_all(self, structs):
        return await self._repository.distinct_all(
            await self._locate_all(
                await self._validator.validate_all(
                    await self._convert_all(structs)
                )
            )
        )


class DomRiaFlatReaper(DomRiaEstateReaper):
    _repository_class = FlatRepository
    _crawler_class = DomRiaFlatCrawler
    _parser_class = DomRiaFlatParser
    _ranger_class = DomRiaFlatRanger
    _validator_class = FlatValidator
    _max_pool_size = 50
