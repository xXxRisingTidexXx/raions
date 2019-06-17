from asyncio import get_event_loop
from datetime import date
from json import loads, dumps
from .utils import exist, load, dump, decimalize, makedir


class Converter:
    _rates_url = None
    _rates_path = None
    _symbols = {
        'грн.': 'UAH', '$': 'USD', '€': 'EUR',
        'USD': 'USD', 'UAH': 'UAH', 'EUR': 'EUR'
    }

    class _Shaft:
        def calc_pairs(self, rates):
            pass

        @staticmethod
        def convert(fr, to, amount, pairs):
            return decimalize(pairs[(fr, to)] * amount)

    _shaft_class = _Shaft

    def __init__(self, crawler, executor):
        self._shaft = self._shaft_class()
        self._crawler = crawler
        self._executor = executor
        self._loop = get_event_loop()
        self._pairs = None

    async def prepare(self):
        rates = None
        if exist(self._rates_path):
            rates = loads(await load(self._rates_path))
        if not self._check(rates):
            try:
                rates = await self._get_rates()
                await dump(self._rates_path, dumps(rates))
            except TypeError:
                raise RuntimeError('no rates were got')
        self._pairs = await self._loop.run_in_executor(
            self._executor, self._shaft.calc_pairs, rates
        )

    def _check(self, rates):
        pass

    async def _get_rates(self):
        pass

    async def convert_to_usd(self, fr, amount):
        return await self.convert(fr, 'USD', amount)

    async def convert(self, fr, to, amount):
        fr, to = self._symbols[fr], self._symbols[to]
        return amount if fr == to else await self._loop.run_in_executor(
            self._executor, self._shaft.convert, fr, to, amount, self._pairs
        )


class NBUConverter(Converter):
    _rates_url = 'https://bank.gov.ua/NBUStatService/v1' \
                 '/statdirectory/exchange?date={}&json'
    _rates_path = 'resources/nbu/rates.json'

    class _Shaft(Converter._Shaft):
        def calc_pairs(self, rates):
            pairs = {r['cc']: r['rate'] for r in rates}
            return {
                ('UAH', 'USD'): decimalize(1 / pairs['USD']),
                ('EUR', 'USD'): decimalize(pairs['EUR'] / pairs['USD'])
            }

    _shaft_class = _Shaft

    async def prepare(self):
        makedir('resources/nbu')
        await super().prepare()

    def _check(self, rates):
        today = date.today()
        return (
            rates is not None and rates[0]['exchangedate'] ==
            f'{self.__str(today.day)}.{self.__str(today.month)}.{today.year}'
        )

    @staticmethod
    def __str(i):
        return f'0{i}' if i < 10 else str(i)

    async def _get_rates(self):
        today = date.today()
        url = self._rates_url.format(
            f'{today.year}{self.__str(today.month)}{self.__str(today.day)}'
        )
        return [
            r for r in await self._crawler.get_json(url)
            if r['cc'] in self._symbols
        ]
