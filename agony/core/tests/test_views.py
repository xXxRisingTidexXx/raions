import logging
from datetime import date
from decimal import Decimal
from django.contrib.gis.geos import Point
from rest_framework.test import APITestCase
from core.models import User, Flat, Geolocation, Detail


class SummaryViewTestCase(APITestCase):
    def setUp(self) -> None:
        logging.disable(logging.CRITICAL)

    def test_get(self):
        flats = (
            Flat.objects.create(
                url='url1', avatar='ava1', published=date(2019, 4, 15),
                geolocation=Geolocation.objects.create(point=Point(34.086782, 52.6523401), locality='Ass'),
                price=Decimal(45000), rate=Decimal(900), area=50, rooms=2, floor=5, total_floor=9
            ),
            Flat.objects.create(
                url='url2', avatar='ava2', published=date(2019, 2, 5), geolocation=Geolocation.objects.create(
                    point=Point(31.0876, 45.209872), locality='New-York City', state='New-York'
                ), price=Decimal(66000), rate=Decimal(2000), area=33, rooms=1, floor=15, total_floor=16
            ),
            Flat.objects.create(
                url='url3', published=date(2019, 5, 7),
                geolocation=Geolocation.objects.create(point=Point(35.089, 49.13021), locality='Pussy'),
                price=Decimal(20000), rate=Decimal(500), area=40, living_area=25.8, kitchen_area=5,
                rooms=1, floor=2, total_floor=5, ceiling_height=2.7
            )
        )
        flats[1].details.add(Detail.objects.filter(value='1 bedroom')[0])
        self.assertEqual(self.client.get('/summary/porn/').status_code, 404)
        self.assertEqual(self.client.get('/sumary/').status_code, 404)
        self.assertEqual(self.client.get('/summary/').data, {'total_flats': 3})


class AuthorizedView(APITestCase):
    def setUp(self):
        self._user = User.objects.create(email='estimo@gmail.com')
        self._user.set_password('EstimoTop2019')
        self._user.save()
        jwt = self.client.post(
            '/auth/', {'email': 'estimo@gmail.com', 'password': 'EstimoTop2019'}
        ).data['token']
        self.client.credentials(HTTP_AUTHORIZATION=f'JWT {jwt}')
        logging.disable(logging.CRITICAL)


