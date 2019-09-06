from decimal import Decimal
from typing import Callable, List
from core.utils import decimalize, snake_case, notnull, filter_map, find
from asyncio import sleep
from pytest import mark, raises


def test_snake_case():
    assert snake_case('URL') == 'url'
    assert snake_case('AdHoc') == 'ad_hoc'
    assert snake_case('IDs') == 'ids'
    assert snake_case('DomRiaFlatParser') == 'dom_ria_flat_parser'
    assert snake_case('HTML5Lib') == 'html5lib'
    assert snake_case('SpringBootBeanPostProcessor') == 'spring_boot_bean_post_processor'


def test_notnull():
    assert notnull({})
    assert notnull(0)
    assert not notnull(None)


def test_decimalize():
    assert decimalize(0) == Decimal('0')
    assert decimalize(1.2) == Decimal('1.2')
    assert decimalize(-1.34) == Decimal('-1.34')
    assert decimalize(2.345) == Decimal('2.345')
    assert decimalize(0.9999) == Decimal('1')
    assert decimalize(45.5433) == Decimal('45.543')
    assert decimalize(0.0001) == Decimal('0')
    assert decimalize(-13.3287) == Decimal('-13.329')


def __mapper_maker(latencies: List[float]) -> Callable:
    iterator = iter(latencies)

    async def mapper(word: str) -> int:
        await sleep(next(iterator, 1))
        return len(word)
    return mapper


@mark.asyncio
@mark.parametrize('latencies', [
    [0.2, 0.3, 0.1, 0.4, 0.5, 0.1],
    [0.3, 0.3, 0.3, 0.3, 0.3, 0.3],
    [0.1, 0.17, 0.1, 0.6, 0.1, 0.7]
])
async def test_filter_map_with_latencies(latencies: List[float]):
    iterator = await filter_map(
        ['Iqos', 'Phantom', 'Vape', 'Glo', 'Parma', 'Ad Hoc'],
        __mapper_maker(latencies),
        lambda l: l > 4
    )
    assert set(iterator) == {6, 5, 7}


@mark.asyncio
async def test_filter_map_emptiness():
    iterator = await filter_map(
        ['Colombo', 'Atlas', 'Django', 'Aldente'],
        __mapper_maker([0.1, 0.3, 0.18, 0.2]),
        lambda l: l < -5
    )
    assert list(iterator) == []


@mark.asyncio
async def test_filter_map_errors():
    with raises(TypeError):
        await filter_map(
            ['Karna', 'Onuka', -12],
            __mapper_maker([0.1, 0.3, 0.2]),
            lambda l: l is not None
        )


@mark.parametrize('predicate, expected', [
    ((lambda w: w.startswith('Моя')), 'Моя мила'),
    ((lambda w: 'xus' in w.lower()), 'NeXus'),
    ((lambda w: w.isdecimal()), '911'),
    ((lambda w: len(w.split('-')) > 3), 'New-Old-Bad-Day')
])
def test_find_something(predicate: Callable, expected: str):
    assert expected == find(predicate, [
        'Cassandra', 'Bad Liar', 'S3', 'New-Old-Bad-Day', 'Ich Will', 'Моя мила',
        'Пирамидаль', 'A-b-y-s-s', 'NeXus', 'Моя боротьба', 'xustain', '911'
    ])


@mark.parametrize('predicate', [
    (lambda w: len(w) > 18),
    (lambda w: 'shine' in w),
    (lambda w: w.replace(' ', ',') == 'Oh, my')
])
def test_find_nothing(predicate: Callable):
    assert find(predicate, [
        'Oh my Zsh', 'Fuckin shit', 'Shirts', 'T-shirt', 'Oh, my', 'KS strangers'
    ]) is None


def test_find_errors():
    with raises(AttributeError):
        find(
            lambda w: w.endswith('sid'),
            ['Boobs', 'Tits', 'Dick', 'Pussy', 'Vgine', {'a': 4}, 'Abbaside']
        )
