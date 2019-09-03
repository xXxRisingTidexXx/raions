from datetime import date
from pytest import fixture
from core.structs import Flat
from core.validators import FlatValidator


@fixture
def flat_validator() -> FlatValidator:
    return FlatValidator()


def test_validate(flat_validator: FlatValidator):
    assert flat_validator.validate(Flat(
        url='x1', published=date.today(), area=45.8, rooms=2, floor=6, total_floor=9
    ))
    assert flat_validator.validate(Flat(
        url='x2', published=date.today(), area=245, kitchen_area=18,
        living_area=139, rooms=4, floor=16, total_floor=16, ceiling_height=3
    ))


def test_validate_emptiness(flat_validator: FlatValidator):
    assert not flat_validator.validate(None)
    assert not flat_validator.validate({'area': 54})
    assert not flat_validator.validate(Flat(
        published=date.today(), area=2, kitchen_area=18,
        rooms=2, floor=5, total_floor=9
    ))
    assert not flat_validator.validate(Flat(
        published=date.today(), rooms=3, floor=5
    ))
    assert not flat_validator.validate(Flat(
        published=date.today(), kitchen_area=1.1,
        living_area=23, rooms=2, floor=1, total_floor=5
    ))
    assert not flat_validator.validate(Flat(
        published=date.today(), area=9876563,
        kitchen_area=784309, rooms=1, floor=12, total_floor=16
    ))
    assert not flat_validator.validate(Flat(
        published=date.today(), area=0.345543, kitchen_area=0.11,
        living_area=0.23, rooms=1, floor=13, total_floor=16
    ))
    assert not flat_validator.validate(Flat(
        published=date.today(), area=25, kitchen_area=25,
        living_area=25, rooms=1, floor=1, total_floor=1
    ))
    assert not flat_validator.validate(Flat(
        published=date.today(), area=98, kitchen_area=1.02,
        rooms=2, floor=7, total_floor=12
    ))
    assert not flat_validator.validate(Flat(
        published=date.today(), area=98, kitchen_area=1.02,
        rooms=3, floor=6, total_floor=9
    ))
    assert not flat_validator.validate(Flat(
        published=date.today(), area=325, kitchen_area=45,
        living_area=225, rooms=1, floor=12, total_floor=16
    ))
    assert not flat_validator.validate(Flat(
        published=date.today(), area=98, kitchen_area=21,
        rooms=9, floor=7, total_floor=16
    ))
    assert not flat_validator.validate(Flat(
        published=date.today(), area=48, kitchen_area=17.6,
        rooms=6, floor=7, total_floor=9
    ))
    assert not flat_validator.validate(Flat(
        published=date.today(), area=325, kitchen_area=45,
        living_area=225, rooms=1, floor=12, total_floor=16
    ))
    assert not flat_validator.validate(Flat(
        published=date.today(), area=170, kitchen_area=33,
        living_area=110, rooms=3, floor=12, total_floor=55
    ))
    assert not flat_validator.validate(Flat(
        published=date.today(), area=48, kitchen_area=13.6,
        rooms=2, floor=17, total_floor=9
    ))
    assert not flat_validator.validate(Flat(
        published=date.today(), area=170, kitchen_area=33,
        living_area=110, rooms=3, floor=12, total_floor=55
    ))
    assert not flat_validator.validate(Flat(
        published=date(2017, 4, 13), area=170,
        living_area=110, rooms=3, floor=12, total_floor=21
    ))
    assert not flat_validator.validate(Flat(
        published=date.today(), area=81, kitchen_area=26, living_area=51,
        rooms=3, floor=12, total_floor=16, ceiling_height=8.1
    ))
    assert not flat_validator.validate(Flat(
        published=date.today(), area=81, kitchen_area=26, living_area=51,
        rooms=3, floor=12, total_floor=16, ceiling_height=0.27
    ))
