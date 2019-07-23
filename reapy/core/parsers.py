import logging
from asyncio import get_event_loop, gather
from datetime import date, datetime
from functools import reduce
from math import ceil, log10
from re import compile
from bs4 import BeautifulSoup
from bs4.element import SoupStrainer
from json import loads
from .decorators import measurable
from .structs import Flat
from .utils import decimalize, json, map_filter


class Parser:
    class _Shaft:
        _builder = 'lxml'
        _offer_strainer = None

        def parse_stop(self, markup):
            try:
                return self._parse_stop(BeautifulSoup(markup, self._builder))
            except (IndexError, AttributeError, ValueError, TypeError):
                logging.exception('stop parsing failed')

        def _parse_stop(self, soup):
            pass

        @staticmethod
        def flat_map_pages(offers_lists):
            return list(
                {o['url']: o for ol in offers_lists for o in ol}.values()
            )

        def parse_page(self, page):
            try:
                return self._parse_page(BeautifulSoup(
                    page, self._builder, parse_only=self._offer_strainer
                ))
            except AttributeError:
                logging.exception('page parsing failed')
                return []

        def _parse_page(self, soup):
            pass

        # noinspection PyBroadException
        def parse_offer(self, offer):
            url = offer.pop('url')
            try:
                soup = BeautifulSoup(offer.pop('markup'), self._builder)
                if self._check_offer(soup):
                    return self._parse_offer(url, soup, **offer)
            except Exception:
                logging.exception(f'{url} parsing failed')

        def _check_offer(self, soup):
            pass

        def _parse_offer(self, url, soup, **kwargs):
            pass

        def parse_junk(self, junk):
            try:
                return self._parse_junk(
                    junk['url'], BeautifulSoup(junk['markup'], self._builder)
                )
            except TypeError:
                logging.exception(f'{junk["url"]} parsing failed')

        def _parse_junk(self, url, soup):
            pass

    _shaft_class = _Shaft

    def __init__(self, executor, scribbler):
        self._executor = executor
        self._scribbler = scribbler
        self._loop = get_event_loop()
        self._shaft = self._shaft_class()

    async def parse_stop(self, markup):
        return await self.__parse('parse_stop', markup)

    async def __parse(self, method, *args):
        return await self._loop.run_in_executor(
            self._executor, getattr(self._shaft, method), *args
        )

    @measurable('page parsing')
    async def parse_pages(self, pages):
        return await self._loop.run_in_executor(
            self._executor, self._shaft.flat_map_pages,
            await gather(*map(self.__parse_page, pages))
        )

    async def __parse_page(self, page):
        return await self.__parse('parse_page', page)

    @measurable('offer parsing')
    async def parse_offers(self, offers):
        return await map_filter(offers, self.__parse_offer)

    async def __parse_offer(self, offer):
        struct = await self.__parse('parse_offer', offer)
        if struct is not None:
            return struct
        await self._scribbler.add('unparsed')

    async def parse_junks(self, junks):
        return set(await map_filter(junks, self.__parse_junk))

    async def __parse_junk(self, junk):
        return await self.__parse('parse_junk', junk)


class EstateParser(Parser):
    class _Shaft(Parser._Shaft):
        _float_pattern = compile(r'^\s*([\d.]+)')
        _int_pattern = compile(r'^\s*(\d+)')
        _details = None

        def _float(self, f):
            try:
                return float(
                    self._float_pattern.search(f.replace(' ', '')).groups()[0]
                )
            except (AttributeError, TypeError):
                pass

        def _int(self, i):
            try:
                return int(self._int_pattern.search(i).groups()[0])
            except (AttributeError, TypeError):
                pass

        def _parse_details(self, pairs):
            return [
                self._details[p[0]][p[1]]
                for p in pairs.items()
                if p[0] in self._details
            ]

    _shaft_class = _Shaft


