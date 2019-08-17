"""
This module is in charge of special networkers - crawlers

Crawlers are very useful abstraction layer upon `aiohttp.ClientSession` -
they cover this connection pool, supplying convenient API for HTTP requests.
Each crawler has a specific set of parameters, suitable for the target site.
"""
from asyncio import Semaphore, gather
from typing import Dict, Union, List, Any, Iterator, Iterable
from aiohttp.client import ClientSession
from core.scribblers import Scribbler
from core.decorators import measurable, networking


class Crawler:
    """
    Basic asynchronous currency calculator. It leverages an HTTP client
    to perform currency rates' requests and an executor to fulfil CPU bound
    calculations. To make them effective, converter caches the actual rates
    in the local file.

    Class properties:
        _page_url: specific resource url template
        _limit: the max number of concurrent connections to the same site
        _timeout: default HTTP request timeout

    Instance properties:
        _session: HTTP connection pool
        _scribbler: statistics entity which writes success & failure shapes
        _semaphore: HTTP connection "restriction frame"
    """
    _page_url = None
    _limit = 80
    _timeout = 10

    def __init__(self, session: ClientSession, scribbler: Scribbler):
        self._session = session
        self._scribbler = scribbler
        self._semaphore = Semaphore(self._limit)

    async def get_json(self, url: str, **kwargs) -> Union[List, Dict]:
        """
        Makes an HTTP request and returns response in JSON format.

        :param url: request's URL
        :param kwargs: additional config like timeout, content-type, etc.
        :return: JSON content via native python objects
        """
        return await self.__get_content(url, 'json', **kwargs)

    @networking
    async def __get_content(self, url: str, content_type: str, **kwargs) -> Any:
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

    @measurable('page crawling')
    async def get_pages(self, indices: List[int], **kwargs) -> Iterator:
        """
        Returns a set of HTML pages from the current site via pagination.

        :param indices: a sequence of pagination indices
        :param kwargs: additional config like timeout, content-type, etc.
        :return: a sequence of HTMLs
        """
        pages = await gather(*(self.__get_page(i, **kwargs) for i in indices))
        return filter(lambda o: o is not None, pages)

    async def __get_page(self, index: int, **kwargs) -> str:
        """
        Fulfills single HTTP request and returns the HTML contents.

        :param index: page's index at the site's pagination
        :param kwargs: additional config like timeout, content-type, etc.
        :return: HTML file's contents
        """
        return await self.get_text(self._page_url.format(index), **kwargs)

    async def get_text(self, url: str, **kwargs) -> str:
        """
        Makes an HTTP request and returns response in HTML (text) format.

        :param url: request's URL
        :param kwargs: additional config like timeout, content-type, etc.
        :return: HTML file's contents
        """
        return await self.__get_content(url, 'text', **kwargs)

    @measurable('offer crawling')
    async def get_offers(self, forms: Iterable, **kwargs) -> Iterator:
        """
        Maps the offer dicts' sequence, adding to each one 'markup' value.
        An offer - it's a dict, which contains object's publication info,
        like URL, page's HTML, etc. "Raw offer" - a dict without 'markup'
        key-value pair.

        :param forms: "raw" offer's list
        :param kwargs: additional config like timeout, content-type, etc.
        :return: a filtered set of offers
        """
        offers = await gather(*(self.__get_offer(f, **kwargs) for f in forms))
        return filter(lambda o: o['markup'] is not None, offers)

    async def __get_offer(self, form: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """
        Maps a "raw offer" form into a normal offer dict.

        :param form: "raw offer" dict
        :param kwargs: additional config like timeout, content-type, etc.
        :return: the same dict with a 'markup' field if the request succeeded
        """
        form['markup'] = await self.get_text(form['url'], **kwargs)
        if form['markup'] is None:
            await self._scribbler.add('unresponded')
        return form


class OlxFlatCrawler(Crawler):
    """
    A crawler which searches flat offers from `www.olx.ua <https://www.olx.ua/>`_.
    """
    _page_url = 'https://www.olx.ua/nedvizhimost/kvartiry-' \
                'komnaty/prodazha-kvartir-komnat/?page={}'


class DomRiaFlatCrawler(Crawler):
    """
    A crawler which searches flat offers from `www.olx.ua <https://dom.ria.com/>`_.
    """
    _page_url = 'https://dom.ria.com/uk/prodazha-kvartir/?page={}'
    _limit = 190
    _timeout = 13
