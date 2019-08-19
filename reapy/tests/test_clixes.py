from uvloop import install
from core.clixes import Clix
from asyncio import run, sleep
from random import uniform, randint
from time import time


async def generate():
    return [[3, -6], [2], [], [5, 9, 0, -23]]


def flatten(ils):
    return [i for il in ils for i in il]


def convert(value):
    return (value + 10) * 3 - 5


async def calc(value):
    await sleep(uniform(0.3, 2))
    return value % randint(40, 500)


async def output(value):
    print(value)


install()
start = time()
run(
    Clix(generate)
    .flatten(flatten)
    .sieve(convert, lambda i: i > 25)
    .map(lambda i: i + 10)
    .reform(calc, lambda i: i > 16)
    .apply(output)
)
end = time()
print(f'Total time: {end - start}')
