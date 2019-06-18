from asyncio import get_event_loop
from datetime import timedelta, date
from .decorators import measurable
from .utils import map_filter


class Validator:
    class _Shaft:
        def validate(self, struct):
            pass

    _shaft_class = _Shaft

    def __init__(self, executor, scribbler):
        self._executor = executor
        self._scribbler = scribbler
        self._loop = get_event_loop()
        self._shaft = self._shaft_class()

    @measurable('validation')
    async def validate_all(self, structs):
        return await map_filter(structs, self.__validate)

    async def __validate(self, struct):
        is_valid = await self._loop.run_in_executor(
            self._executor, self._shaft.validate, struct
        )
        if is_valid:
            return struct


class FlatValidator(Validator):
    class _Shaft(Validator._Shaft):
        __limits = (69.5, 110, 130, 110, 86, 75, 65, 65, 65)
        __expiration = timedelta(days=210)

        def validate(self, struct):
            return (
                struct.area is not None and
                struct.rooms is not None and
                struct.floor is not None and
                struct.total_floor is not None and
                struct.published is not None and
                self.__validate_ranges(struct)
            )

        def __validate_ranges(self, struct):
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

    _shaft_class = _Shaft
