"""
This module describes the most essential part
of the whole data flow - HTML parsing

Parsers use BeautifulSoup4 in order to extract the target values and
build sophisticated data structures. They encapsulate the logic of
HTML processing in the current class hierarchy, that's why all parsers
are very portable and reusable.
"""
from datetime import date, datetime
from decimal import Decimal
from functools import reduce
from math import ceil, log10
from re import compile
from typing import Optional, List, Dict, Any, Tuple, Union
from bs4 import BeautifulSoup
from bs4.element import SoupStrainer, Tag
from json import loads
from core.decorators import nullable
from core.structs import Flat
from core.utils import decimalize, json
from logging import getLogger

logger = getLogger(__name__)


class Parser:
    """
    The most general parser, which supplies facade methods with graceful
    error handling when the descendants are concerned about business logic.
    Generally, the whole process of parsing is a simple search across the
    DOM, appropriate type conversion and building of a resulting struct.

    Class properties:
        _builder: default DOM nodes' processor
        _offer_strainer: if provided, restricts tags' amount
        during the page parsing
    """
    _builder = 'lxml'
    _offer_strainer = None

    def parse_stop(self, markup: str) -> Optional[int]:
        """
        Tries to process the target HTML and supply the last pagination index.

        :param markup: HTML contents
        :return: last paging index or None
        """
        try:
            return self._parse_stop(BeautifulSoup(markup, self._builder))
        except (IndexError, AttributeError, ValueError, TypeError):
            logger.exception('stop parsing failed')

    def _parse_stop(self, soup: BeautifulSoup) -> Optional[int]:
        """
        Tries to process the target HTML and supply the last pagination
        index (except exception handling and data preparation).

        :param soup: DOM tags' tree
        :return: last paging index or None
        """
        pass

    def parse_page(self, markup: str) -> List[Dict[str, Any]]:
        """
        Processes the target page and provides a list of
        "raw offers" (offer page's dicts without 'markup' field).

        :param markup: HTML contents
        :return: list of "raw offers"
        """
        try:
            return self._parse_page(BeautifulSoup(
                markup, self._builder, parse_only=self._offer_strainer
            ))
        except AttributeError:
            logger.exception('page parsing failed')
            return []

    def _parse_page(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """
        Processes the target page and provides a list of "raw offers"
        (offer page's dicts without 'markup' field), but excludes error
        handling and markup preparation.

        :param soup: DOM tags' tree
        :return: list of "raw offers"
        """
        pass

    def parse_offer(self, offer: Dict[str, Any]) -> Optional[Any]:
        """
        Checks and parsers the target offer, providing succinct
        digital description. Mainly, the result includes such values
        as price, rate, location, etc.

        :param offer: target dict with 'markup', 'url' and some other fields
        :return: special data structure or None if the check failed
        """
        url = offer.pop('url')
        try:
            soup = BeautifulSoup(offer.pop('markup'), self._builder)
            if self._check_offer(soup):
                return self._parse_offer(url, soup, **offer)
        except (LookupError, AttributeError, ValueError, TypeError):
            logger.exception(f'{url} parsing failed')

    def _check_offer(self, soup: BeautifulSoup) -> bool:
        """
        Validates the target page if it deserves to be parsed.

        :param soup: DOM tags' tree
        :return: is target page valid or not
        """
        pass

    def _parse_offer(
        self, url: str, soup: BeautifulSoup, **kwargs: Any
    ) -> Any:
        """
        Processes the target offer's dict and builds the final
        struct (after the page validation).

        :param url: offer page's url
        :param soup: DOM tags' tree
        :param kwargs: additional offer's parameters
        :return: short offer's view
        """
        pass

    def parse_junk(self, offer: Dict[str, Any]) -> Optional[str]:
        """
        Processes the target offer and decides whether it's obsolete or not.

        :param offer: target page's view
        :return: offer's url if the page isn't obsolete and None otherwise
        """
        try:
            return self._parse_junk(
                offer['url'], BeautifulSoup(offer['markup'], self._builder)
            )
        except TypeError:
            logger.exception(f'{offer["url"]} parsing failed')

    def _parse_junk(self, url: str, soup: BeautifulSoup) -> Optional[str]:
        """
        Processes the target offer and decides whether it's obsolete or not.

        :param url: offer's url
        :param soup: DOM tags' tree
        :return: offer's url if the page isn't obsolete and None otherwise
        """
        pass


class EstateParser(Parser):
    """
    Special parser's version, suitable for the real estate offers' processing.
    It's capable of simple numeric conversion and offer details' fetching.

    Class properties:
        _float_pattern: real number regex pattern
        _int_pattern: integer number regex pattern
        _details: dict of the details' pairs, needed for localization
        (from UK/RU into EN)
    """
    _float_pattern = compile(r'^\s*([\d.]+)')
    _int_pattern = compile(r'^\s*(\d+)')
    _details = None

    @nullable
    def _float(self, string: str) -> Optional[float]:
        """
        Extracts real number from the string.

        :param string: target char array
        :return: real number or None if the parsing failed
        """
        return float(
            self._float_pattern.search(string.replace(' ', '')).groups()[0]
        )

    @nullable
    def _int(self, string: str) -> Optional[int]:
        """
        Extracts integer number from the string.

        :param string: target char array
        :return: integer number or None if the parsing failed
        """
        return int(self._int_pattern.search(string).groups()[0])

    def _parse_details(self, pairs: Dict[str, str]) -> List[str]:
        """
        Main offer's data is contained by tables, so it's quite easy
        to transform it into key-value pairs and filter the needed
        attributes. This function compares pairs concernedly detail
        localization dicts.

        :param pairs: a map of the offer's features
        :return: offer detail's list
        """
        return [
            self._details[p[0]][p[1]]
            for p in pairs.items()
            if p[0] in self._details
        ]


class OlxEstateParser(EstateParser):
    """
    Deep parser's evolution, specialized on www.olx.ua offers' processing.

    Class properties:
        _url_pattern: truncates the url string removing trailing hash
        _published_pattern: publication date regex pattern
        _months: matches between literal and numeric months
        _shapes_pattern: regex pattern with offer's price and currency
    """
    _offer_strainer = SoupStrainer('a')
    _url_pattern = compile(r'^(\S+\.html)')
    _published_pattern = compile(r'(\d{1,2}) (\w+) (\d{4})')
    _months = {
        'января': 1, 'февраля': 2, 'марта': 3, 'апреля': 4,
        'мая': 5, 'июня': 6, 'июля': 7, 'августа': 8,
        'сентября': 9, 'октября': 10, 'ноября': 11, 'декабря': 12
    }
    _shapes_pattern = compile(r'^([ .\d]+) (\D+)$')

    def _parse_stop(self, soup: BeautifulSoup) -> Optional[int]:
        tags = soup.find_all('a', 'brc8')
        if len(tags) > 0:
            return int(tags[-1].findChild().text)

    def _parse_page(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        return [
            {'url': self._url_pattern.search(t['href']).groups()[0]}
            for t in soup.find_all('a', 'thumb')
        ]

    def _check_offer(self, soup: BeautifulSoup) -> bool:
        return (
            self.__find_junk(soup) is None and
            self.__find_published(soup) is not None and
            self.__find_point(soup) is not None and
            self.__find_price(soup) is not None
        )

    @staticmethod
    def __find_junk(soup: BeautifulSoup) -> Optional[Tag]:
        """
        Detects the tag which indicates the offer's obsolescence.

        :param soup: DOM tags' tree
        :return: target tag
        """
        return soup.find('h3', 'lheight20 large cfff')

    @staticmethod
    def __find_published(soup: BeautifulSoup) -> Optional[Tag]:
        """
        Detects the tag which contains offer's publication date.

        :param soup: DOM tags' tree
        :return: tag with publication date
        """
        return soup.find('span', 'pdingleft10')

    @staticmethod
    def __find_point(soup: BeautifulSoup) -> Optional[Tag]:
        """
        Finds tag with estate's longitude & latitude.

        :param soup: DOM tags' tree
        :return: tag with estate's geoposition
        """
        return soup.find(id='mapcontainer')

    @staticmethod
    def __find_price(soup: BeautifulSoup) -> Optional[Tag]:
        """
        Finds tag with offer's price and currency.

        :param soup: DOM tags' tree
        :return: tag with offer's shapes
        """
        tag = soup.find('strong', 'xxxx-large')
        return (
            tag if tag is not None
            else soup.find_all('strong', 'xx-large')[1]
        )

    @staticmethod
    def _parse_avatar(soup: BeautifulSoup) -> Optional[str]:
        """
        Extracts offer's avatar source if available.

        :param soup: DOM tags' tree
        :return: offer avatar's source or None
        """
        tag = soup.find('img', 'vtop')
        if tag is not None:
            return tag['src']

    def _parse_published(self, soup: BeautifulSoup) -> date:
        """
        Fetches offer's publication date.

        :param soup: DOM tags' tree
        :return: offer's publication date
        """
        published = self._published_pattern.search(
            self.__find_published(soup).text
        ).groups()
        return date(
            int(published[2]),
            self._months.get(published[1], 1),
            int(published[0])
        )

    def _parse_geolocation(
        self, soup: BeautifulSoup
    ) -> Dict[str, Tuple[float, float]]:
        """
        Finds offer's geoposition and transforms them into point.

        :param soup: DOM tags' tree
        :return: offer's positional data
        """
        tag = self.__find_point(soup)
        return {'point': (float(tag['data-lon']), float(tag['data-lat']))}

    def _parse_shapes(
        self, soup: BeautifulSoup
    ) -> Dict[str, Union[Decimal, str]]:
        """
        Fetches offer's price and currency.

        :param soup: DOM tags' tree
        :return: offer's financial values
        """
        shapes = self._shapes_pattern.match(
            self.__find_price(soup).text
        ).groups()
        return {
            'price': decimalize(shapes[0].replace(' ', '')),
            'currency': shapes[1]
        }

    @staticmethod
    def _parse_pairs(soup: BeautifulSoup) -> Dict[str, str]:
        """
        Extracts offer's tabular data (area, floor, details, etc).

        :param soup: DOM tags' tree
        :return: offer's numeric data & details
        """
        return {
            t.find('th').text: t.find('strong').text.strip('\t\n')
            for t in soup.find_all('table', 'item')
        }

    def _parse_junk(self, url: str, soup: BeautifulSoup) -> Optional[str]:
        if self.__find_junk(soup) is not None:
            return url


class OlxFlatParser(OlxEstateParser):
    """
    Final parsers' progress, specialized on www.olx.ua flat offers' processing.
    """
    _details = json('resources/olx_flat_reaper/details.json')

    def _parse_offer(
        self, url: str, soup: BeautifulSoup, **kwargs: Any
    ) -> Flat:
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

    def __parse_parameters(
        self, pairs: Dict[str, str]
    ) -> Dict[str, Union[int, float]]:
        """
        Extracts basic offer's numeric parameters.

        :param pairs: offer's tabular data
        :return: offer's numeric parameters
        """
        return {
            'area': self._float(pairs.get('Общая площадь')),
            'kitchen_area': self._float(pairs.get('Площадь кухни')),
            'rooms': self._int(pairs.get('Количество комнат')),
            'floor': self._int(pairs.get('Этаж')),
            'total_floor': self._int(pairs.get('Этажность')),
        }


class DomRiaEstateParser(EstateParser):
    """
    Deep parser's evolution, specialized on dom.ria.com offers' processing.

    Class properties:
        _published_pattern: publication date regex pattern
        _months: matches between literal and numeric months
        _json_pattern: regex pattern with offer's API data
        _impurities: extra words to be replaced in an offer's address
    """
    _published_pattern = compile(r'(\d{2}) (\w{3})( \d{4})?')
    _months = {
        'січ': 1, 'янв': 1, 'лют': 2, 'фев': 2, 'бер': 3, 'мар': 3,
        'кві': 4, 'апр': 4, 'тра': 5, 'май': 5, 'чер': 6, 'июн': 6,
        'лип': 7, 'июл': 7, 'сер': 8, 'авг': 8, 'вер': 9, 'сен': 9,
        'жов': 10, 'окт': 10, 'лис': 11, 'ноя': 11, 'гру': 12, 'дек': 12
    }
    _json_pattern = compile(r'STATE__=(.+);\(function')
    _impurities = (' ул.', ' просп.', ' пер.', ' буд.', ' бул.', ' вул.')

    def _parse_stop(self, soup: BeautifulSoup) -> int:
        return int(
            soup.find_all('a', 'page-link')[4].text.replace(' ', '')
        )

    def _check_offer(self, soup: BeautifulSoup) -> bool:
        return (
            self.__find_junk(soup) is None and
            self.__find_description(soup) is not None and
            'Дог' not in self.__find_price(soup)
        )

    @staticmethod
    def __find_junk(soup: BeautifulSoup) -> Optional[Tag]:
        """
        Detects the tag which indicates the offer's obsolescence.

        :param soup: DOM tags' tree
        :return: target tag
        """
        return soup.find('div', 'warning middle')

    @staticmethod
    def __find_description(soup: BeautifulSoup) -> Optional[Tag]:
        """
        Finds the tag with main offer's tabular data.

        :param soup: DOM tags' tree
        :return: tag with main offer's contents
        """
        return soup.find('div', id='description')

    @staticmethod
    def __find_price(soup: BeautifulSoup) -> str:
        """
        Finds offer's price literal.

        :param soup: DOM tags' tree
        :return: offer's price string
        """
        return soup.find('span', 'price').text

    @staticmethod
    def _parse_avatar(soup: BeautifulSoup, avatar: str) -> str:
        """
        Extracts medium offer avatar's source or returns minified one.

        :param soup: DOM tags' tree
        :param avatar: minified avatar source
        :return: offer avatar's source
        """
        tag = soup.find('picture', 'outline')
        return tag.find('img')['src'] if tag is not None else avatar

    def _parse_published(self, soup: BeautifulSoup) -> date:
        """
        Fetches offer's publication date.

        :param soup: DOM tags' tree
        :return: offer's publication date
        """
        published = self._published_pattern.search(
            soup.find('li', 'mt-15').find('b').text
        ).groups()
        return date(
            datetime.today().year if published[2] is None else int(published[2]),
            self._months[published[1]],
            self._int(published[0] if published[0][0] != '0' else published[0][1])
        )

    def _parse_geolocation(
        self, soup: BeautifulSoup
    ) -> Dict[str, Union[str, Tuple[float, float]]]:
        """
        Finds offer's geoposition and transforms them into geodict.

        :param soup: DOM tags' tree
        :return: offer's positional data (either point or geodict)
        """
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

    def _parse_address(self, data: Dict[str, Any]) -> str:
        """
        Parses offer's geo data and fetches address units (locality, street, etc).

        :param data: geoposition's JSON description
        :return: address string
        """
        return ', '.join((
            data.get('city_name_uk', data.get('city_name', '')),
            data.get('district_name_uk', data.get('district_name', '')),
            reduce(
                lambda s, i: s.replace(i, ''), self._impurities,
                data.get('street_name_uk', data.get('street_name', ''))
            )
        ))

    def _parse_price(self, soup: BeautifulSoup) -> Decimal:
        """
        Extracts offer's price (in USD).

        :param soup: DOM tags' tree
        :return: offer's price
        """
        return decimalize(
            self.__find_price(soup).replace(' ', '').replace('$', '')
        )

    def _parse_pairs(self, soup: BeautifulSoup) -> Dict[str, str]:
        return {
            **self.__parse_description(soup), **self.__parse_additional(soup)
        }

    def __parse_description(self, soup: BeautifulSoup) -> Dict[str, str]:
        """
        Fetches offer's main tabular data.

        :param soup: DOM tags' tree
        :return: offer's numeric values and some details
        """
        return {
            t.find('div', 'label').text.strip():
                t.find('div', 'indent').text.strip()
            for t in self.__find_description(soup).find_all(
                'ul', 'unstyle'
            )[1].find_all('li', 'mt-15')
        }

    @staticmethod
    def __parse_additional(soup: BeautifulSoup) -> Dict[str, str]:
        """
        Fetches offer's extra tabular data.

        :param soup: DOM tags' tree
        :return: majority of the offer's details
        """
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

    def _parse_junk(self, url: str, soup: BeautifulSoup) -> Optional[str]:
        if self.__find_junk(soup) is not None:
            return url


class DomRiaFlatParser(DomRiaEstateParser):
    """
    Final parsers' progress, specialized on dom.ria.com flat offers' processing.

    Class properties:
        __area_pattern: regex to extract flat's area shapes
        during the page processing
    """
    _offer_strainer = SoupStrainer('section')
    _details = json('resources/dom_ria_flat_reaper/details.json')
    __area_pattern = compile(r'Площа (\S+)/(\S+)/(\S+)')

    def _parse_page(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        return list(filter(
            lambda o: o is not None, map(
                self.__parse_section,
                soup.find_all('section', 'ticket-clear')
            )
        ))

    def __parse_section(self, tag: Tag) -> Dict[str, Any]:
        """
        Finds offer's specific data during the page processing.

        :param tag: DOM's node
        :return: "raw offer"
        """
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

    def _parse_offer(
        self, url: str, soup: BeautifulSoup, **kwargs: Any
    ) -> Flat:
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

    def _parse_pairs(self, soup: BeautifulSoup) -> Dict[str, str]:
        pairs = super()._parse_pairs(soup)
        pairs['Тип'] = next(filter(
            lambda t: t.endswith(' житло'),
            map(
                lambda t: t.text.strip(),
                soup.find_all('li', 'labelHot')
            )
        ), None)
        return pairs

    def __parse_parameters(
        self, pairs: Dict[str, str]
    ) -> Dict[str, Union[int, float]]:
        """
        Extracts basic offer's numeric parameters (floor, rooms, etc).

        :param pairs: offer's tabular data
        :return: offer's numeric parameters
        """
        return {
            'rooms': self._int(pairs.get('Кімнат')),
            'floor': self._int(pairs.get('Поверх')),
            'total_floor': self._int(pairs.get('Поверховість')),
            'ceiling_height': self._ceiling_height(
                pairs.get('висота стелі')
            )
        }

    def _ceiling_height(self, string: str) -> Optional[float]:
        """
        Calculates flat's ceiling height (dependently on the digits' amount).

        :param string: number's char array
        :return: ceiling height in meters or None
        """
        ceiling_height = self._float(string)
        if ceiling_height is not None:
            return ceiling_height * 10 ** ceil(-log10(ceiling_height))
