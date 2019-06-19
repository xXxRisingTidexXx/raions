from asyncio import gather
from unittest import TestCase
from asynctest import CoroutineMock
from core.crawlers import Crawler
from core.geolocators import NominatimGeolocator
from core.decorators import webtest


class NominatimGeolocatorTestCase(TestCase):
    @webtest
    async def test_locate(self, session, executor, scribbler):
        geolocator = NominatimGeolocator(Crawler(session, scribbler), executor, scribbler)
        geolocator._crawler.get_json = CoroutineMock(side_effect=(
            {
                'place_id': 127512700,
                'licence': 'Data © OpenStreetMap contributors, ODbL 1.0. https://osm.org/copyright',
                'osm_type': 'way',
                'osm_id': 221856396,
                'lat': '46.9540677',
                'lon': '32.0679921093019',
                'display_name': '70, 4-а Повздовжня вулиця, Старий Водопій, Інгульський '
                                'район, Миколаїв, Миколаївська область, 54028, Україна',
                'address': {
                    'house_number': '70',
                    'road': '4-а Повздовжня вулиця',
                    'neighbourhood': 'Старий Водопій',
                    'county': 'Інгульський район',
                    'city': 'Миколаїв',
                    'state': 'Миколаївська область',
                    'postcode': '54028',
                    'country': 'Україна',
                    'country_code': 'ua'
                },
                'boundingbox': ['46.9539304', '46.9542051', '32.0677453', '32.0682389']
            },
            [
                {
                    'place_id': 113906256,
                    'licence': 'Data © OpenStreetMap contributors, ODbL 1.0. https://osm.org/copyright',
                    'osm_type': 'way',
                    'osm_id': 164792111,
                    'boundingbox': ['49.2257329', '49.2344952', '28.4121576', '28.4154968'],
                    'lat': '49.2301549',
                    'lon': '28.4138787',
                    'display_name': 'Юності проспект, Вишенька, Вінниця, '
                                    'Вінницька область, 21000-21499, Україна',
                    'class': 'highway',
                    'type': 'secondary',
                    'importance': 0.42000000000000004,
                    'address': {
                        'road': 'Юності проспект',
                        'suburb': 'Вишенька',
                        'city': 'Вінниця',
                        'state': 'Вінницька область',
                        'postcode': '21000-21499',
                        'country': 'Україна',
                        'country_code': 'ua'
                    }
                }
            ],
            [
                {
                    'place_id': 112359385,
                    'licence': 'Data © OpenStreetMap contributors, ODbL 1.0. https://osm.org/copyright',
                    'osm_type': 'way',
                    'osm_id': 160744974,
                    'boundingbox': ['46.9552593', '46.9557007', '31.9380506', '31.9396165'],
                    'lat': '46.9555386',
                    'lon': '31.9388867',
                    'display_name': 'Лазурна вулиця, Намив, Заводський район, '
                                    'Миколаїв, Миколаївська область, 54058, Україна',
                    'class': 'highway',
                    'type': 'residential',
                    'importance': 0.42000000000000004,
                    'address': {
                        'road': 'Лазурна вулиця',
                        'neighbourhood': 'Намив',
                        'county': 'Заводський район',
                        'city': 'Миколаїв',
                        'state': 'Миколаївська область',
                        'postcode': '54058',
                        'country': 'Україна',
                        'country_code': 'ua'
                    }
                }
            ],
            [
                {
                    'place_id': 112185814,
                    'licence': 'Data © OpenStreetMap contributors, ODbL 1.0. https://osm.org/copyright',
                    'osm_type': 'way',
                    'osm_id': 160146376,
                    'boundingbox': ['46.4794822', '46.4796559', '30.7431342', '30.7435512'],
                    'lat': '46.4795618',
                    'lon': '30.7433421724603',
                    'display_name': '14, Жуковського вулиця, Ланжерон, Одеса, Приморський '
                                    'район, Одеса, Одеська область, 65082, Україна',
                    'class': 'building',
                    'type': 'yes',
                    'importance': 0.42099999999999993,
                    'address': {
                        'house_number': '14',
                        'road': 'Жуковського вулиця',
                        'suburb': 'Ланжерон',
                        'city': 'Одеса',
                        'county': 'Приморський район',
                        'state': 'Одеська область',
                        'postcode': '65082',
                        'country': 'Україна',
                        'country_code': 'ua'
                    }
                }
            ],
            [
                {
                    'place_id': 195586826,
                    'licence': 'Data © OpenStreetMap contributors, ODbL 1.0. https://osm.org/copyright',
                    'osm_type': 'way',
                    'osm_id': 593824220,
                    'boundingbox': ['48.4490091', '48.451786', '35.0665555', '35.0697879'],
                    'lat': '48.4501532',
                    'lon': '35.0678803',
                    'display_name': 'Сімферопольська вулиця, Дніпро, Соборний район, Дніпровська '
                                    'міська рада, Дніпропетровська область, 49094, Україна',
                    'class': 'highway',
                    'type': 'tertiary',
                    'importance': 0.4,
                    'address': {
                        'road': 'Сімферопольська вулиця',
                        'city': 'Дніпро',
                        'county': 'Дніпровська міська рада',
                        'state': 'Дніпропетровська область',
                        'postcode': '49094',
                        'country': 'Україна',
                        'country_code': 'ua'
                    }
                }
            ],
            {
                'place_id': 167903024,
                'licence': 'Data © OpenStreetMap contributors, ODbL 1.0. https://osm.org/copyright',
                'osm_type': 'way',
                'osm_id': 415887957,
                'lat': '50.2300920926146',
                'lon': '30.6501038210499',
                'display_name': 'Козин, Обухівський район, Київська область, 08711, Україна',
                'address': {
                    'village': 'Козин',
                    'county': 'Обухівський район',
                    'state': 'Київська область',
                    'postcode': '08711',
                    'country': 'Україна',
                    'country_code': 'ua'
                },
                'boundingbox': ['50.2294179', '50.2304689', '30.6500062', '30.6507118']
            },
            {
                'place_id': 163131409,
                'licence': 'Data © OpenStreetMap contributors, ODbL 1.0. https://osm.org/copyright',
                'osm_type': 'way',
                'osm_id': 381936481,
                'lat': '51.5428873',
                'lon': '31.292074',
                'display_name': 'Чернігівський провулок, Чернігів, Деснянський район, Чернігівська '
                                'міська рада, Чернігівська область, 14000-14499, Україна',
                'address': {
                    'road': 'Чернігівський провулок',
                    'city': 'Чернігів',
                    'county': 'Чернігівська міська рада',
                    'state': 'Чернігівська область',
                    'postcode': '14000-14499',
                    'country': 'Україна',
                    'country_code': 'ua'
                },
                'boundingbox': ['51.5405408', '51.5428873', '31.292074', '31.2953411']
            },
            {
                'place_id': 84210281,
                'licence': 'Data © OpenStreetMap contributors, ODbL 1.0. https://osm.org/copyright',
                'osm_type': 'way',
                'osm_id': 34697290,
                'lat': '46.291399912498',
                'lon': '30.6491012294219',
                'display_name': 'Приморська вулиця, Старе Бугово, Чорноморськ, Молодіжненська сільська '
                                'рада, Чорноморська міська рада, Одеська область, 68003, Україна',
                'address': {
                    'road': 'Приморська вулиця',
                    'neighbourhood': 'Старе Бугово',
                    'town': 'Чорноморськ',
                    'city': 'Молодіжненська сільська рада',
                    'county': 'Чорноморська міська рада',
                    'state': 'Одеська область',
                    'postcode': '68003',
                    'country': 'Україна',
                    'country_code': 'ua'
                },
                'boundingbox': ['46.2834083', '46.2948631', '30.6484649', '30.6505118']
            },
            {
                'place_id': 154774936,
                'licence': 'Data © OpenStreetMap contributors, ODbL 1.0. https://osm.org/copyright',
                'osm_type': 'way',
                'osm_id': 343944356,
                'lat': '48.14936585',
                'lon': '23.0299709189926',
                'display_name': 'JJ, 13, Вакарова вулиця, Цілина, Виноградівська міська рада, '
                                'Виноградівський район, Закарпатська область, 90300, Україна',
                'address': {
                    'hotel': 'JJ',
                    'house_number': '13',
                    'road': 'Вакарова вулиця',
                    'neighbourhood': 'Цілина',
                    'city': 'Виноградівська міська рада',
                    'county': 'Виноградівський район',
                    'state': 'Закарпатська область',
                    'postcode': '90300',
                    'country': 'Україна',
                    'country_code': 'ua'
                },
                'boundingbox': ['48.1491456', '48.1494798', '23.0296393', '23.0303115']
            },
            [
                {
                    'place_id': 250514989,
                    'licence': 'Data © OpenStreetMap contributors, ODbL 1.0. https://osm.org/copyright',
                    'osm_type': 'way',
                    'osm_id': 471302694,
                    'boundingbox': ['43.1182499', '43.118394', '131.915841', '131.9160034'],
                    'lat': '43.118323',
                    'lon': '131.915929464024',
                    'display_name': '14, улица Жуковского, Ленинский район, Владивосток, '
                                    'Владивостокский городской округ, Приморский край, ДФО, 690000, РФ',
                    'class': 'building',
                    'type': 'house',
                    'importance': 0.32100000000000006,
                    'address': {
                        'house_number': '14',
                        'road': 'улица Жуковского',
                        'city_district': 'Ленинский район',
                        'city': 'Владивосток',
                        'county': 'Владивостокский городской округ',
                        'state': 'Приморский край',
                        'postcode': '690000',
                        'country': 'РФ',
                        'country_code': 'ru'
                    }
                }
            ],
            {
                'place_id': 254761294,
                'licence': 'Data © OpenStreetMap contributors, ODbL 1.0. https://osm.org/copyright',
                'osm_type': 'node',
                'osm_id': 3815077900,
                'lat': '0',
                'lon': '0',
                'display_name': 'Atlas Buoy 0.00E 0.00N',
                'address': {'address29': 'Atlas Buoy 0.00E 0.00N'},
                'boundingbox': ['-0.0001', '0.0001', '-0.0001', '0.0001']
            },
            [
                {
                    'place_id': 198929892,
                    'licence': 'Data © OpenStreetMap contributors, ODbL 1.0. https://osm.org/copyright',
                    'osm_type': 'relation',
                    'osm_id': 1577673,
                    'boundingbox': ['55.7520028', '55.7552929', '37.6178899', '37.6234209'],
                    'lat': '55.7536532',
                    'lon': '37.6213676671642',
                    'display_name': 'Красная площадь, Китай-город, Тверской район, '
                                    'Центральный административный округ, Москва, ЦФО, РФ',
                    'class': 'highway',
                    'type': 'pedestrian',
                    'importance': 0.7910371921866901,
                    'address': {
                        'pedestrian': 'Красная площадь',
                        'neighbourhood': 'Китай-город',
                        'suburb': 'Тверской район',
                        'state_district': 'Центральный административный округ',
                        'state': 'Москва',
                        'country': 'РФ',
                        'country_code': 'ru'
                    }
                }
            ],
            {'error': 'Unable to geocode'},
            {'error': 'Unable to geocode'},
            {
                'place_id': 22389798,
                'licence': 'Data © OpenStreetMap contributors, ODbL 1.0. https://osm.org/copyright',
                'osm_type': 'node',
                'osm_id': 2209384485,
                'lat': '30.3782016',
                'lon': '30.3552079',
                'display_name': 'مدينة وادي النطرون, \u200fالبحيرة\u200e, مصر',
                'address': {
                    'town': 'مدينة وادي النطرون',
                    'state': '\u200fالبحيرة\u200e',
                    'country': 'مصر',
                    'country_code': 'eg'
                },
                'boundingbox': ['30.2982016', '30.4582016', '30.2752079', '30.4352079']
            },
            [
                {
                    'place_id': 199324647,
                    'licence': 'Data © OpenStreetMap contributors, ODbL 1.0. https://osm.org/copyright',
                    'osm_type': 'relation',
                    'osm_id': 8398124,
                    'boundingbox': ['40.6996823', '40.8777963', '-74.0194416', '-73.9101872'],
                    'lat': '40.7900869',
                    'lon': '-73.9598295',
                    'display_name': 'Manhattan, New York County, NYC, New York, USA',
                    'class': 'boundary',
                    'type': 'administrative',
                    'importance': 1.01014193609354,
                    'icon': 'https://nominatim.openstreetmap.org/images/'
                            'mapicons/poi_boundary_administrative.p.20.png',
                    'address': {
                        'city_district': 'Manhattan',
                        'county': 'New York County',
                        'city': 'NYC',
                        'state': 'New York',
                        'country': 'USA',
                        'country_code': 'us'
                    }
                }
            ],
            [],
            {'error': 'Unable to geocode'},
            []
        ))
        cases = (
            (
                {'point': (32.06781272, 46.95413871)},
                {
                    'point': (32.0679921093019, 46.9540677),
                    'state': 'Миколаївська область',
                    'locality': 'Миколаїв',
                    'county': 'Інгульський район',
                    'neighbourhood': 'Старий Водопій',
                    'road': '4-а Повздовжня вулиця',
                    'house_number': '70'
                }
            ),
            (
                {'address': 'Вінниця, Вишенька, Юності, 20/73'},
                {
                    'point': (28.4138787, 49.2301549),
                    'state': 'Вінницька область',
                    'locality': 'Вінниця',
                    'county': None,
                    'neighbourhood': 'Вишенька',
                    'road': 'Юності проспект',
                    'house_number': None
                }
            ),
            (
                {'address': 'Миколаїв, Намив, Лазурна'},
                {
                    'point': (31.9388867, 46.9555386),
                    'state': 'Миколаївська область',
                    'locality': 'Миколаїв',
                    'county': 'Заводський район',
                    'neighbourhood': 'Намив',
                    'road': 'Лазурна вулиця',
                    'house_number': None
                }
            ),
            (
                {'address': 'Одеса, Приморський, Жуковського, 14'},
                {
                    'point': (30.7433421724603, 46.4795618),
                    'state': 'Одеська область',
                    'locality': 'Одеса',
                    'county': 'Приморський район',
                    'neighbourhood': 'Ланжерон',
                    'road': 'Жуковського вулиця',
                    'house_number': '14'
                }
            ),
            (
                {'address': 'Дніпропетровськ, Соборний, Сімферопольська'},
                {
                    'point': (35.0678803, 48.4501532),
                    'state': 'Дніпропетровська область',
                    'locality': 'Дніпро',
                    'county': 'Соборний район',
                    'neighbourhood': None,
                    'road': 'Сімферопольська вулиця',
                    'house_number': None
                }
            ),
            (
                {'point': (30.64999962, 50.22999954)},
                {
                    'point': (30.6501038210499, 50.2300920926146),
                    'state': 'Київська область',
                    'locality': 'Козин',
                    'county': 'Обухівський район',
                    'neighbourhood': None,
                    'road': None,
                    'house_number': None
                }
            ),
            (
                {'point': (31.28781997, 51.54306979)},
                {
                    'point': (31.292074, 51.5428873),
                    'state': 'Чернігівська область',
                    'locality': 'Чернігів',
                    'county': 'Деснянський район',
                    'neighbourhood': None,
                    'road': 'Чернігівський провулок',
                    'house_number': None
                }
            ),
            (
                {'point': (30.6491012294218, 46.2913999124985)},
                {
                    'point': (30.6491012294219, 46.291399912498),
                    'state': 'Одеська область',
                    'locality': 'Чорноморськ',
                    'county': None,
                    'neighbourhood': 'Старе Бугово',
                    'road': 'Приморська вулиця',
                    'house_number': None
                }
            ),
            (
                {'point': (23.0299709189926, 48.14936585)},
                {
                    'point': (23.0299709189926, 48.14936585),
                    'state': 'Закарпатська область',
                    'locality': None,
                    'county': 'Виноградівський район',
                    'neighbourhood': 'Цілина',
                    'road': 'Вакарова вулиця',
                    'house_number': '13'
                }
            ),
            (
                {'address': 'Владивосток, Жуковского, 14'}, None
            ),
            (
                {'point': (0, 0)}, None
            ),
            (
                {'address': 'Москва, Красная площадь'}, None
            ),
            (
                {'point': (-90, -90)}, None
            ),
            (
                {'point': (32.4902112, -34.823234)}, None
            ),
            (
                {'point': (30.3109384, 30.34655432)}, None
            ),
            (
                {'address': 'Manhattan, NY 10036, USA'}, None
            ),
            (
                {'address': 'qd2wdwefergrtgrtg, 98'}, None
            ),
            (
                {'point': (4.987653627, 54.12345435)}, None
            ),
            (
                {'address': 'wefweKBJybwjybfwkLJNK8o23hkjwf, 82nkwekjfkj, 1'}, None
            )
        )
        await gather(*(self.__locate(geolocator, c) for c in cases))

    async def __locate(self, geolocator, case):
        self.assertEqual(await geolocator.locate(case[0]), case[1])
