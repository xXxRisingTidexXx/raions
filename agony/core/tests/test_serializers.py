from datetime import date
from decimal import Decimal
from django.contrib.gis.geos import Point
from django.test import TestCase
from core.models import Geolocation, Flat, Detail
from core.serializers import GeolocationSerializer, FlatSerializer


class GeolocationSerializerTestCase(TestCase):
    def setUp(self):
        self.__geolocations = (
            Geolocation.objects.create(
                state='Харківська область', locality='Харків', county='Немишлянський район', point=Point(50, 51.3)
            ),
            Geolocation.objects.create(
                state=None, locality='Київ', county='Подільський район', point=Point(48, 51.1)
            )
        )

    def test_serialization(self):
        expected = (
            {
                'type': 'Feature',
                'geometry': {'type': 'Point', 'coordinates': [50, 51.3]},
                'properties': {
                    'state': 'Харківська область', 'locality': 'Харків', 'county': 'Немишлянський район',
                    'neighbourhood': None, 'road': None, 'house_number': None
                }
            },
            {
                'type': 'Feature',
                'geometry': {'type': 'Point', 'coordinates': [48, 51.1]},
                'properties': {
                    'state': None, 'locality': 'Київ', 'county': 'Подільський район',
                    'neighbourhood': None, 'road': None, 'house_number': None
                }
            }
        )
        for i in range(len(self.__geolocations)):
            self.assertEqual(GeolocationSerializer(self.__geolocations[i]).data, expected[i])


class FlatSerializerTestCase(TestCase):
    def setUp(self):
        self.__flats = (
            Flat.objects.create(
                url='url1', avatar='ava1', published=date(2019, 4, 15),
                geolocation=Geolocation.objects.create(point=Point(34.086782, 52.6523401), locality='Залупинськ'),
                price=Decimal(45000), rate=Decimal(900), area=50, rooms=2, floor=5, total_floor=9
            ),
            Flat.objects.create(
                url='url2', published=date(2019, 5, 7),
                geolocation=Geolocation.objects.create(point=Point(35.089, 49.13021), locality='Козятин'),
                price=Decimal(20000), rate=Decimal(500), area=40, living_area=25.8, kitchen_area=5,
                rooms=1, floor=2, total_floor=5, ceiling_height=2.7
            )
        )
        self.__flats[0].details.add(Detail.objects.filter(value='Цегла')[0])
        self.__flats[1].details.add(Detail.objects.filter(value='Моноліт')[0])
        self.__flats[1].details.add(Detail.objects.filter(value='2 санвузли')[0])

    def test_serialization(self):
        expected = (
            {
                'id': self.__flats[0].id,
                'url': 'url1',
                'avatar': 'ava1',
                'geolocation': {
                    'type': 'Feature',
                    'geometry': {'type': 'Point', 'coordinates': [34.086782, 52.6523401]},
                    'properties': {
                        'state': None, 'locality': 'Залупинськ', 'county': None,
                        'neighbourhood': None, 'road': None, 'house_number': None
                    }
                },
                'price': '45000.00',
                'rate': '900.00',
                'area': 50,
                'living_area': None,
                'kitchen_area': None,
                'rooms': 2,
                'floor': 5,
                'total_floor': 9,
                'ceiling_height': None,
                'details': [{'feature': 'wall_type', 'value': 'Цегла', 'group': 'building'}]
            },
            {
                'id': self.__flats[1].id,
                'url': 'url2',
                'avatar': None,
                'geolocation': {
                    'type': 'Feature',
                    'geometry': {'type': 'Point', 'coordinates': [35.089, 49.13021]},
                    'properties': {
                        'state': None, 'locality': 'Козятин', 'county': None,
                        'neighbourhood': None, 'road': None, 'house_number': None
                    }
                },
                'price': '20000.00',
                'rate': '500.00',
                'area': 40,
                'living_area': 25.8,
                'kitchen_area': 5,
                'rooms': 1,
                'floor': 2,
                'total_floor': 5,
                'ceiling_height': 2.7,
                'details': [
                    {'feature': 'wall_type', 'value': 'Моноліт', 'group': 'building'},
                    {'feature': 'bathrooms', 'value': '2 санвузли', 'group': 'supplies'}
                ]
            }
        )
        for i in range(len(self.__flats)):
            self.assertEqual(FlatSerializer(self.__flats[i]).data, expected[i])