class OlxEstateParser(EstateParser):
    class _Shaft(EstateParser._Shaft):
        _offer_strainer = SoupStrainer('a')
        _url_pattern = compile(r'^(\S+\.html)')
        _published_pattern = compile(r'(\d{1,2}) (\w+) (\d{4})')
        _months = {
            'января': 1, 'февраля': 2, 'марта': 3, 'апреля': 4,
            'мая': 5, 'июня': 6, 'июля': 7, 'августа': 8,
            'сентября': 9, 'октября': 10, 'ноября': 11, 'декабря': 12
        }
        _shapes_pattern = compile(r'^([ .\d]+) (\D+)$')

        def _parse_stop(self, soup):
            tags = soup.find_all('a', 'brc8')
            if len(tags) > 0:
                return int(tags[-1].findChild().text)

        def _parse_page(self, soup):
            return [
                {'url': self._url_pattern.search(t['href']).groups()[0]}
                for t in soup.find_all('a', 'thumb')
            ]

        def _check_offer(self, soup):
            return (
                self.__find_junk(soup) is None and
                self.__find_published(soup) is not None and
                self.__find_point(soup) is not None and
                self.__find_price(soup) is not None
            )

        @staticmethod
        def __find_junk(soup):
            return soup.find('h3', 'lheight20 large cfff')

        @staticmethod
        def __find_published(soup):
            return soup.find('span', 'pdingleft10')

        @staticmethod
        def __find_point(soup):
            return soup.find(id='mapcontainer')

        @staticmethod
        def __find_price(soup):
            tag = soup.find('strong', 'xxxx-large')
            return (
                tag if tag is not None
                else soup.find_all('strong', 'xx-large')[1]
            )

        @staticmethod
        def _parse_avatar(soup):
            tag = soup.find('img', 'vtop')
            if tag is not None:
                return tag['src']

        def _parse_published(self, soup):
            pub = self._published_pattern.search(
                self.__find_published(soup).text
            ).groups()
            return date(
                int(pub[2]), self._months.get(pub[1], 1), int(pub[0])
            )

        def _parse_geolocation(self, soup):
            tag = self.__find_point(soup)
            return {'point': (float(tag['data-lon']), float(tag['data-lat']))}

        def _parse_shapes(self, soup):
            shapes = self._shapes_pattern.match(
                self.__find_price(soup).text
            ).groups()
            return {
                'price': decimalize(shapes[0].replace(' ', '')),
                'currency': shapes[1]
            }

        @staticmethod
        def _parse_pairs(soup):
            return {
                t.find('th').text: t.find('strong').text.strip('\t\n')
                for t in soup.find_all('table', 'item')
            }

        def _parse_junk(self, url, soup):
            if self.__find_junk(soup) is not None:
                return url

    _shaft_class = _Shaft


class OlxFlatParser(OlxEstateParser):
    class _Shaft(OlxEstateParser._Shaft):
        _details = json('resources/olx_flat_reaper/details.json')

        def _parse_offer(self, url, soup, **kwargs):
            shapes = self._parse_shapes(soup)
            pairs = self._parse_pairs(soup)
            params = self.__parse_parameters(pairs)
            return Flat(
                url=url,
                avatar=self._parse_avatar(soup),
                published=self._parse_published(soup),
                geolocation=self._parse_geolocation(soup),
                price=shapes['price'],
                currency=shapes['currency'],
                area=params['area'],
                kitchen_area=params['kitchen_area'],
                rooms=params['rooms'],
                floor=params['floor'],
                total_floor=params['total_floor'],
                details=self._parse_details(pairs)
            )

        def __parse_parameters(self, pairs):
            return {
                'area': self._float(pairs.get('Общая площадь')),
                'kitchen_area': self._float(pairs.get('Площадь кухни')),
                'rooms': self._int(pairs.get('Количество комнат')),
                'floor': self._int(pairs.get('Этаж')),
                'total_floor': self._int(pairs.get('Этажность')),
            }

    _shaft_class = _Shaft


