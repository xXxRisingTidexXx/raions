"""
*reapy*'s numeric validation module

Parsed data structures contain many numeric values. Sometimes offers'
publishers make written mistakes, pointing irrelevant shapes, ranges,
values. That's why :class:`core.validators.Validator` and its successors
are in charge of correct data checks and filtering.
"""
from asyncio import get_event_loop
from datetime import timedelta, date
from .decorators import measurable
from .utils import map_filter


class Validator:
    """
    Checks the validity of the parsed structures

    Basically, validation process is a simple stuff: a sequence of structs
    is sieved through a special filter. Each struct with irrelevant field
    values would be discarded; the others would pass further.

    Class properties:
        _shaft_class (Validator._Shaft): an inner class, which wraps all
        synchronous calculations (to be able to call them in the executor)

    Instance properties:
        _executor (ProcessPoolExecutor): CPU bound problems' calculator
        _scribbler (Scribbler): shape statistician
        _loop (Any): asyncio event loop
        _shaft (Converter._Shaft): synchronous functions' wrapper
    """
    class _Shaft:
        """
        An inner class, which covers CPU bound calculations

        Asynchronous context requires CPU bound problems to be done in an
        executor, that's why :class:`concurrent.futures.ProcessPoolExecutor`
        is used in :class:`core.validators.Validator`. But multiprocessing
        classes use :mod:`pickles`, which causes problems with serialization.
        That's why converter can't pass its methods to the executor and why it
        requires extra object with synchronous methods.
        """
        def validate(self, struct):
            """
            Checks the struct special fields' values. If all of them are correct,
            the struct will pass.

            :param struct: the parsed object
            :return: the struct if it's valid and None otherwise
            """
            pass

    _shaft_class = _Shaft

    def __init__(self, executor, scribbler):
        """
        Initializes CPU bound problems' calculator and shape statistician

        :param executor: CPU bound problems' calculator
        :param scribbler: shape statistician
        """
        self._executor = executor
        self._scribbler = scribbler
        self._loop = get_event_loop()
        self._shaft = self._shaft_class()

    @measurable('validation')
    async def validate_all(self, structs):
        """
        Validates the structs' sequence

        :param structs: set of parsed objects
        :return: set of validated objects
        """
        return await map_filter(structs, self.__validate)

    async def __validate(self, struct):
        """
        Validates the single struct

        :param struct: parsed object
        :return: the struct if it's correct and None otherwise
        """
        is_valid = await self._loop.run_in_executor(
            self._executor, self._shaft.validate, struct
        )
        if is_valid:
            return struct
        await self._scribbler.add('invalidated')


class FlatValidator(Validator):
    """
    Validator, specialized on the flat checks
    """
    class _Shaft(Validator._Shaft):
        """
        Synchronous validator's core, which checks flats. Among other
        params, flats' specific area and offers' publication dates are
        taken into account.

        Class properties:
            __limits (tuple[float]): a set of max flats' specific areas;
            each value is calculated empirically for each room count
            __expiration (timedelta): max offers' expiration period; too
            'old' offers shouldn't be taken into account
        """
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

    _shaft_class = _Shaft
