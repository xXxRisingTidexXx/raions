import logging
from asyncio import Semaphore, TimeoutError, gather
from aiohttp import ContentTypeError, ClientError, ClientPayloadError
from aiohttp.client import TooManyRedirects
from .decorators import measurable


class Crawler:
    _page_url = None
    _limit = 100
    _timeout = 10

    def __init__(self, session, scribbler):
        self._session = session
        self._scribbler = scribbler
        self._semaphore = Semaphore(self._limit)

    async def get_json(self, url, **kwargs):
        return await self.__get_content(url, 'json', **kwargs)

    async def __get_content(self, url, content_type, **kwargs):
        try:
            kwargs['timeout'] = kwargs.get('timeout', self._timeout)
            async with kwargs.pop('semaphore', self._semaphore):
                async with self._session.get(url, **kwargs) as response:
                    return await getattr(response, content_type)()
        except (TimeoutError, TooManyRedirects, ClientPayloadError):
            pass
        except ContentTypeError:
            logging.warning(
                f'{url} crawling failed, possibly \'cause of TooManyRequests'
            )
        except ClientError:
            logging.exception(f'{url} crawling failed')

    @measurable('page crawling')
    async def get_pages(self, indices, **kwargs):
        return filter(
            lambda o: o is not None,
            await gather(*(self.__get_page(i, **kwargs) for i in indices))
        )

    async def __get_page(self, index, **kwargs):
        return await self.get_text(self._index_page_url(index), **kwargs)

    async def get_text(self, url, **kwargs):
        return await self.__get_content(url, 'text', **kwargs)

    def _index_page_url(self, index):
        return self._page_url.format(index)

    @measurable('offer crawling')
    async def get_offers(self, offers, **kwargs):
        return filter(
            lambda o: o['markup'] is not None,
            await gather(*(self.__get_offer(o, **kwargs) for o in offers))
        )

    async def __get_offer(self, offer, **kwargs):
        offer['markup'] = await self.get_text(offer['url'], **kwargs)
        if offer['markup'] is None:
            await self._scribbler.add('unresponded')
        return offer


class OlxFlatCrawler(Crawler):
    _page_url = 'https://www.olx.ua/nedvizhimost/kvartiry' \
                '-komnaty/prodazha-kvartir-komnat/?page={}'


class DomRiaFlatCrawler(Crawler):
    _page_url = 'https://dom.ria.com/uk/prodazha-kvartir/?page={}'
    _limit = 190
    _timeout = 13
