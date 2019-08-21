from concurrent.futures.process import ProcessPoolExecutor
from asyncio import Queue, gather, get_event_loop
from typing import Callable, Generator, Iterable, List, Any
from core.utils import notnull, filter_map


class Clix:
    def __init__(self, creator: Callable):
        self._creator = creator
        self._queue = Queue()
        self._executor = ProcessPoolExecutor()
        self._loop = None

    def reform(self, mapper: Callable, predicate: Callable = notnull) -> 'Clix':
        self._queue.put_nowait(
            lambda iterable: filter_map(iterable, mapper, predicate)
        )
        return self

    def map(self, mapper: Callable) -> 'Clix':
        self._queue.put_nowait(
            lambda iterable: gather(*(self.__execute(mapper, i) for i in iterable))
        )
        return self

    def __execute(self, function: Callable, *args) -> Generator:
        return self._loop.run_in_executor(self._executor, function, *args)

    def flatten(self, flattener: Callable) -> 'Clix':
        self._queue.put_nowait(lambda iterable: self.__execute(flattener, iterable))
        return self

    def sieve(self, mapper: Callable, predicate: Callable = notnull) -> 'Clix':
        return self.reform(lambda i: self.__execute(mapper, i), predicate)

    async def apply(self, applier: Callable) -> Iterable:
        self._loop = get_event_loop()
        iterable = await self._creator()
        while not self._queue.empty():
            function = await self._queue.get()
            iterable = await function(iterable)
        self._executor.shutdown()
        return await gather(*(map(applier, iterable)))

    @staticmethod
    async def __skip(value: Any) -> Any:
        return value

    async def list(self) -> List:
        iterable = await self.apply(self.__skip)
        return list(iterable)
