from pytest import fixture, raises
from core.geomappers import NominatimGeomapper


@fixture
def nominatim_geomapper() -> NominatimGeomapper:
    return NominatimGeomapper()


def test_map_with_errors(nominatim_geomapper: NominatimGeomapper):
    with raises(AttributeError):
        nominatim_geomapper.map(None)  # noqa
    with raises(AttributeError):
        nominatim_geomapper.map({
            'address': 'wefweKBJybwjybfwkLJNK8o23hkjwf, 82nkwekjfkj, 1'
        })


def test_map_failure(nominatim_geomapper: NominatimGeomapper):
    assert None is nominatim_geomapper.map({})
    assert None is nominatim_geomapper.map({'error': 'Unable to geocode'})
    assert None is nominatim_geomapper.map({'point': (4.987653627, 54.12345435)})
    assert None is nominatim_geomapper.map({
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
    })
    assert None is nominatim_geomapper.map({
        'place_id': 254761294,
        'licence': 'Data © OpenStreetMap contributors, ODbL 1.0. https://osm.org/copyright',
        'osm_type': 'node',
        'osm_id': 3815077900,
        'lat': '0',
        'lon': '0',
        'display_name': 'Atlas Buoy 0.00E 0.00N',
        'address': {'address29': 'Atlas Buoy 0.00E 0.00N'},
        'boundingbox': ['-0.0001', '0.0001', '-0.0001', '0.0001']
    })
    assert None is nominatim_geomapper.map({
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
    })


def test_search_county(nominatim_geomapper: NominatimGeomapper):
    assert nominatim_geomapper._search_county(  # noqa
        'Україна, Черкаська область, Черкаси, Громова провулок, Соснівський район'
    ) == 'Соснівський район'
    assert nominatim_geomapper._search_county(  # noqa
        'Дніпропетровська область, Дніпропетровськ, Амур-'
        'Нижньодніпровський район, Промтех, Голубенка вулиця, 19'
    ) == 'Амур-Нижньодніпровський район'
    assert None is nominatim_geomapper._search_county(  # noqa
        'Україна, Вінницька область, Вінниця, Вишенька, Коцюбинського вулиця, 24'
    )
    assert None is nominatim_geomapper._search_county(  # noqa
        'Україна, Київська область, Хукіно, Новий житловий район, Чуба вулиця'
    )
    assert nominatim_geomapper._search_county(  # noqa
        'Солом’янський район, Київ, Жуляни, Бобровського вулиця, 289б'
    ) == 'Солом’янський район'
    assert nominatim_geomapper._search_county(  # noqa
        'Кам\'янський район'
    ) == 'Кам\'янський район'


def test_map_successfully(nominatim_geomapper: NominatimGeomapper):
    assert nominatim_geomapper.map({
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
    }) == {
        'point': (32.0679921093019, 46.9540677),
        'state': 'Миколаївська область',
        'locality': 'Миколаїв',
        'county': 'Інгульський район',
        'neighbourhood': 'Старий Водопій',
        'road': '4-а Повздовжня вулиця',
        'house_number': '70'
    }
    assert nominatim_geomapper.map({
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
    }) == {
        'point': (35.0678803, 48.4501532),
        'state': 'Дніпропетровська область',
        'locality': 'Дніпро',
        'county': 'Соборний район',
        'neighbourhood': None,
        'road': 'Сімферопольська вулиця',
        'house_number': None
    }
    assert nominatim_geomapper.map({
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
    }) == {
        'point': (31.292074, 51.5428873),
        'state': 'Чернігівська область',
        'locality': 'Чернігів',
        'county': 'Деснянський район',
        'neighbourhood': None,
        'road': 'Чернігівський провулок',
        'house_number': None
    }
    assert nominatim_geomapper.map({
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
    }) == {
        'point': (30.6501038210499, 50.2300920926146),
        'state': 'Київська область',
        'locality': 'Козин',
        'county': 'Обухівський район',
        'neighbourhood': None,
        'road': None,
        'house_number': None
    }
    assert nominatim_geomapper.map({
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
    }) == {
        'point': (30.6491012294219, 46.291399912498),
        'state': 'Одеська область',
        'locality': 'Чорноморськ',
        'county': None,
        'neighbourhood': 'Старе Бугово',
        'road': 'Приморська вулиця',
        'house_number': None
    }
    assert nominatim_geomapper.map({
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
    }) == {
        'point': (23.0299709189926, 48.14936585),
        'state': 'Закарпатська область',
        'locality': None,
        'county': 'Виноградівський район',
        'neighbourhood': 'Цілина',
        'road': 'Вакарова вулиця',
        'house_number': '13'
    }