class SavedViewTestCase(AuthorizedView):
    def test_get(self):
        flats = (
            Flat.objects.create(
                url='url1', avatar='ava1', published=date(2019, 4, 15),
                geolocation=Geolocation.objects.create(point=Point(34.086782, 52.6523401), locality='Хуйомайо'),
                price=Decimal(45000), rate=Decimal(900), area=50, rooms=2, floor=5, total_floor=9
            ),
            Flat.objects.create(
                url='url2', avatar='ava2', published=date(2019, 2, 5), geolocation=Geolocation.objects.create(
                    point=Point(31.0876, 45.209872), locality='Великі Хуї', state='Черкаська область'
                ), price=Decimal(66000), rate=Decimal(2000), area=33, rooms=1, floor=15, total_floor=16
            ),
            Flat.objects.create(
                url='url3', published=date(2019, 5, 7),
                geolocation=Geolocation.objects.create(point=Point(35.089, 49.13021), locality='Козятин'),
                price=Decimal(20000), rate=Decimal(500), area=40, living_area=25.8, kitchen_area=5,
                rooms=1, floor=2, total_floor=5, ceiling_height=2.7
            )
        )
        flats[1].details.add(Detail.objects.filter(value='1 bedroom')[0])
        self._user.saved_flats.add(flats[0])
        self._user.saved_flats.add(flats[1])
        expected = {
            'saved_flats': [
                {
                    'id': flats[0].id,
                    'url': 'url1',
                    'avatar': 'ava1',
                    'geolocation': {
                        'type': 'Feature',
                        'geometry': {'type': 'Point', 'coordinates': [34.086782, 52.6523401]},
                        'properties': {
                            'state': None, 'locality': 'Хуйомайо', 'county': None,
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
                    'details': []
                },
                {
                    'id': flats[1].id,
                    'url': 'url2',
                    'avatar': 'ava2',
                    'geolocation': {
                        'type': 'Feature',
                        'geometry': {'type': 'Point', 'coordinates': [31.0876, 45.209872]},
                        'properties': {
                            'state': 'Черкаська область', 'locality': 'Великі Хуї', 'county': None,
                            'neighbourhood': None, 'road': None, 'house_number': None
                        }
                    },
                    'price': '66000.00',
                    'rate': '2000.00',
                    'area': 33,
                    'living_area': None,
                    'kitchen_area': None,
                    'rooms': 1,
                    'floor': 15,
                    'total_floor': 16,
                    'ceiling_height': None,
                    'details': [
                        {'feature': 'bedrooms', 'value': '1 bedroom', 'group': 'interior'}
                    ]
                }
            ]
        }
        response = self.client.get('/saved/')
        self.assertEqual(response.data, expected)
        self.assertEqual(response.status_code, 200)
        self._user.saved_flats.remove()

    def test_patch(self):
        flat = Flat.objects.create(
            url='url1', avatar='ava1', published=date(2019, 4, 15),
            geolocation=Geolocation.objects.create(point=Point(34.086782, 52.6523401), locality='Хуйомайо'),
            price=Decimal(45000), rate=Decimal(900), area=50, rooms=2, floor=5, total_floor=9
        )
        self.assertEqual(self.client.patch('/saved/dick/-1/').status_code, 404)
        self.assertEqual(self.client.patch(f'/saved/dick/{flat.id}/').status_code, 404)
        self.assertEqual(self.client.patch('/saved/dick/').status_code, 404)
        self.assertEqual(self.client.patch('/saved/flats/').status_code, 404)
        self.assertEqual(self.client.patch('/saved/flats/-1/').status_code, 404)
        self.assertEqual(self.client.patch(f'/saved/flats/{flat.id}/').status_code, 200)

    def test_delete(self):
        flat = Flat.objects.create(
            url='url1', avatar='ava1', published=date(2019, 4, 15),
            geolocation=Geolocation.objects.create(point=Point(34.086782, 52.6523401), locality='Хуйомайо'),
            price=Decimal(45000), rate=Decimal(900), area=50, rooms=2, floor=5, total_floor=9
        )
        self._user.saved_flats.add(flat)
        self.assertEqual(self.client.delete('/saved/dick/-1/').status_code, 404)
        self.assertEqual(self.client.delete(f'/saved/dick/{flat.id}/').status_code, 404)
        self.assertEqual(self.client.delete('/saved/dick/').status_code, 404)
        self.assertEqual(self.client.delete('/saved/flats/').status_code, 404)
        self.assertEqual(self.client.delete('/saved/flats/-1/').status_code, 404)
        self.assertEqual(self.client.delete(f'/saved/flats/{flat.id}/').status_code, 200)
        self.assertEqual(self.client.delete(f'/saved/flats/{flat.id}/').status_code, 200)


class GeolocationAutocompleteViewTestCase(AuthorizedView):
    def test_get(self):
        Geolocation.objects.create(point=Point(1, 1), state='Greece', locality='Characters', county='Io')
        Geolocation.objects.create(point=Point(1.34, 1.311), state='Greece', locality='Myths')
        Geolocation.objects.create(point=Point(-1.28340, 2.0032), state='Greece', locality='Legends')
        Geolocation.objects.create(point=Point(1.77765, -1.9), state='Greece', county='Vine')
        Geolocation.objects.create(point=Point(-0.108, -2.1101), state='Greece', locality='Characters', county='Zeus')
        Geolocation.objects.create(point=Point(0.02, 1.003), state='Greece', locality='Cities', county='Athens')
        Geolocation.objects.create(point=Point(-5.2, -2.221), state='Greece', locality='Cities', county='Sparta')
        Geolocation.objects.create(point=Point(2.082, -2.005), state='Greece', locality='Cities', county='Knossos')
        Geolocation.objects.create(point=Point(18.4, 23.4), state='Germany', locality='Cities', county='Munich')
        Geolocation.objects.create(point=Point(14.78, 28.135), state='Germany', locality='Cities', county='Berlin')
        Geolocation.objects.create(point=Point(-18.34, 17), state='France', locality='Bordeaux', county='Vine')
        Geolocation.objects.create(point=Point(38.34, 45.751), state='Germany', locality='Myths')
        Geolocation.objects.create(point=Point(31.4, 42), state='Germany', locality='Legends')
        Geolocation.objects.create(point=Point(33.309, 44.712), state='Germany', locality='Leg')
        cases = (
            (
                {'state': 'Foo', 'county': 'Bar'}, []
            ),
            (
                {'state': 'Greeces'}, []
            ),
            (
                {'state': 'Russia', 'locality': 'cities', 'county': 'moScOw'}, []
            ),
            (
                {'county': 'vin'},
                [
                    {'state': 'France', 'locality': 'Bordeaux', 'county': 'Vine'},
                    {'state': 'Greece', 'locality': None, 'county': 'Vine'}
                ]
            ),
            (
                {'locality': 'chaR', 'county': 'ze'},
                [{'state': 'Greece', 'locality': 'Characters', 'county': 'Zeus'}]
            ),
            (
                {'locality': 'leg'},
                [
                    {'state': 'Germany', 'locality': 'Leg', 'county': None},
                    {'state': 'Germany', 'locality': 'Legends', 'county': None},
                    {'state': 'Greece', 'locality': 'Legends', 'county': None}
                ]
            ),
            (
                {'state': 'Gre', 'locality': 'ci'},
                [
                    {'state': 'Greece', 'locality': 'Cities', 'county': 'Athens'},
                    {'state': 'Greece', 'locality': 'Cities', 'county': 'Knossos'},
                    {'state': 'Greece', 'locality': 'Cities', 'county': 'Sparta'}
                ]
            ),
            (
                {'state': 'ger', 'locality': 'ci', 'county': 'Mun'},
                [{'state': 'Germany', 'locality': 'Cities', 'county': 'Munich'}]
            )
        )
        for case in cases:
            self.assertEqual(self.client.get('/geolocation-autocomplete/', case[0]).data, case[1])


class DetailAutocompleteViewTestCase(AuthorizedView):
    def test_get(self):
        cases = (
            (
                {'value': 'fooo'}, set()
            ),
            (
                {'value': '15 bedrooms'}, set()
            ),
            (
                {'value': '1'}, {'1 passenger elevator', '1 bedroom'}
            ),
            (
                {'value': 'br'}, {'brick'}
            ),
            (
                {'value': 'ink'}, {'inkerman stone'}
            ),
            (
                {'value': 'AdJacEnt '},
                {
                    'adjacent bathrooms',
                    'adjacent planning',
                    'adjacent through planning'
                }
            ),
            (
                {'value': 'adjac'},
                {
                    'adjacent bathrooms',
                    'adjacent planning',
                    'adjacent through planning',
                    'adjacent-separate planning'
                }
            ),
            (
                {'value': 'metal'},
                {
                    'metal door', 'metal double door', 'metal-plastic door', 'metal-plastic windows'
                }
            ),
            (
                {'value': 'metaL-PlasTic'},
                {
                    'metal-plastic door',
                    'metal-plastic windows'
                }
            ),
            (
                {'value': 'mono'},
                {
                    'monolith',
                    'monolithic frame',
                    'monolithic reinforced concrete',
                    'monolithic brick',
                    'monolithic block'
                }
            )
        )
        for case in cases:
            json = self.client.get('/detail-autocomplete/', case[0]).data
            self.assertTrue(isinstance(json, list))
            self.assertEqual(set(json), case[1])


class LookupViewTestCase(AuthorizedView):
    def test_post(self):
        flats = (
            Flat.objects.create(
                url='url1', avatar='ava1', published=date(2019, 4, 15),
                geolocation=Geolocation.objects.create(point=Point(34.086782, 52.6523401), locality='Хуйомайо'),
                price=Decimal(45000), rate=Decimal(900), area=50, rooms=2, floor=5, total_floor=9
            ),
            Flat.objects.create(
                url='url2', avatar='ava2', published=date(2019, 4, 15), geolocation=Geolocation.objects.create(
                    point=Point(31.0876, 45.209872), locality='Великі Хуї', state='Черкаська область'
                ), price=Decimal(66000), rate=Decimal(2000), area=33, rooms=1, floor=15, total_floor=16
            ),
            Flat.objects.create(
                url='url3', published=date(2019, 5, 7),
                geolocation=Geolocation.objects.create(point=Point(35.089, 49.13021), locality='Козятин'),
                price=Decimal(20000), rate=Decimal(500), area=40, living_area=25.8, kitchen_area=5,
                rooms=1, floor=2, total_floor=5, ceiling_height=2.7
            ),
            Flat.objects.create(
                url='url4', published=date(2019, 3, 13),
                geolocation=Geolocation.objects.create(point=Point(44.223, 48.216), locality='Пиздоград'),
                price=Decimal(33000), rate=Decimal(600), area=55, living_area=39, kitchen_area=14,
                rooms=2, floor=15, total_floor=21,
            ),
            Flat.objects.create(
                url='url5', published=date(2019, 3, 14),
                geolocation=Geolocation.objects.filter(point=Point(44.223, 48.216)).first(),
                price=Decimal(31200), rate=Decimal(600), area=52, living_area=33, kitchen_area=13.3,
                rooms=2, floor=12, total_floor=21,
            )
        )
        details = (
            Detail.objects.filter(value='adjacent bathrooms')[0],
            Detail.objects.filter(value='separate bathrooms')[0],
            Detail.objects.filter(value='brick')[0],
            Detail.objects.filter(value='monolith')[0],
            Detail.objects.filter(value='monolithic frame')[0],
            Detail.objects.filter(value='monolithic reinforced concrete')[0],
            Detail.objects.filter(value='inkerman stone')[0],
            Detail.objects.filter(value='panel')[0],
            Detail.objects.filter(value='1 passenger elevator')[0],
            Detail.objects.filter(value='2 bedrooms')[0],
            Detail.objects.filter(value='metal double door')[0],
            Detail.objects.filter(value='metal door')[0],
            Detail.objects.filter(value='metal-plastic door')[0],
            Detail.objects.filter(value='adjacent planning')[0],
            Detail.objects.filter(value='metal-plastic windows')[0],
            Detail.objects.filter(value='internal insulation')[0]
        )
        flats[0].details.add(details[0], details[2], details[8], details[14])
        flats[1].details.add(details[1], details[6])
        flats[2].details.add(details[9], details[12], details[15])
        flats[4].details.add(details[6], details[11], details[13], details[14])
        cases = (
            (
                {'rooms_to': 1},
                [
                    {
                        'id': flats[2].id,
                        'url': 'url3',
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
                            {'feature': 'warming', 'value': 'internal insulation', 'group': 'supplies'},
                            {'feature': 'door_type', 'value': 'metal-plastic door', 'group': 'interior'},
                            {'feature': 'bedrooms', 'value': '2 bedrooms', 'group': 'interior'}
                        ]
                    },
                    {
                        'id': flats[1].id,
                        'url': 'url2',
                        'avatar': 'ava2',
                        'geolocation': {
                            'type': 'Feature',
                            'geometry': {'type': 'Point', 'coordinates': [31.0876, 45.209872]},
                            'properties': {
                                'state': 'Черкаська область', 'locality': 'Великі Хуї', 'county': None,
                                'neighbourhood': None, 'road': None, 'house_number': None
                            }
                        },
                        'price': '66000.00',
                        'rate': '2000.00',
                        'area': 33,
                        'living_area': None,
                        'kitchen_area': None,
                        'rooms': 1,
                        'floor': 15,
                        'total_floor': 16,
                        'ceiling_height': None,
                        'details': [
                            {'feature': 'wall_type', 'value': 'inkerman stone', 'group': 'building'},
                            {'feature': 'bathrooms', 'value': 'separate bathrooms', 'group': 'supplies'}
                        ]
                    }
                ]
            ),
            (
                {'rooms_from': 3}, []
            ),
            (
                {'rooms_from': 2, 'ceiling_height_from': 3}, []
            ),
            (
                {'area_from': 45, 'area_to': 51},
                [
                    {
                        'id': flats[0].id,
                        'url': 'url1',
                        'avatar': 'ava1',
                        'geolocation': {
                            'type': 'Feature',
                            'geometry': {'type': 'Point', 'coordinates': [34.086782, 52.6523401]},
                            'properties': {
                                'state': None, 'locality': 'Хуйомайо', 'county': None,
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
                        'details': [
                            {
                                'feature': 'wall_type',
                                'value': 'brick',
                                'group': 'building'
                            },
                            {
                                'feature': 'window_type',
                                'value': 'metal-plastic windows',
                                'group': 'interior'
                            },
                            {
                                'feature': 'bathrooms',
                                'value': 'adjacent bathrooms',
                                'group': 'supplies'
                            },
                            {
                                'feature': 'passenger_elevators',
                                'value': '1 passenger elevator',
                                'group': 'building'
                            }
                        ]
                    }
                ]
            ),
            (
                {},
                [
                    {
                        'id': flats[2].id,
                        'url': 'url3',
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
                            {'feature': 'warming', 'value': 'internal insulation', 'group': 'supplies'},
                            {'feature': 'door_type', 'value': 'metal-plastic door', 'group': 'interior'},
                            {'feature': 'bedrooms', 'value': '2 bedrooms', 'group': 'interior'}
                        ]
                    },
                    {
                        'id': flats[0].id,
                        'url': 'url1',
                        'avatar': 'ava1',
                        'geolocation': {
                            'type': 'Feature',
                            'geometry': {'type': 'Point', 'coordinates': [34.086782, 52.6523401]},
                            'properties': {
                                'state': None, 'locality': 'Хуйомайо', 'county': None,
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
                        'details': [
                            {
                                'feature': 'wall_type',
                                'value': 'brick',
                                'group': 'building'
                            },
                            {
                                'feature': 'window_type',
                                'value': 'metal-plastic windows',
                                'group': 'interior'
                            },
                            {
                                'feature': 'bathrooms',
                                'value': 'adjacent bathrooms',
                                'group': 'supplies'
                            },
                            {
                                'feature': 'passenger_elevators',
                                'value': '1 passenger elevator',
                                'group': 'building'
                            }
                        ]
                    },
                    {
                        'id': flats[1].id,
                        'url': 'url2',
                        'avatar': 'ava2',
                        'geolocation': {
                            'type': 'Feature',
                            'geometry': {'type': 'Point', 'coordinates': [31.0876, 45.209872]},
                            'properties': {
                                'state': 'Черкаська область', 'locality': 'Великі Хуї', 'county': None,
                                'neighbourhood': None, 'road': None, 'house_number': None
                            }
                        },
                        'price': '66000.00',
                        'rate': '2000.00',
                        'area': 33,
                        'living_area': None,
                        'kitchen_area': None,
                        'rooms': 1,
                        'floor': 15,
                        'total_floor': 16,
                        'ceiling_height': None,
                        'details': [
                            {'feature': 'wall_type', 'value': 'inkerman stone', 'group': 'building'},
                            {'feature': 'bathrooms', 'value': 'separate bathrooms', 'group': 'supplies'}
                        ]
                    },
                    {
                        'id': flats[4].id,
                        'url': 'url5',
                        'avatar': None,
                        'geolocation': {
                            'type': 'Feature',
                            'geometry': {'type': 'Point', 'coordinates': [44.223, 48.216]},
                            'properties': {
                                'state': None, 'locality': 'Пиздоград', 'county': None,
                                'neighbourhood': None, 'road': None, 'house_number': None
                            }
                        },
                        'price': '31200.00',
                        'rate': '600.00',
                        'area': 52,
                        'living_area': 33,
                        'kitchen_area': 13.3,
                        'rooms': 2,
                        'floor': 12,
                        'total_floor': 21,
                        'ceiling_height': None,
                        'details': [
                            {
                                'feature': 'planning',
                                'value': 'adjacent planning',
                                'group': 'interior'
                            },
                            {
                                'feature': 'wall_type',
                                'value': 'inkerman stone',
                                'group': 'building'
                            },
                            {
                                'feature': 'door_type',
                                'value': 'metal door',
                                'group': 'interior'
                            },
                            {
                                'feature': 'window_type',
                                'value': 'metal-plastic windows',
                                'group': 'interior'
                            }
                        ]
                    },
                    {
                        'id': flats[3].id,
                        'url': 'url4',
                        'avatar': None,
                        'geolocation': {
                            'type': 'Feature',
                            'geometry': {'type': 'Point', 'coordinates': [44.223, 48.216]},
                            'properties': {
                                'state': None, 'locality': 'Пиздоград', 'county': None,
                                'neighbourhood': None, 'road': None, 'house_number': None
                            }
                        },
                        'price': '33000.00',
                        'rate': '600.00',
                        'area': 55,
                        'living_area': 39,
                        'kitchen_area': 14,
                        'rooms': 2,
                        'floor': 15,
                        'total_floor': 21,
                        'ceiling_height': None,
                        'details': []
                    }
                ]
            ),
            (
                {'details': ['metal-plastic windows', 'adjacent planning']},
                [
                    {
                        'id': flats[4].id,
                        'url': 'url5',
                        'avatar': None,
                        'geolocation': {
                            'type': 'Feature',
                            'geometry': {'type': 'Point', 'coordinates': [44.223, 48.216]},
                            'properties': {
                                'state': None, 'locality': 'Пиздоград', 'county': None,
                                'neighbourhood': None, 'road': None, 'house_number': None
                            }
                        },
                        'price': '31200.00',
                        'rate': '600.00',
                        'area': 52,
                        'living_area': 33,
                        'kitchen_area': 13.3,
                        'rooms': 2,
                        'floor': 12,
                        'total_floor': 21,
                        'ceiling_height': None,
                        'details': [
                            {
                                'feature': 'planning',
                                'value': 'adjacent planning',
                                'group': 'interior'
                            },
                            {
                                'feature': 'wall_type',
                                'value': 'inkerman stone',
                                'group': 'building'
                            },
                            {
                                'feature': 'door_type',
                                'value': 'metal door',
                                'group': 'interior'
                            },
                            {
                                'feature': 'window_type',
                                'value': 'metal-plastic windows',
                                'group': 'interior'
                            }
                        ]
                    }
                ]
            ),
            (
                {'details': ['adjacent planning', 'brick', '1 bedroom']}, []
            ),
            (
                {'details': ['aerocrete']}, []
            ),
            (
                {'ceiling_height_from': 2.8, 'details': ['aerocrete']}, []
            ),
            (
                {'area_from': 50, 'details': ['metal-plastic windows']},
                [
                    {
                        'id': flats[0].id,
                        'url': 'url1',
                        'avatar': 'ava1',
                        'geolocation': {
                            'type': 'Feature',
                            'geometry': {'type': 'Point', 'coordinates': [34.086782, 52.6523401]},
                            'properties': {
                                'state': None, 'locality': 'Хуйомайо', 'county': None,
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
                        'details': [
                            {
                                'feature': 'wall_type',
                                'value': 'brick',
                                'group': 'building'
                            },
                            {
                                'feature': 'window_type',
                                'value': 'metal-plastic windows',
                                'group': 'interior'
                            },
                            {
                                'feature': 'bathrooms',
                                'value': 'adjacent bathrooms',
                                'group': 'supplies'
                            },
                            {
                                'feature': 'passenger_elevators',
                                'value': '1 passenger elevator',
                                'group': 'building'
                            }
                        ]
                    },
                    {
                        'id': flats[4].id,
                        'url': 'url5',
                        'avatar': None,
                        'geolocation': {
                            'type': 'Feature',
                            'geometry': {'type': 'Point', 'coordinates': [44.223, 48.216]},
                            'properties': {
                                'state': None, 'locality': 'Пиздоград', 'county': None,
                                'neighbourhood': None, 'road': None, 'house_number': None
                            }
                        },
                        'price': '31200.00',
                        'rate': '600.00',
                        'area': 52,
                        'living_area': 33,
                        'kitchen_area': 13.3,
                        'rooms': 2,
                        'floor': 12,
                        'total_floor': 21,
                        'ceiling_height': None,
                        'details': [
                            {
                                'feature': 'planning',
                                'value': 'adjacent planning',
                                'group': 'interior'
                            },
                            {
                                'feature': 'wall_type',
                                'value': 'inkerman stone',
                                'group': 'building'
                            },
                            {
                                'feature': 'door_type',
                                'value': 'metal door',
                                'group': 'interior'
                            },
                            {
                                'feature': 'window_type',
                                'value': 'metal-plastic windows',
                                'group': 'interior'
                            }
                        ]
                    }
                ]
            ),
            (
                {'living_area_to': 35, 'kitchen_area_from': 12},
                [
                    {
                        'id': flats[4].id,
                        'url': 'url5',
                        'avatar': None,
                        'geolocation': {
                            'type': 'Feature',
                            'geometry': {'type': 'Point', 'coordinates': [44.223, 48.216]},
                            'properties': {
                                'state': None, 'locality': 'Пиздоград', 'county': None,
                                'neighbourhood': None, 'road': None, 'house_number': None
                            }
                        },
                        'price': '31200.00',
                        'rate': '600.00',
                        'area': 52,
                        'living_area': 33,
                        'kitchen_area': 13.3,
                        'rooms': 2,
                        'floor': 12,
                        'total_floor': 21,
                        'ceiling_height': None,
                        'details': [
                            {
                                'feature': 'planning',
                                'value': 'adjacent planning',
                                'group': 'interior'
                            },
                            {
                                'feature': 'wall_type',
                                'value': 'inkerman stone',
                                'group': 'building'
                            },
                            {
                                'feature': 'door_type',
                                'value': 'metal door',
                                'group': 'interior'
                            },
                            {
                                'feature': 'window_type',
                                'value': 'metal-plastic windows',
                                'group': 'interior'
                            }
                        ]
                    }
                ]
            ),
            (
                {'kitchen_area_to': 17, 'details': ['internal insulation']},
                [
                    {
                        'id': flats[2].id,
                        'url': 'url3',
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
                            {'feature': 'warming', 'value': 'internal insulation', 'group': 'supplies'},
                            {'feature': 'door_type', 'value': 'metal-plastic door', 'group': 'interior'},
                            {'feature': 'bedrooms', 'value': '2 bedrooms', 'group': 'interior'}
                        ]
                    }
                ]
            ),
            (
                {'total_floor_from': 18, 'order_by': 'area'},
                [
                    {
                        'id': flats[4].id,
                        'url': 'url5',
                        'avatar': None,
                        'geolocation': {
                            'type': 'Feature',
                            'geometry': {'type': 'Point', 'coordinates': [44.223, 48.216]},
                            'properties': {
                                'state': None, 'locality': 'Пиздоград', 'county': None,
                                'neighbourhood': None, 'road': None, 'house_number': None
                            }
                        },
                        'price': '31200.00',
                        'rate': '600.00',
                        'area': 52,
                        'living_area': 33,
                        'kitchen_area': 13.3,
                        'rooms': 2,
                        'floor': 12,
                        'total_floor': 21,
                        'ceiling_height': None,
                        'details': [
                            {
                                'feature': 'planning',
                                'value': 'adjacent planning',
                                'group': 'interior'
                            },
                            {
                                'feature': 'wall_type',
                                'value': 'inkerman stone',
                                'group': 'building'
                            },
                            {
                                'feature': 'door_type',
                                'value': 'metal door',
                                'group': 'interior'
                            },
                            {
                                'feature': 'window_type',
                                'value': 'metal-plastic windows',
                                'group': 'interior'
                            }
                        ]
                    },
                    {
                        'id': flats[3].id,
                        'url': 'url4',
                        'avatar': None,
                        'geolocation': {
                            'type': 'Feature',
                            'geometry': {'type': 'Point', 'coordinates': [44.223, 48.216]},
                            'properties': {
                                'state': None, 'locality': 'Пиздоград', 'county': None,
                                'neighbourhood': None, 'road': None, 'house_number': None
                            }
                        },
                        'price': '33000.00',
                        'rate': '600.00',
                        'area': 55,
                        'living_area': 39,
                        'kitchen_area': 14,
                        'rooms': 2,
                        'floor': 15,
                        'total_floor': 21,
                        'ceiling_height': None,
                        'details': []
                    }
                ]
            ),
            (
                {'rooms_from': 2, 'order_by': '-price'},
                [
                    {
                        'id': flats[0].id,
                        'url': 'url1',
                        'avatar': 'ava1',
                        'geolocation': {
                            'type': 'Feature',
                            'geometry': {'type': 'Point', 'coordinates': [34.086782, 52.6523401]},
                            'properties': {
                                'state': None, 'locality': 'Хуйомайо', 'county': None,
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
                        'details': [
                            {
                                'feature': 'wall_type',
                                'value': 'brick',
                                'group': 'building'
                            },
                            {
                                'feature': 'window_type',
                                'value': 'metal-plastic windows',
                                'group': 'interior'
                            },
                            {
                                'feature': 'bathrooms',
                                'value': 'adjacent bathrooms',
                                'group': 'supplies'
                            },
                            {
                                'feature': 'passenger_elevators',
                                'value': '1 passenger elevator',
                                'group': 'building'
                            }
                        ]
                    },
                    {
                        'id': flats[3].id,
                        'url': 'url4',
                        'avatar': None,
                        'geolocation': {
                            'type': 'Feature',
                            'geometry': {'type': 'Point', 'coordinates': [44.223, 48.216]},
                            'properties': {
                                'state': None, 'locality': 'Пиздоград', 'county': None,
                                'neighbourhood': None, 'road': None, 'house_number': None
                            }
                        },
                        'price': '33000.00',
                        'rate': '600.00',
                        'area': 55,
                        'living_area': 39,
                        'kitchen_area': 14,
                        'rooms': 2,
                        'floor': 15,
                        'total_floor': 21,
                        'ceiling_height': None,
                        'details': []
                    },
                    {
                        'id': flats[4].id,
                        'url': 'url5',
                        'avatar': None,
                        'geolocation': {
                            'type': 'Feature',
                            'geometry': {'type': 'Point', 'coordinates': [44.223, 48.216]},
                            'properties': {
                                'state': None, 'locality': 'Пиздоград', 'county': None,
                                'neighbourhood': None, 'road': None, 'house_number': None
                            }
                        },
                        'price': '31200.00',
                        'rate': '600.00',
                        'area': 52,
                        'living_area': 33,
                        'kitchen_area': 13.3,
                        'rooms': 2,
                        'floor': 12,
                        'total_floor': 21,
                        'ceiling_height': None,
                        'details': [
                            {
                                'feature': 'planning',
                                'value': 'adjacent planning',
                                'group': 'interior'
                            },
                            {
                                'feature': 'wall_type',
                                'value': 'inkerman stone',
                                'group': 'building'
                            },
                            {
                                'feature': 'door_type',
                                'value': 'metal door',
                                'group': 'interior'
                            },
                            {
                                'feature': 'window_type',
                                'value': 'metal-plastic windows',
                                'group': 'interior'
                            }
                        ]
                    }
                ]
            ),
            (
                {'details': ['metal-plastic windows'], 'order_by': 'fucking shit'},
                [
                    {
                        'id': flats[0].id,
                        'url': 'url1',
                        'avatar': 'ava1',
                        'geolocation': {
                            'type': 'Feature',
                            'geometry': {'type': 'Point', 'coordinates': [34.086782, 52.6523401]},
                            'properties': {
                                'state': None, 'locality': 'Хуйомайо', 'county': None,
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
                        'details': [
                            {
                                'feature': 'wall_type',
                                'value': 'brick',
                                'group': 'building'
                            },
                            {
                                'feature': 'window_type',
                                'value': 'metal-plastic windows',
                                'group': 'interior'
                            },
                            {
                                'feature': 'bathrooms',
                                'value': 'adjacent bathrooms',
                                'group': 'supplies'
                            },
                            {
                                'feature': 'passenger_elevators',
                                'value': '1 passenger elevator',
                                'group': 'building'
                            }
                        ]
                    },
                    {
                        'id': flats[4].id,
                        'url': 'url5',
                        'avatar': None,
                        'geolocation': {
                            'type': 'Feature',
                            'geometry': {'type': 'Point', 'coordinates': [44.223, 48.216]},
                            'properties': {
                                'state': None, 'locality': 'Пиздоград', 'county': None,
                                'neighbourhood': None, 'road': None, 'house_number': None
                            }
                        },
                        'price': '31200.00',
                        'rate': '600.00',
                        'area': 52,
                        'living_area': 33,
                        'kitchen_area': 13.3,
                        'rooms': 2,
                        'floor': 12,
                        'total_floor': 21,
                        'ceiling_height': None,
                        'details': [
                            {
                                'feature': 'planning',
                                'value': 'adjacent planning',
                                'group': 'interior'
                            },
                            {
                                'feature': 'wall_type',
                                'value': 'inkerman stone',
                                'group': 'building'
                            },
                            {
                                'feature': 'door_type',
                                'value': 'metal door',
                                'group': 'interior'
                            },
                            {
                                'feature': 'window_type',
                                'value': 'metal-plastic windows',
                                'group': 'interior'
                            }
                        ]
                    }
                ]
            )
        )
        self.assertEqual(self.client.post('/lookup/').status_code, 404)
        self.assertEqual(self.client.post('/lookup/bar/').status_code, 404)
        self.assertEqual(self.client.post('/lookup/bar/', {'rooms_to': 4}).status_code, 404)
        for case in cases:
            self.assertEqual(self.client.post('/lookup/flats/', case[0]).data, case[1])
