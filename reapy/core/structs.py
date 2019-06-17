from datetime import date
from decimal import Decimal
from attr import attrs, attrib


@attrs(slots=True)
class Flat(object):
    url = attrib(default=None, type=str)
    avatar = attrib(default=None, type=str)
    published = attrib(default=None, type=date)
    geolocation = attrib(default=None, type=dict)
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
    details = attrib(default=[], type=list)
