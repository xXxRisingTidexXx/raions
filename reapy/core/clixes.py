from concurrent.futures.process import ProcessPoolExecutor
from asyncio import Queue, gather, get_event_loop
from typing import Callable, Generator
from core.utils import notnull, filter_map


class Clix:
    def __init__(self, creator: Callable):
        self._creator = creator
        self._queue = Queue()
        self._executor = ProcessPoolExecutor()
        self._loop = get_event_loop()

    def reform(self, mapper: Callable, predicate: Callable = notnull):
        self._queue.put_nowait(
            lambda iterable: filter_map(iterable, mapper, predicate)
        )
        return self

    def map(self, mapper: Callable):
        self._queue.put_nowait(
            lambda iterable: gather(*(self.__execute(mapper, i) for i in iterable))
        )
        return self

    def __execute(self, function: Callable, *args) -> Generator:
        return self._loop.run_in_executor(self._executor, function, *args)

    def flatten(self, flattener: Callable):
        self._queue.put_nowait(lambda iterable: self.__execute(flattener, iterable))
        return self

    def sieve(self, mapper: Callable, predicate: Callable = notnull):
        return self.reform(lambda i: self.__execute(mapper, i), predicate)

    async def apply(self, applier: Callable):
        iterable = await self._creator()
        while not self._queue.empty():
            function = await self._queue.get()
            iterable = await function(iterable)
        await gather(*(map(applier, iterable)))
        self._executor.shutdown()