class DomRiaEstateParser(EstateParser):
    class _Shaft(EstateParser._Shaft):
        _published_pattern = compile(r'(\d{2}) (\w{3})( \d{4})?')
        _months = {
            'січ': 1, 'янв': 1, 'лют': 2, 'фев': 2, 'бер': 3, 'мар': 3,
            'кві': 4, 'апр': 4, 'тра': 5, 'май': 5, 'чер': 6, 'июн': 6,
            'лип': 7, 'июл': 7, 'сер': 8, 'авг': 8, 'вер': 9, 'сен': 9,
            'жов': 10, 'окт': 10, 'лис': 11, 'ноя': 11, 'гру': 12, 'дек': 12
        }
        _json_pattern = compile(r'STATE__=(.+);\(function')
        _impurities = (
            ' ул.', ' просп.', ' пер.', ' буд.', ' бул.', ' вул.'
        )

        def _parse_stop(self, soup):
            return int(
                soup.find_all('a', 'page-link')[4].text.replace(' ', '')
            )

        def _check_offer(self, soup):
            return (
                self.__find_junk(soup) is None and
                self.__find_description(soup) is not None and
                'Дог' not in self.__find_price(soup)
            )

        @staticmethod
        def __find_junk(soup):
            return soup.find('div', 'warning middle')

        @staticmethod
        def __find_description(soup):
            return soup.find('div', id='description')

        @staticmethod
        def __find_price(soup):
            return soup.find('span', 'price').text

        @staticmethod
        def _parse_avatar(soup, avatar):
            tag = soup.find('picture', 'outline')
            return tag.find('img')['src'] if tag is not None else avatar

        def _parse_published(self, soup):
            pub = self._published_pattern.search(
                soup.find('li', 'mt-15').find('b').text
            ).groups()
            return date(
                datetime.today().year if pub[2] is None else int(pub[2]),
                self._months[pub[1]],
                self._int(pub[0] if pub[0][0] != '0' else pub[0][1])
            )

        def _parse_geolocation(self, soup):
            data = loads(self._json_pattern.search(next(filter(
                lambda t: t.text.startswith('window'),
                soup.find_all('script')
            )).text).groups()[0])['dataForFinalPage']['realty']
            try:
                return {
                    'point': (
                        float(data['longitude']), float(data['latitude'])
                    )
                }
            except (KeyError, ValueError):
                return {'address': self._parse_address(data)}

        def _parse_address(self, data):
            return ', '.join((
                data.get('city_name_uk', data.get('city_name', '')),
                data.get('district_name_uk', data.get('district_name', '')),
                reduce(
                    lambda s, i: s.replace(i, ''), self._impurities,
                    data.get('street_name_uk', data.get('street_name', ''))
                )
            ))

        def _parse_price(self, soup):
            return decimalize(
                self.__find_price(soup).replace(' ', '').replace('$', '')
            )

        def _parse_pairs(self, soup):
            return {
                **self.__parse_description(soup),
                **self.__parse_additional(soup)
            }

        def __parse_description(self, soup):
            return {
                t.find('div', 'label').text.strip():
                    t.find('div', 'indent').text.strip()
                for t in self.__find_description(soup).find_all(
                    'ul', 'unstyle'
                )[1].find_all('li', 'mt-15')
            }

        @staticmethod
        def __parse_additional(soup):
            additional = soup.find('ul', id='additionalInfo')
            return {} if additional is None else {
                p[0]: p[1]
                for t in additional.find_all('li', 'mt-20')
                for p in (
                    p.split(': ')
                    for p in t.find('div', 'boxed').text.strip().split(' • ')
                    if ':' in p
                )
            }

        def _parse_junk(self, url, soup):
            if self.__find_junk(soup) is not None:
                return url

    _shaft_class = _Shaft


class DomRiaFlatParser(DomRiaEstateParser):
    class _Shaft(DomRiaEstateParser._Shaft):
        _offer_strainer = SoupStrainer('section')
        _details = json('resources/dom_ria_flat_reaper/details.json')
        __area_pattern = compile(r'Площа (\S+)/(\S+)/(\S+)')

        def _parse_page(self, soup):
            return list(filter(
                lambda o: o is not None, map(
                    self.__parse_section,
                    soup.find_all('section', 'ticket-clear')
                )
            ))

        def __parse_section(self, tag):
            url = tag.find('a', 'blue')['href']
            if url.startswith('/uk/'):
                avatar = tag.find('span', 'load-photo').find('img')
                areas = self.__area_pattern.search(next((
                    t.text for t in tag.find_all('li', 'mt-5 i-block')
                    if t.get('title', '').startswith('Площа:')
                ))).groups()
                return {
                    'url': f'https://dom.ria.com{url}',
                    'avatar': avatar.get('src', avatar.get('data-src')),
                    'area': self._float(areas[0]),
                    'living_area': self._float(areas[1]),
                    'kitchen_area': self._float(areas[2])
                }

        def _parse_offer(self, url, soup, **kwargs):
            pairs = self._parse_pairs(soup)
            params = self.__parse_parameters(pairs)
            return Flat(
                url=url,
                avatar=self._parse_avatar(soup, kwargs['avatar']),
                published=self._parse_published(soup),
                geolocation=self._parse_geolocation(soup),
                price=self._parse_price(soup),
                area=kwargs['area'],
                living_area=kwargs['living_area'],
                kitchen_area=kwargs['kitchen_area'],
                rooms=params['rooms'],
                floor=params['floor'],
                total_floor=params['total_floor'],
                ceiling_height=params['ceiling_height'],
                details=self._parse_details(pairs)
            )

        def _parse_pairs(self, soup):
            pairs = super()._parse_pairs(soup)
            pairs['Тип'] = next(filter(
                lambda t: t.endswith(' житло'),
                map(
                    lambda t: t.text.strip(),
                    soup.find_all('li', 'labelHot')
                )
            ), None)
            return pairs

        def __parse_parameters(self, pairs):
            return {
                'rooms': self._int(pairs.get('Кімнат')),
                'floor': self._int(pairs.get('Поверх')),
                'total_floor': self._int(pairs.get('Поверховість')),
                'ceiling_height': self._ceiling_height(
                    pairs.get('висота стелі')
                )
            }

        def _ceiling_height(self, ch):
            ch = self._float(ch)
            if ch is not None:
                return ch * 10 ** ceil(-log10(ch))

    _shaft_class = _Shaft
