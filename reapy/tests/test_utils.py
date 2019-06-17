from decimal import Decimal
from unittest import TestCase
from core.utils import decimalize, snake_case


class UtilsTestCase(TestCase):
    def test_decimalize(self):
        cases = (
            (0, Decimal('0')),
            (1.2, Decimal('1.2')),
            (-1.34, Decimal('-1.34')),
            (2.345, Decimal('2.345')),
            (0.9999, Decimal('1')),
            (45.5433, Decimal('45.543')),
            (-12.65, Decimal('-12.65')),
            (19.543, Decimal('19.543')),
            (0.0001, Decimal('0')),
            (0.009, Decimal('0.009'))
        )
        for case in cases:
            self.assertEqual(decimalize(case[0]), case[1])

    def test_snake_case(self):
        cases = (
            ('URL', 'url'), ('AdHoc', 'ad_hoc'), ('IDs', 'ids'), ('DomRiaFlatParser', 'dom_ria_flat_parser'),
            ('HTML5Lib', 'html5lib'), ('SpringBootBeanPostProcessor', 'spring_boot_bean_post_processor')
        )
        for case in cases:
            self.assertEqual(snake_case(case[0]), case[1])
