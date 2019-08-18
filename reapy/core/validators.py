"""
*reapy*'s numeric validation module

Parsed data structures contain many numeric values. Sometimes offers'
publishers make written mistakes, pointing irrelevant shapes, ranges,
values. That's why :class:`core.validators.Validator` and its successors
are in charge of correct data checks and filtering.
"""
from datetime import timedelta, date
from typing import Any
from core.utils import notnull


class Validator:
    def validate(self, struct: Any) -> bool:
        return notnull(struct)


class FlatValidator(Validator):
    """
    Validator, specialized on the flat checks
    Class properties:
        __limits: a set of max flats' specific areas;
        each value is calculated empirically for each room count
        __expiration: max offers' expiration period; too
        'old' offers shouldn't be taken into account
    """
    __limits = (69.5, 110, 130, 110, 86, 75, 65, 65, 65)
    __expiration = timedelta(days=210)  # TODO: fix the quarter validation

    def validate(self, struct: Any) -> bool:
        return (
            super().validate(struct) and
            struct.area is not None and
            struct.rooms is not None and
            struct.floor is not None and
            struct.total_floor is not None and
            struct.published is not None and
            self.__validate_ranges(struct)
        )

    def __validate_ranges(self, struct: Any) -> bool:
        """
        Checks struct's publication date and
        numeric values concernedly specific ranges

        :param struct: parsed object
        :return: the struct if it's correct and None otherwise
        """
        specific_area = struct.area / struct.rooms
        return (
            date.today() - struct.published < self.__expiration and
            10 <= struct.area < 560 and
            1 <= struct.rooms <= 9 and
            13.5 <= specific_area <= self.__limits[struct.rooms - 1] and
            1 <= struct.total_floor <= 47 and
            0 <= struct.floor <= struct.total_floor and (
                struct.kitchen_area is None or
                2 <= struct.kitchen_area < struct.area
            ) and (
                struct.living_area is None or
                5 < struct.living_area < struct.area
            ) and (
                struct.ceiling_height is None or
                1.8 <= struct.ceiling_height <= 6
            )
        )
