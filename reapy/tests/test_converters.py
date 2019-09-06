from decimal import Decimal
from asynctest import CoroutineMock
from pytest import mark, fixture, raises
from core.crawlers import Crawler
from core.converters import NBUConverter
from core.utils import decimalize


@fixture
async def nbu_converter() -> NBUConverter:
    crawler = Crawler()
    await crawler.prepare()
    crawler.get_json = CoroutineMock(return_value=[
        {
            "r030": 840,
            "txt": "Долар США",
            "rate": 26.619328,
            "cc": "USD",
            "exchangedate": "13.05.2019"
        },
        {
            "r030": 978,
            "txt": "Євро",
            "rate": 29.608679,
            "cc": "EUR",
            "exchangedate": "13.05.2019"
        }
    ])
    converter = NBUConverter(crawler)
    await converter.prepare()
    yield converter
    await crawler.spare()


@mark.parametrize('fr, to, amount, expected', [
    ('грн.', 'USD', decimalize(1), decimalize(0.038)),
    ('UAH', 'USD', decimalize(1), decimalize(0.038)),
    ('EUR', 'USD', decimalize(1), decimalize(1.112)),
    ('UAH', 'USD', decimalize(200000), decimalize(7600)),
    ('EUR', 'USD', decimalize(1000), decimalize(1112)),
    ('EUR', '$', decimalize(1000), decimalize(1112)),
    ('EUR', 'USD', decimalize(11500), decimalize(12788)),
    ('EUR', 'USD', decimalize(30000), decimalize(33360)),
    ('UAH', 'USD', decimalize(50000), decimalize(1900)),
    ('UAH', 'USD', decimalize(1300000), decimalize(49400)),
    ('EUR', 'USD', decimalize(5670), decimalize(6305.04)),
    ('UAH', 'USD', decimalize(4671000), decimalize(177498)),
    ('грн.', '$', decimalize(4671000), decimalize(177498)),
    ('$', '$', decimalize(15000), decimalize(15000)),
    ('€', 'USD', decimalize(30000), decimalize(33360)),
    ('UAH', '$', decimalize(200000), decimalize(7600)),
    ('грн.', '$', decimalize(200000), decimalize(7600)),
    ('€', 'USD', decimalize(11500), decimalize(12788)),
    ('€', '$', decimalize(1), decimalize(1.112))
])
@mark.asyncio
async def test_convert_successful(
    nbu_converter: NBUConverter, fr: str, to: str,
    amount: Decimal, expected: Decimal
):
    assert nbu_converter.convert(fr, to, amount) == expected


@mark.parametrize('fr, amount, expected', [
    ('EUR', decimalize(1), decimalize(1.112)),
    ('UAH', decimalize(200000), decimalize(7600)),
    ('EUR', decimalize(1000), decimalize(1112)),
    ('€', decimalize(30000), decimalize(33360)),
    ('UAH', decimalize(200000), decimalize(7600)),
    ('грн.', decimalize(200000), decimalize(7600))
])
@mark.asyncio
async def test_convert_to_usd_successful(
    nbu_converter: NBUConverter, fr: str,
    amount: Decimal, expected: Decimal
):
    assert nbu_converter.convert_to_usd(fr, amount) == expected


@fixture
async def unhealthy_converter() -> NBUConverter:
    crawler = Crawler()
    await crawler.prepare()
    crawler.get_json = CoroutineMock(return_value=None)
    converter = NBUConverter(crawler)
    await converter.prepare()
    yield converter
    await crawler.spare()


@mark.asyncio
async def test_convert_unhealthy(unhealthy_converter: NBUConverter):
    assert unhealthy_converter.convert_to_usd(
        'UAH', decimalize(25000)
    ) is None
    assert unhealthy_converter.convert(
        '€', '$', decimalize(42700)
    ) is None
    assert unhealthy_converter.convert_to_usd(
        '$', decimalize(23000)
    ) == decimalize(23000)


@mark.asyncio
async def test_convert_with_errors(nbu_converter: NBUConverter):
    with raises(KeyError):
        nbu_converter.convert_to_usd('RUB', Decimal(18000))
