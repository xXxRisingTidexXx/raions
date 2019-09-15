from logging import disable, CRITICAL
from datetime import date
from decimal import Decimal
from django.contrib.gis.geos import Point
from rest_framework.test import APITestCase
from core.models import User, Flat, Geolocation, Detail


class SummaryViewTestCase(APITestCase):
    def setUp(self):
        disable(CRITICAL)

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
        flats[1].details.add(Detail.objects.filter(value='1 спальня')[0])
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
        disable(CRITICAL)


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
        flats[1].details.add(Detail.objects.filter(value='1 спальня')[0])
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
                        {'feature': 'bedrooms', 'value': '1 спальня', 'group': 'interior'}
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
                    {
                        'state': 'France',
                        'locality': 'Bordeaux',
                        'county': 'Vine',
                        'neighbourhood': None,
                        'road': None,
                        'house_number': None
                    },
                    {
                        'state': 'Greece',
                        'locality': None,
                        'county': 'Vine',
                        'neighbourhood': None,
                        'road': None,
                        'house_number': None
                    }
                ]
            ),
            (
                {'locality': 'chaR', 'county': 'ze'},
                [
                    {
                        'state': 'Greece',
                        'locality': 'Characters',
                        'county': 'Zeus',
                        'neighbourhood': None,
                        'road': None,
                        'house_number': None
                    }
                ]
            ),
            (
                {'locality': 'leg'},
                [
                    {
                        'state': 'Germany',
                        'locality': 'Leg',
                        'county': None,
                        'neighbourhood': None,
                        'road': None,
                        'house_number': None
                    },
                    {
                        'state': 'Germany',
                        'locality': 'Legends',
                        'county': None,
                        'neighbourhood': None,
                        'road': None,
                        'house_number': None
                    },
                    {
                        'state': 'Greece',
                        'locality': 'Legends',
                        'county': None,
                        'neighbourhood': None,
                        'road': None,
                        'house_number': None
                    }
                ]
            ),
            (
                {'state': 'Gre', 'locality': 'ci'},
                [
                    {
                        'state': 'Greece',
                        'locality': 'Cities',
                        'county': 'Athens',
                        'neighbourhood': None,
                        'road': None,
                        'house_number': None
                    },
                    {
                        'state': 'Greece',
                        'locality': 'Cities',
                        'county': 'Knossos',
                        'neighbourhood': None,
                        'road': None,
                        'house_number': None
                    },
                    {
                        'state': 'Greece',
                        'locality': 'Cities',
                        'county': 'Sparta',
                        'neighbourhood': None,
                        'road': None,
                        'house_number': None
                    }
                ]
            ),
            (
                {'state': 'ger', 'locality': 'ci', 'county': 'Mun'},
                [
                    {
                        'state': 'Germany',
                        'locality': 'Cities',
                        'county': 'Munich',
                        'neighbourhood': None,
                        'road': None,
                        'house_number': None
                    }
                ]
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
                {'value': '15 спалень'}, set()
            ),
            (
                {'value': '1'}, {'1 пасажирський ліфт', '1 спальня'}
            ),
            (
                {'value': ' цег'}, {'Цегла'}
            ),
            (
                {'value': ' іНк'}, {'Інкерманський камінь'}
            ),
            (
                {'value': ' СуміЖн   '},
                {
                    'Суміжний санвузол',
                    'Суміжне планування',
                    'Суміжно-роздільне планування',
                    'Суміжне, прохідне планування'
                }
            ),
            (
                {'value': ' метал '},
                {
                    'Металеві двері', 'Металеві подвійні двері',
                    'Металопластикові двері', 'Металопластикові вікна'
                }
            ),
            (
                {'value': ' метАлоПластиКоВі '},
                {'Металопластикові двері', 'Металопластикові вікна'}
            ),
            (
                {'value': '  Моно '},
                {
                    'Моноліт',
                    'Монолітно-каркасний',
                    'Монолітний залізобетон',
                    'Монолітно-цегляний',
                    'Монолітно-блоковий'
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
            ),
            Flat.objects.create(
                url='url6', published=date(2019, 1, 14),
                geolocation=Geolocation.objects.filter(point=Point(44.223, 48.216)).first(),
                price=Decimal(41600), rate=Decimal(800), area=67, living_area=47, kitchen_area=13.3,
                rooms=2, floor=8, total_floor=21, is_visible=False
            )
        )
        details = (
            Detail.objects.get(value='Суміжний санвузол'),
            Detail.objects.get(value='Роздільний санвузол'),
            Detail.objects.get(value='Цегла'),
            Detail.objects.get(value='Моноліт'),
            Detail.objects.get(value='Монолітно-каркасний'),
            Detail.objects.get(value='Монолітний залізобетон'),
            Detail.objects.get(value='Інкерманський камінь'),
            Detail.objects.get(value='Панель'),
            Detail.objects.get(value='1 пасажирський ліфт'),
            Detail.objects.get(value='2 спальні'),
            Detail.objects.get(value='Металеві подвійні двері'),
            Detail.objects.get(value='Металеві двері'),
            Detail.objects.get(value='Металопластикові двері'),
            Detail.objects.get(value='Суміжне планування'),
            Detail.objects.get(value='Металопластикові вікна'),
            Detail.objects.get(value='Внутрішнє утеплення')
        )
        flats[0].details.add(details[0], details[2], details[8], details[14])
        flats[1].details.add(details[1], details[6])
        flats[2].details.add(details[9], details[12], details[15])
        flats[4].details.add(details[6], details[11], details[13], details[14])
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
                            {'feature': 'warming', 'value': 'Внутрішнє утеплення', 'group': 'supplies'},
                            {'feature': 'door_type', 'value': 'Металопластикові двері', 'group': 'interior'},
                            {'feature': 'bedrooms', 'value': '2 спальні', 'group': 'interior'}
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
                            {'feature': 'wall_type', 'value': 'Інкерманський камінь', 'group': 'building'},
                            {'feature': 'bathrooms', 'value': 'Роздільний санвузол', 'group': 'supplies'}
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
                                'value': 'Цегла',
                                'group': 'building'
                            },
                            {
                                'feature': 'window_type',
                                'value': 'Металопластикові вікна',
                                'group': 'interior'
                            },
                            {
                                'feature': 'bathrooms',
                                'value': 'Суміжний санвузол',
                                'group': 'supplies'
                            },
                            {
                                'feature': 'passenger_elevators',
                                'value': '1 пасажирський ліфт',
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
                            {'feature': 'warming', 'value': 'Внутрішнє утеплення', 'group': 'supplies'},
                            {'feature': 'door_type', 'value': 'Металопластикові двері', 'group': 'interior'},
                            {'feature': 'bedrooms', 'value': '2 спальні', 'group': 'interior'}
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
                                'value': 'Цегла',
                                'group': 'building'
                            },
                            {
                                'feature': 'window_type',
                                'value': 'Металопластикові вікна',
                                'group': 'interior'
                            },
                            {
                                'feature': 'bathrooms',
                                'value': 'Суміжний санвузол',
                                'group': 'supplies'
                            },
                            {
                                'feature': 'passenger_elevators',
                                'value': '1 пасажирський ліфт',
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
                            {'feature': 'wall_type', 'value': 'Інкерманський камінь', 'group': 'building'},
                            {'feature': 'bathrooms', 'value': 'Роздільний санвузол', 'group': 'supplies'}
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
                                'value': 'Суміжне планування',
                                'group': 'interior'
                            },
                            {
                                'feature': 'wall_type',
                                'value': 'Інкерманський камінь',
                                'group': 'building'
                            },
                            {
                                'feature': 'door_type',
                                'value': 'Металеві двері',
                                'group': 'interior'
                            },
                            {
                                'feature': 'window_type',
                                'value': 'Металопластикові вікна',
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
                {'details': ['Металопластикові вікна', 'Суміжне планування']},
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
                                'value': 'Суміжне планування',
                                'group': 'interior'
                            },
                            {
                                'feature': 'wall_type',
                                'value': 'Інкерманський камінь',
                                'group': 'building'
                            },
                            {
                                'feature': 'door_type',
                                'value': 'Металеві двері',
                                'group': 'interior'
                            },
                            {
                                'feature': 'window_type',
                                'value': 'Металопластикові вікна',
                                'group': 'interior'
                            }
                        ]
                    }
                ]
            ),
            (
                {'details': ['Суміжне планування', 'Цегла', '1 спальня']}, []
            ),
            (
                {'details': ['Газоблок']}, []
            ),
            (
                {'ceiling_height_from': 2.8, 'details': ['Газо']}, []
            ),
            (
                {'area_from': 50, 'details': ['Металопластикові вікна']},
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
                                'value': 'Цегла',
                                'group': 'building'
                            },
                            {
                                'feature': 'window_type',
                                'value': 'Металопластикові вікна',
                                'group': 'interior'
                            },
                            {
                                'feature': 'bathrooms',
                                'value': 'Суміжний санвузол',
                                'group': 'supplies'
                            },
                            {
                                'feature': 'passenger_elevators',
                                'value': '1 пасажирський ліфт',
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
                                'value': 'Суміжне планування',
                                'group': 'interior'
                            },
                            {
                                'feature': 'wall_type',
                                'value': 'Інкерманський камінь',
                                'group': 'building'
                            },
                            {
                                'feature': 'door_type',
                                'value': 'Металеві двері',
                                'group': 'interior'
                            },
                            {
                                'feature': 'window_type',
                                'value': 'Металопластикові вікна',
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
                                'value': 'Суміжне планування',
                                'group': 'interior'
                            },
                            {
                                'feature': 'wall_type',
                                'value': 'Інкерманський камінь',
                                'group': 'building'
                            },
                            {
                                'feature': 'door_type',
                                'value': 'Металеві двері',
                                'group': 'interior'
                            },
                            {
                                'feature': 'window_type',
                                'value': 'Металопластикові вікна',
                                'group': 'interior'
                            }
                        ]
                    }
                ]
            ),
            (
                {'kitchen_area_to': 17, 'details': ['Внутрішнє утеплення']},
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
                            {'feature': 'warming', 'value': 'Внутрішнє утеплення', 'group': 'supplies'},
                            {'feature': 'door_type', 'value': 'Металопластикові двері', 'group': 'interior'},
                            {'feature': 'bedrooms', 'value': '2 спальні', 'group': 'interior'}
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
                                'value': 'Суміжне планування',
                                'group': 'interior'
                            },
                            {
                                'feature': 'wall_type',
                                'value': 'Інкерманський камінь',
                                'group': 'building'
                            },
                            {
                                'feature': 'door_type',
                                'value': 'Металеві двері',
                                'group': 'interior'
                            },
                            {
                                'feature': 'window_type',
                                'value': 'Металопластикові вікна',
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
                                'value': 'Цегла',
                                'group': 'building'
                            },
                            {
                                'feature': 'window_type',
                                'value': 'Металопластикові вікна',
                                'group': 'interior'
                            },
                            {
                                'feature': 'bathrooms',
                                'value': 'Суміжний санвузол',
                                'group': 'supplies'
                            },
                            {
                                'feature': 'passenger_elevators',
                                'value': '1 пасажирський ліфт',
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
                                'value': 'Суміжне планування',
                                'group': 'interior'
                            },
                            {
                                'feature': 'wall_type',
                                'value': 'Інкерманський камінь',
                                'group': 'building'
                            },
                            {
                                'feature': 'door_type',
                                'value': 'Металеві двері',
                                'group': 'interior'
                            },
                            {
                                'feature': 'window_type',
                                'value': 'Металопластикові вікна',
                                'group': 'interior'
                            }
                        ]
                    }
                ]
            ),
            (
                {'details': ['Металопластикові вікна'], 'order_by': 'fucking shit'},
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
                                'value': 'Цегла',
                                'group': 'building'
                            },
                            {
                                'feature': 'window_type',
                                'value': 'Металопластикові вікна',
                                'group': 'interior'
                            },
                            {
                                'feature': 'bathrooms',
                                'value': 'Суміжний санвузол',
                                'group': 'supplies'
                            },
                            {
                                'feature': 'passenger_elevators',
                                'value': '1 пасажирський ліфт',
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
                                'value': 'Суміжне планування',
                                'group': 'interior'
                            },
                            {
                                'feature': 'wall_type',
                                'value': 'Інкерманський камінь',
                                'group': 'building'
                            },
                            {
                                'feature': 'door_type',
                                'value': 'Металеві двері',
                                'group': 'interior'
                            },
                            {
                                'feature': 'window_type',
                                'value': 'Металопластикові вікна',
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
