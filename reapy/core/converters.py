"""
This module contains a set of currency converters

Each offer in the data flow has a price, but many web-resources publish offers
without automatic recalculation. Classes below carry out currency conversion,
based on public APIs.
"""
from datetime import date
from decimal import Decimal
from typing import Dict, Tuple
from core.crawlers import Crawler
from core.utils import decimalize


class Converter:
    """
    Basic asynchronous currency calculator. It leverages an HTTP client
    to perform currency rates' requests and an executor to fulfil CPU bound
    calculations. If a currency pairs' request fails and conversion is
    obligatory, converter returns nothing.

    Class properties:
        _rates_url: public rates' API url
        _symbols: complete dictionary of the currency chars
        _shaft_class: an inner class, which wraps all
        synchronous calculations (to be able to call them in the executor)

    Instance properties:
        _crawler: asynchronous HTTP client
        _executor: CPU bound problems' calculator
        _loop: asyncio event loop
        _pairs: currency pairs' ratios
        _shaft: synchronous functions' wrapper
    """
    _rates_url = None
    _symbols = {
        'грн.': 'UAH', '$': 'USD', '€': 'EUR',
        'USD': 'USD', 'UAH': 'UAH', 'EUR': 'EUR'
    }

    def __init__(self, crawler: Crawler):
        self._crawler = crawler
        self._pairs = None

    async def prepare(self):
        """
        Sets the currency pairs, fetching the rates via HTTP request.
        """
        self._pairs = await self._calc_pairs()

    async def _calc_pairs(self) -> Dict[Tuple, Decimal]:
        """
        Fetches the rates' JSON from the public API and calculates
        the resulting currency pairs.

        :return: currency ratios
        """
        pass

    def convert_to_usd(self, fr: str, amount: Decimal) -> Decimal:
        """
        Converts the input money sum into USD.

        :param fr: input currency
        :param amount: money sum
        :return: money sum in USD
        """
        return self.convert(fr, 'USD', amount)

    def convert(self, fr: str, to: str, amount: Decimal) -> Decimal:
        """
        Converts the input money sum into another currency.

        :param fr: input currency
        :param to: output currency
        :param amount: money sum
        :return: mapped money sum
        """
        fr, to = self._symbols[fr], self._symbols[to]
        if fr == to:
            return amount
        pair = self._pairs.get((fr, to))
        return decimalize(pair * amount) if pair is not None else None


class NBUConverter(Converter):
    """
    Currency converter based on the National Bank of Ukraine public API.
    """
    _rates_url = 'https://bank.gov.ua/NBUStatService/v1/' \
                 'statdirectory/exchange?date={}&json'

    async def _calc_pairs(self) -> Dict[Tuple, Decimal]:
        today = date.today()
        rates = await self._crawler.get_json(self._rates_url.format(
            f'{today.year}{self.__str(today.month)}{self.__str(today.day)}'
        ))
        if rates is None:
            return {}
        shapes = {r['cc']: r['rate'] for r in rates}
        return {
            ('UAH', 'USD'): decimalize(1 / shapes['USD']),
            ('EUR', 'USD'): decimalize(shapes['EUR'] / shapes['USD'])
        }

    @staticmethod
    def __str(i: int) -> str:
        """
        Expands the integer to two digits.

        :param i: int to be expanded
        :return: string number which takes 2 digits
        """
        return f'0{i}' if i < 10 else str(i)
