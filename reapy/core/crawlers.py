"""
This module is in charge of special networkers - crawlers

Crawlers are very useful abstraction layer upon `aiohttp.ClientSession` -
they cover this connection pool, supplying convenient API for HTTP requests.
Each crawler has a specific set of parameters, suitable for the target site.
"""
from asyncio import Semaphore
from typing import Dict, Union, List, Any
from aiohttp.client import ClientSession
from core.decorators import networking


class Crawler:
    """
    Simple asynchronous HTTP client, which encapsulates the logic of web requests
    inside itself. All descendants are specialized on concrete web sites, but the
    current class supplies simple interface of the web interaction with any site.
    It's reusable and portable, that's why any crawler can easily fetch data via
    the Internet.

    Class properties:
        _limit: the max number of concurrent connections to the same site
        _timeout: default HTTP request timeout

    Instance properties:
        _session: HTTP connection pool
        _scribbler: statistics entity which writes success & failure shapes
        _semaphore: HTTP connection "restriction frame"
    """
    _limit = 10
    _timeout = 1

    def __init__(self):
        self._session = None
        self._semaphore = Semaphore(self._limit)

    async def prepare(self):
        """
        Acquires HTTP connection pool.
        """
        self._session = ClientSession()

    async def get_json(self, url: str, **kwargs: Any) -> Union[List, Dict]:
        """
        Makes an HTTP request and returns response in JSON format.

        :param url: request's URL
        :param kwargs: additional config like timeout, content-type, etc.
        :return: JSON content via native python objects
        """
        return await self.__get_content(url, 'json', **kwargs)

    @networking
    async def __get_content(
        self, url: str, content_type: str, **kwargs: Any
    ) -> Any:
        """
        Makes an HTTP request and returns response in a specified format.

        :param url: request's URL
        :param content_type: response's data type, like JSON, text, etc.
        :param kwargs: additional config like timeout, content-type, etc.
        :return: response's content
        """
        kwargs['timeout'] = kwargs.get('timeout', self._timeout)
        async with kwargs.pop('semaphore', self._semaphore):
            async with self._session.get(url, **kwargs) as response:
                return await getattr(response, content_type)()

    async def get_text(self, url: str, **kwargs: Any) -> str:
        """
        Makes an HTTP request and returns response in HTML (text) format.

        :param url: request's URL
        :param kwargs: additional config like timeout, content-type, etc.
        :return: HTML file's markup
        """
        return await self.__get_content(url, 'text', **kwargs)

    async def spare(self):
        """
        Releases HTTP connection pool.
        """
        await self._session.close()


class EstateCrawler(Crawler):
    _page_url = None

    async def get_page(self, index: int) -> str:
        """
        Fulfills single HTTP request and returns the HTML markup.

        :param index: page's index at the site's pagination
        :return: HTML file's markup
        """
        return await self.get_text(self._page_url.format(index))

    async def get_offer(self, form: Dict[str, Any]) -> Dict[str, Any]:
        """
        Maps a "raw offer" form into a normal offer dict.

        :param form: "raw offer" dict
        :return: the same dict with a 'markup' field if the request succeeded
        """
        form['markup'] = await self.get_text(form['url'])
        return form


class OlxFlatCrawler(EstateCrawler):
    """
    A crawler which searches flat offers from `www.olx.ua <https://www.olx.ua/>`_.
    """
    _page_url = 'https://www.olx.ua/nedvizhimost/kvartiry-' \
                'komnaty/prodazha-kvartir-komnat/?page={}'
    _limit = 80
    _timeout = 10


class DomRiaFlatCrawler(EstateCrawler):
    """
    A crawler which searches flat offers from `www.olx.ua <https://dom.ria.com/>`_.
    """
    _page_url = 'https://dom.ria.com/uk/prodazha-kvartir/?page={}'
    _limit = 190
    _timeout = 13
