"""
This module describes *reapy*'s DTOs

Structs are simple classes without any behaviour (like C++ structs) whose
single task is to transfer the data in a convenient way with the dot-notation.
"""
from datetime import date
from decimal import Decimal
from typing import List, Dict, Any
from attr import attrs, attrib


@attrs(slots=True)
class Flat(object):
    """
    A simple flat's object comprehension

    Instance properties:
        url: original offer's url
        avatar: offer's main image url
        published: offer's publication day
        geolocation: holds flat's location (lon/lat) and literal description
        price: offer's price (in USD)
        rate: price of a 1 square meter of the flat (in USD)
        currency: currency's symbol (generally - $ or USD)
        area: flat's area (in square meters)
        living_area: flat's living_area (in square meters)
        kitchen_area: flat's kitchen_area (in square meters)
        rooms: flat's room count
        floor: flat's floor (may be -1 if it's underground)
        total_floor: flat's house total_floor
        ceiling_height: flat's ceiling_height (in meters)
        details: details' list (flat's literal description)
    """
    url = attrib(default=None, type=str)
    avatar = attrib(default=None, type=str)
    published = attrib(default=None, type=date)
    geolocation = attrib(default=None, type=Dict[str, Any])
    price = attrib(default=None, type=Decimal)
    rate = attrib(default=None, type=Decimal)
    currency = attrib(default='$', type=str)
    area = attrib(default=None, type=float)
    living_area = attrib(default=None, type=float)
    kitchen_area = attrib(default=None, type=float)
    rooms = attrib(default=None, type=int)
    floor = attrib(default=None, type=int)
    total_floor = attrib(default=None, type=int)
    ceiling_height = attrib(default=None, type=float)
    details = attrib(default=[], type=List[str])
