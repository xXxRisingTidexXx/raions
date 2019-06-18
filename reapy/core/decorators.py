import logging
from asyncio import run
from concurrent.futures import ProcessPoolExecutor
from time import time
from aiohttp import ClientSession
from asyncpg import create_pool
from uvloop import install
from . import TESTING_DSN


def measurable(name):
    def decorator_wrapper(coroutine):
        async def coroutine_wrapper(*args, **kwargs):
            logging.info(f'{name} has been started')
            start = time()
            result = await coroutine(*args, **kwargs)
            end = time()
            logging.info(f'{name} has been finished, it took {end - start:.2f} sec')
            return result
        return coroutine_wrapper
    return decorator_wrapper


def dbtest(main):
    def wrapper(test_case):
        install()
        run(runner(main, test_case))

    async def runner(test, test_case):
        async with create_pool(TESTING_DSN) as pool:
            await __truncate_tables(pool)
            try:
                await test(test_case, pool)
            finally:
                await __truncate_tables(pool)
    return wrapper


async def __truncate_tables(pool):
    async with pool.acquire() as connection:
        await connection.execute('TRUNCATE TABLE core_user_saved_flats CASCADE')
        await connection.execute('TRUNCATE TABLE core_user CASCADE')
        await connection.execute('TRUNCATE TABLE flats_details CASCADE')
        await connection.execute('TRUNCATE TABLE details CASCADE')
        await connection.execute('TRUNCATE TABLE flats CASCADE')
        await connection.execute('TRUNCATE TABLE geolocations CASCADE')


def processtest(main):
    def wrapper(test_case):
        install()
        run(runner(main, test_case))

    async def runner(test, test_case):
        with ProcessPoolExecutor() as executor:
            await test(test_case, executor)
    return wrapper


def webtest(main):
    def wrapper(test_case):
        install()
        run(runner(main, test_case))

    async def runner(test, test_case):
        async with ClientSession() as session:
            with ProcessPoolExecutor() as executor:
                await test(test_case, session, executor)
    return wrapper
