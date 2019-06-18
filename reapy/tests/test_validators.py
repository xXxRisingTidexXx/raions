from datetime import date
from unittest import TestCase
from asynctest import CoroutineMock
from core.decorators import processtest
from core.structs import Flat
from core.validators import FlatValidator


class FlatValidatorTestCase(TestCase):
    @processtest
    async def test_validate(self, executor):
        validator = FlatValidator(executor, CoroutineMock())
        structs = (
            Flat(
                url='x1', published=date.today(), area=45.8, rooms=2, floor=6, total_floor=9
            ),
            Flat(
                url='x2', published=date.today(), area=245, kitchen_area=18,
                living_area=139, rooms=4, floor=16, total_floor=16, ceiling_height=3
            ),
            Flat(
                published=date.today(), area=2, kitchen_area=18, rooms=2, floor=5, total_floor=9
            ),
            Flat(
                published=date.today(), rooms=3, floor=5
            ),
            Flat(
                published=date.today(), kitchen_area=1.1, living_area=23, rooms=2, floor=1, total_floor=5
            ),
            Flat(
                published=date.today(), area=9876563, kitchen_area=784309, rooms=1, floor=12, total_floor=16
            ),
            Flat(
                published=date.today(), area=0.345543, kitchen_area=0.11,
                living_area=0.23, rooms=1, floor=13, total_floor=16
            ),
            Flat(
                published=date.today(), area=25, kitchen_area=25, living_area=25, rooms=1, floor=1, total_floor=1
            ),
            Flat(
                published=date.today(), area=98, kitchen_area=1.02, rooms=2, floor=7, total_floor=12
            ),
            Flat(
                published=date.today(), area=98, kitchen_area=1.02, rooms=3, floor=6, total_floor=9
            ),
            Flat(
                published=date.today(), area=325, kitchen_area=45, living_area=225, rooms=1, floor=12, total_floor=16
            ),
            Flat(
                published=date.today(), area=98, kitchen_area=21, rooms=9, floor=7, total_floor=16
            ),
            Flat(
                published=date.today(), area=48, kitchen_area=17.6, rooms=6, floor=7, total_floor=9
            ),
            Flat(
                published=date.today(), area=325, kitchen_area=45, living_area=225, rooms=1, floor=12, total_floor=16
            ),
            Flat(
                published=date.today(), area=170, kitchen_area=33, living_area=110, rooms=3, floor=12, total_floor=55
            ),
            Flat(
                published=date.today(), area=48, kitchen_area=13.6, rooms=2, floor=17, total_floor=9
            ),
            Flat(
                published=date.today(), area=170, kitchen_area=33, living_area=110, rooms=3, floor=12, total_floor=55
            ),
            Flat(
                published=date(2017, 4, 13), area=170, living_area=110, rooms=3, floor=12, total_floor=21
            ),
            Flat(
                published=date.today(), area=81, kitchen_area=26, living_area=51,
                rooms=3, floor=12, total_floor=16, ceiling_height=8.1
            ),
            Flat(
                published=date.today(), area=81, kitchen_area=26, living_area=51,
                rooms=3, floor=12, total_floor=16, ceiling_height=0.27
            )
        )
        expected = [
            Flat(
                url='x1', published=date.today(), area=45.8, rooms=2, floor=6, total_floor=9
            ),
            Flat(
                url='x2', published=date.today(), area=245, kitchen_area=18,
                living_area=139, rooms=4, floor=16, total_floor=16, ceiling_height=3
            )
        ]
        self.assertListEqual(list(await validator.validate_all(structs)), expected)
