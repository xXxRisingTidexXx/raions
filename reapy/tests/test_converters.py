from asynctest import CoroutineMock
from unittest import TestCase
from core.crawlers import Crawler
from core.decorators import webtest
from core.converters import NBUConverter
from core.utils import decimalize


class NBUConverterTestCase(TestCase):
    @webtest
    async def test_convert(self, session, executor, scribbler):
        converter = NBUConverter(Crawler(session, scribbler), executor)
        converter._crawler.get_json = CoroutineMock(
            side_effect=(
                [
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
                ],
                None
            )
        )
        await converter.prepare()
        cases = (
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
        )
        for case in cases:
            self.assertEqual(await converter.convert(case[0], case[1], case[2]), case[3])
            if case[1] == 'USD' or case[1] == '$':
                self.assertEqual(await converter.convert_to_usd(case[0], case[2]), case[3])
        await converter.prepare()
        self.assertIsNone(await converter.convert_to_usd('UAH', decimalize(25000)))
        self.assertIsNone(await converter.convert('€', '$', decimalize(42700)))
        self.assertEqual(await converter.convert_to_usd('$', decimalize(23000)), decimalize(23000))
