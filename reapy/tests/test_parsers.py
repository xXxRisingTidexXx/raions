from datetime import date
from decimal import Decimal
from pytest import fixture, raises
from core.utils import read
from core.structs import Flat
from core.parsers import OlxFlatParser, DomRiaFlatParser


@fixture
def olx_flat_parser() -> OlxFlatParser:
    return OlxFlatParser()


def test_parse_stop_olx_flat(olx_flat_parser: OlxFlatParser):
    assert 500 == olx_flat_parser.parse_stop(
        read('fixtures/test_parse_stop/olx_flat0.html')
    )


def test_parse_stop_olx_flat_emptiness(olx_flat_parser: OlxFlatParser):
    assert None is olx_flat_parser.parse_stop(6)  # noqa
    assert None is olx_flat_parser.parse_stop(None)  # noqa
    assert None is olx_flat_parser.parse_stop('')  # noqa
    assert None is olx_flat_parser.parse_stop({'url': 'https://pornhub.org/'})  # noqa


def test_parse_page_olx_flat(olx_flat_parser: OlxFlatParser):
    assert olx_flat_parser.parse_page(
        read('fixtures/test_parse_stop/olx_flat0.html')
    ) == [
        {
            'url': 'https://www.olx.ua/obyavlenie/1komnatnaya-s-remontom-IDCGxWq.html'
        },
        {
            'url': 'https://www.olx.ua/obyavlenie/prodam-2-komnatnaya-kvartira'
                   '-alekseevka-ul-klochkovskaya-nedorogo-IDDHmS1.html'
        },
        {
            'url': 'https://www.olx.ua/obyavlenie/1k-kv-ul-pogranichnaya-'
                   '4-slobodskaya-13500-IDwTGfi.html'
        },
        {
            'url': 'https://www.olx.ua/obyavlenie/prodam-2h-komnatnuyu-kvartiru-'
                   'v-pecherskom-r-ne-po-adresu-chigorina-61a-IDDgALO.html'
        },
        {
            'url': 'https://www.olx.ua/obyavlenie/prodatsya-2'
                   '-kmnatna-kvartira-IDDxelY.html'
        },
        {
            'url': 'https://www.olx.ua/obyavlenie/3-komnatnaya-na-kirova-IDE8Nh7.html'
        },
        {
            'url': 'https://www.olx.ua/obyavlenie/prodam-bolshuyu'
                   '-2-h-komnatnuyu-kvartiru-IDeESec.html'
        },
        {
            'url': 'https://www.olx.ua/obyavlenie/prodam-kvartiru'
                   '-v-otlichnom-meste-IDE8Ncg.html'
        },
        {
            'url': 'https://www.olx.ua/obyavlenie/prodam-2-komn-kvartiru'
                   '-s-remontom-dom-mebeli-IDDVJHL.html'
        },
        {
            'url': 'https://www.olx.ua/obyavlenie/krasnyy-liman-m-n-'
                   'yuzhnyy-prodaetsya-dvuhkomnatnaya-kvartira-IDDFTpw.html'
        },
        {
            'url': 'https://www.olx.ua/obyavlenie/prodam-2-komn-kvartiru'
                   '-s-remontom-na-lyustdorfskoy-dor-IDDVJHg.html'
        },
        {
            'url': 'https://www.olx.ua/obyavlenie/bez-komissii-4-h-komnatnaya'
                   '-kvartira-131-kv-m-v-dome-gamma-IDE5g6Y.html'
        },
        {
            'url': 'https://www.olx.ua/obyavlenie/prodam-svoyu-kvartiru-2-'
                   'h-kom-kv-ul-tsentrarnaya-IDDVJH2.html'
        },
        {
            'url': 'https://www.olx.ua/obyavlenie/prodam-2-'
                   'komnatnaya-kvartira-bogoduhov-IDE8Ngp.html'
        },
        {
            'url': 'https://www.olx.ua/obyavlenie/zhk-kahovskaya-ul-60'
                   '-levoberezhnaya-metro-peshkom-15-min-IDDoEah.html'
        },
        {
            'url': 'https://www.olx.ua/obyavlenie/prodatsya-kvartira-IDC9iQS.html'
        },
        {
            'url': 'https://www.olx.ua/obyavlenie/termnovo-2k-kvartira-'
                   'provulok-klyuchniy-r-n-kaskad-ch-IDDFSeR.html'
        },
        {
            'url': 'https://www.olx.ua/obyavlenie/prodam-1-'
                   'komnatnuyu-kvartiru-IDE8N9K.html'
        },
        {
            'url': 'https://www.olx.ua/obyavlenie/2-kmnatna-'
                   'kvartira-v-tsentr-IDCQe45.html'
        },
        {
            'url': 'https://www.olx.ua/obyavlenie/2-h-kim-kv-ra-68-kv-m-'
                   'metro-cherngvska-3-hvilini-ul-krakivska-27-IDE5g5f.html'
        },
        {
            'url': 'https://www.olx.ua/obyavlenie/prodam-2-h-komn-ot'
                   '-hozyaina-r-n-prestizha-IDxXZLU.html'
        },
        {
            'url': 'https://www.olx.ua/obyavlenie/kvartira-1-komnatnaya-IDDuh8l.html'
        },
        {
            'url': 'https://www.olx.ua/obyavlenie/13000-obmn-abo-prodazha-'
                   '3-oh-km-kv-v-lubnah-na-kvartiru-v-poltav-IDpL2x6.html'
        },
        {
            'url': 'https://www.olx.ua/obyavlenie/prodam-ili-obmenyayu-2-'
                   'h-kom-kvartiru-na-3-h-4-h-komnatnuyu-IDDq68U.html'
        },
        {
            'url': 'https://www.olx.ua/obyavlenie/prodam-2-k-cheshku-'
                   'pr-kirova-rayon-m-dragomanova-IDE5g4Q.html'
        },
        {
            'url': 'https://www.olx.ua/obyavlenie/rassrochka-na-zhile-'
                   'prodaetsya-3-k-kvartira-75m2-IDE5g4I.html'
        },
        {
            'url': 'https://www.olx.ua/obyavlenie/prodam-svoyu-1-kvartiru-v'
                   '-arkadii-stikon-s-realnym-vidom-na-more-IDz4kTm.html'
        },
        {
            'url': 'https://www.olx.ua/obyavlenie/prodam-kvartiru-'
                   'v-tsentr-duzhe-termnovo-IDwjbAK.html'
        },
        {
            'url': 'https://www.olx.ua/obyavlenie/4k-vul-shevchenka-101-'
                   '62-9-5-6-6ts-49-900-IDBpTQe.html'
        },
        {
            'url': 'https://www.olx.ua/obyavlenie/prodam-1k-'
                   'kvartiru-na-massive-IDE8NcI.html'
        },
        {
            'url': 'https://www.olx.ua/obyavlenie/odnokomnatnaya-v-'
                   'irpene-36-m-kv-ul-severinovskaya-IDE5g3c.html'
        },
        {
            'url': 'https://www.olx.ua/obyavlenie/prodam-1komnatnuyu-kvartiru'
                   '-1-5-pr-yubileynyy-87-IDE8N4G.html'
        },
        {
            'url': 'https://www.olx.ua/obyavlenie/prodam-1k-'
                   'kv-ul-astronomicheskaya-37-IDDKQUk.html'
        },
        {
            'url': 'https://www.olx.ua/obyavlenie/2-km-kv-za-super-tsnoyu-IDBCqGS.html'
        },
        {
            'url': 'https://www.olx.ua/obyavlenie/2-h-komnatnaya-kvartira'
                   '-v-klubnom-dome-v-tsentre-odessy-IDDVJCI.html'
        },
        {
            'url': 'https://www.olx.ua/obyavlenie/prodam-v-tsentre-3-'
                   'k-kvartiru-ul-sumskaya-mayakovskogo-IDE8bVF.html'
        },
        {
            'url': 'https://www.olx.ua/obyavlenie/prodam-eksklyuzivnuyu-2-'
                   'h-komnatnuyu-kvartiru-ukraina-glagoleva-atb-IDDTHoZ.html'
        },
        {
            'url': 'https://www.olx.ua/obyavlenie/3k-vul-pd-dubom-71-50'
                   '-9-3-3ts-rayon-forumu-105-000-IDBQJ3Y.html'
        },
        {
            'url': 'https://www.olx.ua/obyavlenie/2-h-komnatnya-kvartira-IDCsSwA.html'
        },
        {
            'url': 'https://www.olx.ua/obyavlenie/prodam-kvartiru-vozle-metro'
                   '-borispolskaya-novyy-dom-2016g-nedorogo-IDDGvHG.html'
        },
        {
            'url': 'https://www.olx.ua/obyavlenie/prodam-2k-'
                   'kvartiru-ul-gagarina-IDE1nIx.html'
        },
        {
            'url': 'https://www.olx.ua/obyavlenie/prodazha-3-h-komnatnoy'
                   '-kvartiry-zhitomir-desantnikov-IDv0P2O.html'
        },
        {
            'url': 'https://www.olx.ua/obyavlenie/3k-vul-dzherelna-'
                   '71-50-9-3-3ts-105-000-IDCBl6g.html'
        },
        {
            'url': 'https://www.olx.ua/obyavlenie/vidovaya-2-h-'
                   'komnatnaya-kvartira-v-arkadii-IDDVJAS.html'
        }
    ]


def test_parse_offer_olx_flat(olx_flat_parser: OlxFlatParser):
    assert olx_flat_parser.parse_offer({
        'url': 'https://www.olx.ua/obyavlenie/prodam-2k-'
               'kvartiru-v-tsentre-1000-melochey-IDDqNsA.html',
        'markup': read('fixtures/test_parse_offer/olx_flat0.html')
    }) == Flat(
        url='https://www.olx.ua/obyavlenie/prodam-2k'
            '-kvartiru-v-tsentre-1000-melochey-IDDqNsA.html',
        avatar='https://apollo-ireland.akamaized.net:443/v1'
               '/files/atbs10v8fzy43-UA/image;s=644x461',
        published=date(2019, 2, 25),
        geolocation={'point': (37.56492189, 47.13203091)},
        price=Decimal('18200.000'),
        area=46.0,
        kitchen_area=6.0,
        rooms=2,
        floor=5,
        total_floor=5,
        details=[]
    )


def test_parse_offer_olx_flat_with_errors(olx_flat_parser: OlxFlatParser):
    with raises(AttributeError):
        assert None is olx_flat_parser.parse_offer(None)  # noqa
    assert None is olx_flat_parser.parse_offer({'url': 'xxx'})

#         offers = (
#             {
#                 'url': 'https://www.olx.ua/obyavlenie/2-komnatnaya-kvartira-74-met'
#                        'ra-v-novopecherskoy-vezhe-po-ul-kikvidze-41-IDCqiKk.html',
#                 'markup': await load('fixtures/test_parse_offer/olx_flat1.html')
#             },
#             {
#                 'url': 'https://www.olx.ua/obyavlenie/bolshaya-kvartira-v-samom-tsentre-irpenya-IDDJbxi.html',
#                 'markup': await load('fixtures/test_parse_offer/olx_flat2.html')
#             },
#             {
#                 'url': 'https://www.olx.ua/obyavlenie/prodam-2-komnatnuyu-kvartir'
#                        'u-v-32-zhemchuzhine-arkadiya-dom-sdan-IDBbRIG.html',
#                 'markup': await load('fixtures/test_parse_offer/olx_flat3.html')
#             },
#             {
#                 'url': 'https://www.olx.ua/obyavlenie/prodam-3-k-'
#                        'kvartiru-ul-uzhviy-10-podolskiy-r-n-IDDIwaX.html',
#                 'markup': await load('fixtures/test_parse_offer/olx_flat4.html')
#             },
#             {
#                 'url': 'https://www.olx.ua/obyavlenie/prodazha-obmen-nedvizhimosti'
#                        '-v-kieve-na-nedvizhimost-v-sankt-peterburge-IDypRFA.html',
#                 'markup': await load('fixtures/test_parse_offer/olx_flat5.html')
#             }
#         )
#         structs = [
#             Flat(
#                 url='https://www.olx.ua/obyavlenie/2-komnatnaya-kvartira-74-metra-v-'
#                     'novopecherskoy-vezhe-po-ul-kikvidze-41-IDCqiKk.html',
#                 avatar='https://apollo-ireland.akamaized.net:443/v1/files/nyj7wonmwpf9-UA/image;s=644x461',
#                 published=date(2019, 2, 27),
#                 geolocation={'point': (30.55172926, 50.4070917)},
#                 price=decimalize('1850000.000'),
#                 currency='грн.',
#                 area=74.0,
#                 kitchen_area=28.0,
#                 rooms=2,
#                 floor=8,
#                 total_floor=26,
#                 details=[
#                     'under construction', 'monolith', 'separate planning', 'separate bathrooms',
#                     'own boiler room', 'after construction', 'no furniture'
#                 ]
#             ),
#             Flat(
#                 url='https://www.olx.ua/obyavlenie/bolshaya-kvartira-v-samom-tsentre-irpenya-IDDJbxi.html',
#                 avatar='https://apollo-ireland.akamaized.net:443/v1/files/37oo82mm73sv3-UA/image;s=644x461',
#                 published=date(2019, 3, 23),
#                 geolocation={'point': (30.2593, 50.51752)},
#                 price=decimalize('30500.000'),
#                 area=75.0,
#                 kitchen_area=16.0,
#                 rooms=1,
#                 floor=9,
#                 total_floor=10,
#                 details=[
#                     'the tsar project', 'brick', 'adjacent through planning',
#                     'adjacent bathrooms', 'own boiler room'
#                 ]
#             ),
#             Flat(
#                 url='https://www.olx.ua/obyavlenie/prodam-2-komnatnuyu-kvartiru'
#                     '-v-32-zhemchuzhine-arkadiya-dom-sdan-IDBbRIG.html',
#                 avatar='https://apollo-ireland.akamaized.net:443/v1/files/p5fbluxbefad3-UA/image;s=644x461',
#                 published=date(2019, 3, 12),
#                 geolocation={'point': (30.76142585, 46.42438896)},
#                 price=decimalize('50000.000'),
#                 area=52.0,
#                 kitchen_area=9.0,
#                 rooms=2,
#                 floor=4,
#                 total_floor=24,
#                 details=[
#                     'under construction', 'free layout', 'separate bathrooms',
#                     'own boiler room', 'after construction'
#                 ]
#             ),
#             Flat(
#                 url='https://www.olx.ua/obyavlenie/prodam-3-k-kvartiru-ul-uzhviy-10-podolskiy-r-n-IDDIwaX.html',
#                 avatar='https://apollo-ireland.akamaized.net:443/v1/files/b45v2qziwxkp3-UA/image;s=644x461',
#                 published=date(2019, 3, 22),
#                 geolocation={'point': (30.43441159, 50.50743121)},
#                 price=decimalize('60000.000'),
#                 area=74.0,
#                 kitchen_area=9.0,
#                 rooms=3,
#                 floor=5,
#                 total_floor=9,
#                 details=[
#                     'separate planning', 'separate bathrooms', 'euro-standard design', 'furniture is present'
#                 ]
#             ),
#             Flat(
#                 url='https://www.olx.ua/obyavlenie/prodazha-obmen-nedvizhimosti'
#                     '-v-kieve-na-nedvizhimost-v-sankt-peterburge-IDypRFA.html',
#                 avatar='https://apollo-ireland.akamaized.net:443/v1/files/34mlkr9opvr2-UA/image;s=644x461',
#                 published=date(2019, 5, 20),
#                 geolocation={'point': (30.50188948, 50.39525513)},
#                 price=decimalize('71051.200'),
#                 area=62.1,
#                 kitchen_area=7.2,
#                 rooms=3,
#                 floor=2,
#                 total_floor=5,
#                 details=[]
#             )
#         ]
#         self.assertListEqual(list(await parser.parse_offers(offers)), structs)
#
#
# class DomRiaFlatParserTestCase(TestCase):
#     def setUp(self) -> None:
#         logging.disable()
#
#     def tearDown(self) -> None:
#         logging.disable(logging.WARNING)
#
#     @processtest
#     async def test_parse_stop(self, executor, scribbler):
#         parser = DomRiaFlatParser(executor, scribbler)
#         self.assertEqual(
#             await parser.parse_stop(await load('fixtures/test_parse_stop/dom_ria_flat0.html')), 5664
#         )
#         self.assertIsNone(await parser.parse_stop(None))
#
#     @processtest
#     async def test_parse_pages(self, executor, scribbler):
#         parser = DomRiaFlatParser(executor, scribbler)
#         pages = (await load('fixtures/test_parse_page/dom_ria_flat0.html'),)
#         offers = [
#             {
#                 'area': 44.5,
#                 'avatar': 'https://cdn.riastatic.com/photosnewr/dom/photo/realty__97544760-300x200x80.webp',
#                 'kitchen_area': 21,
#                 'living_area': 18,
#                 'url': 'https://dom.ria.com/uk/realty-perevireno-prodaja-kvartira'
#                        '-vinnitsa-sverdlovskiy-massiv-sverdlova-ulitsa-15556698.html'
#             },
#             {
#                 'area': 73.0,
#                 'avatar': 'https://cdn3.riastatic.com/photosnewr/dom/photo/realty__98744213-300x200x80.webp',
#                 'kitchen_area': 20,
#                 'living_area': 42,
#                 'url': 'https://dom.ria.com/uk/realty-perevireno-prodaja-kvartira'
#                        '-vinnitsa-zamoste-50letiya-pobedyi-ulitsa-15688237.html'
#             },
#             {
#                 'area': 52.0,
#                 'avatar': 'https://cdn1.riastatic.com/photosnewr/dom/photo/realty__97472381-300x200x80.webp',
#                 'kitchen_area': 15,
#                 'living_area': 30,
#                 'url': 'https://dom.ria.com/uk/realty-perevireno-prodaja-kvartira'
#                        '-vinnitsa-staryiy-gorod-pokryishkina-ulitsa-15540541.html'
#             },
#             {
#                 'area': 46.0,
#                 'avatar': 'https://cdn2.riastatic.com/photosnewr/dom/photo/realty__98504337-300x200x80.webp',
#                 'kitchen_area': 14,
#                 'living_area': 22,
#                 'url': 'https://dom.ria.com/uk/realty-perevireno-prodaja-kvartira-'
#                        'vinnitsa-sverdlovskiy-massiv-sverdlova-ulitsa-15627514.html'
#             },
#             {
#                 'area': 43.0,
#                 'avatar': 'https://cdn4.riastatic.com/photosnewr/dom/photo/realty__99057354-300x200x80.webp',
#                 'kitchen_area': 14,
#                 'living_area': 18,
#                 'url': 'https://dom.ria.com/uk/realty-perevireno-prodaja-kvartira'
#                        '-vinnitsa-staryiy-gorod-pokryishkina-ulitsa-15731411.html'
#             },
#             {
#                 'area': 43.7,
#                 'avatar': 'https://cdn2.riastatic.com/photosnewr/dom/photo/realty__97216697-300x200x80.webp',
#                 'kitchen_area': 11,
#                 'living_area': 18,
#                 'url': 'https://dom.ria.com/uk/realty-perevireno-prodaja-kvartira-kiev-'
#                        'goloseevskiy-yasinovatskiy-pereulok-15514751.html'
#             },
#             {
#                 'area': 125.0,
#                 'avatar': 'https://cdn4.riastatic.com/photosnewr/dom/photo/realty__98415934-300x200x80.webp',
#                 'kitchen_area': 13,
#                 'living_area': 80,
#                 'url': 'https://dom.ria.com/uk/realty-perevireno-prodaja-kvartira-'
#                        'vinnitsa-sverdlovskiy-massiv-litvinenko-ulitsa-15636114.html'
#             },
#             {
#                 'area': 75.0,
#                 'avatar': 'https://cdn2.riastatic.com/photosnewr/dom/photo/realty__98735197-300x200x80.webp',
#                 'kitchen_area': None,
#                 'living_area': None,
#                 'url': 'https://dom.ria.com/uk/realty-perevireno-prodaja-kvartira-'
#                        'vinnitsa-agronomichnoe-michurina-ulitsa-15702463.html'
#             },
#             {
#                 'area': 65.0,
#                 'avatar': 'https://cdn3.riastatic.com/photosnewr/dom/photo/realty__98734323-300x200x80.webp',
#                 'kitchen_area': None,
#                 'living_area': None,
#                 'url': 'https://dom.ria.com/uk/realty-perevireno-prodaja-kvartira-'
#                        'vinnitsa-agronomichnoe-michurina-ulitsa-15702369.html'
#             },
#             {
#                 'area': 87.0,
#                 'avatar': 'https://cdn4.riastatic.com/photosnewr/dom/photo/realty__98733749-300x200x80.webp',
#                 'kitchen_area': None,
#                 'living_area': None,
#                 'url': 'https://dom.ria.com/uk/realty-perevireno-prodaja-kvartira-'
#                        'vinnitsa-agronomichnoe-michurina-ulitsa-15702313.html'
#             },
#             {
#                 'area': 65.0,
#                 'avatar': 'https://cdn4.riastatic.com/photosnewr/dom/photo/realty__97435174-300x200x80.webp',
#                 'kitchen_area': 13,
#                 'living_area': 38,
#                 'url': 'https://dom.ria.com/uk/realty-perevireno-prodaja-kvartira-vinnitsa'
#                        '-barskoe-shosse-odesskaya-ulitsa-15521626.html'
#             },
#             {
#                 'area': 44.0,
#                 'avatar': 'https://cdn.riastatic.com/photosnewr/dom/photo/realty__98027540-300x200x80.webp',
#                 'kitchen_area': 13.5,
#                 'living_area': 23,
#                 'url': 'https://dom.ria.com/uk/realty-perevireno-prodaja-kvartira'
#                        '-vinnitsa-staryiy-gorod-jk-evropeyskiy-kvartal-15579915.html'
#             },
#             {
#                 'area': 45.0,
#                 'avatar': 'https://cdn3.riastatic.com/photosnewr/dom/photo/realty__97758973-300x200x80.webp',
#                 'kitchen_area': 16,
#                 'living_area': 20,
#                 'url': 'https://dom.ria.com/uk/realty-perevireno-prodaja-kvartira-'
#                        'vinnitsa-zamoste-olega-antonova-ulitsa-15579936.html'
#             },
#             {
#                 'area': 61.6,
#                 'avatar': 'https://cdn1.riastatic.com/photosnewr/dom/photo/realty__97747186-300x200x80.webp',
#                 'kitchen_area': 15,
#                 'living_area': 37,
#                 'url': 'https://dom.ria.com/uk/realty-perevireno-prodaja-kvartira-'
#                        'vinnitsa-sverdlovskiy-massiv-sverdlova-ulitsa-15585429.html'
#             },
#             {
#                 'area': 78.0,
#                 'avatar': 'https://cdn1.riastatic.com/photosnewr/dom/photo/realty__97943841-300x200x80.webp',
#                 'kitchen_area': 15,
#                 'living_area': 46,
#                 'url': 'https://dom.ria.com/uk/realty-perevireno-prodaja-kvartira'
#                        '-vinnitsa-sverdlovskiy-massiv-knyazey-koriatovichey-ulitsa-15609009.html'
#             },
#             {
#                 'area': 56.26,
#                 'avatar': 'https://cdn3.riastatic.com/photosnewr/dom/photo/realty__98794643-300x200x80.webp',
#                 'kitchen_area': 14.44,
#                 'living_area': 20.12,
#                 'url': 'https://dom.ria.com/uk/realty-perevireno-prodaja-kvartira'
#                        '-vinnitsa-zamoste-50letiya-pobedyi-ulitsa-15672070.html'
#             },
#             {
#                 'area': 50.5,
#                 'avatar': 'https://cdn.riastatic.com/photosnewr/dom/photo/realty__97337415-300x200x80.webp',
#                 'kitchen_area': 18,
#                 'living_area': 23,
#                 'url': 'https://dom.ria.com/uk/realty-perevireno-prodaja-kvartira'
#                        '-vinnitsa-sverdlovskiy-massiv-knyazey-koriatovichey-ulitsa-15506576.html'
#             },
#             {
#                 'area': 73.0,
#                 'avatar': 'https://cdn1.riastatic.com/photosnewr/dom/photo/realty__83999686-300x200x80.webp',
#                 'kitchen_area': 46,
#                 'living_area': 27,
#                 'url': 'https://dom.ria.com/uk/realty-perevireno-prodaja-kvartira'
#                        '-vinnitsa-podole-svobodyi-bulvar-14149728.html'
#             },
#             {
#                 'area': 49.0,
#                 'avatar': 'https://cdn1.riastatic.com/photosnewr/dom/photo/realty__98237561-300x200x80.webp',
#                 'kitchen_area': 17.2,
#                 'living_area': 15,
#                 'url': 'https://dom.ria.com/uk/realty-perevireno-prodaja-kvartira'
#                        '-vinnitsa-zamoste-chehova-ulitsa-15646353.html'
#             },
#             {
#                 'area': 65.0,
#                 'avatar': 'https://cdn.riastatic.com/photosnewr/dom/photo/realty__97707270-300x200x80.webp',
#                 'kitchen_area': 9,
#                 'living_area': 40,
#                 'url': 'https://dom.ria.com/uk/realty-perevireno-prodaja-kvartira-'
#                        'vinnitsa-vishenka-keletskaya-ulitsa-15582553.html'
#             }
#         ]
#         self.assertEqual(list(await parser.parse_pages(pages)), offers)
#
#     @processtest
#     async def test_parse_offers(self, executor, scribbler):
#         parser = DomRiaFlatParser(executor, scribbler)
#         offers = (
#             {
#                 'url': 'https://dom.ria.com/uk/realty-perevireno-prodaja-kvartira-'
#                        'odessa-primorskiy-italyanskiy-bulvar-15546830.html',
#                 'markup': await load('fixtures/test_parse_offer/dom_ria_flat0.html'),
#                 'avatar': 'https://cdn.riastatic.com/photosnew/dom/photo/perevireno-prodaja'
#                           '-kvartira-odessa-primorskiy-italyanskiy-bulvar__97597766fl.jpg',
#                 'area': 47.7,
#                 'living_area': 22.0,
#                 'kitchen_area': 15.0
#             },
#             {
#                 'url': 'https://dom.ria.com/uk/novostroyka-km-vyshnevyi-khutir-4972/',
#                 'markup': await load('fixtures/test_parse_offer/dom_ria_flat1.html'),
#                 'avatar': None,
#                 'area': 26,
#                 'living_area': 14.6,
#                 'kitchen_area': 8.3
#             },
#             {
#                 'url': 'https://dom.ria.com/uk/realty-perevireno-prodaja-kvartira-'
#                        'vinnitsa-staryiy-gorod-pokryishkina-ulitsa-15223903.html',
#                 'markup': await load('fixtures/test_parse_offer/dom_ria_flat2.html'),
#                 'avatar': 'https://cdn.riastatic.com/photosnew/dom/photo/perevireno-prodaja'
#                           '-kvartira-vinnitsa-staryiy-gorod-pokryishkina-ulitsa__94899036fl.jpg',
#                 'area': 52,
#                 'living_area': 32,
#                 'kitchen_area': 14
#             },
#             {
#                 'url': 'https://dom.ria.com/uk/realty-perevireno-prodaja-kvartira-'
#                        'odessa-primorskiy-italyanskiy-bulvar-15591101.html',
#                 'markup': await load('fixtures/test_parse_offer/dom_ria_flat3.html'),
#                 'avatar': 'https://cdn.riastatic.com/photosnew/dom/photo/perevireno-prodaja'
#                           '-kvartira-odessa-primorskiy-italyanskiy-bulvar__97910469fl.jpg',
#                 'area': 65,
#                 'living_area': None,
#                 'kitchen_area': None
#             },
#             {
#                 'url': 'https://dom.ria.com/uk/realty-perevireno-prodaja-kvartira-'
#                        'kiev-dneprovskiy-prajskaya-ulitsa-15581555.html',
#                 'markup': await load('fixtures/test_parse_offer/dom_ria_flat4.html'),
#                 'avatar': 'https://cdn.riastatic.com/photosnew/dom/photo/perevireno-prodaja'
#                           '-kvartira-kiev-dneprovskiy-prajskaya-ulitsa__97897725fl.jpg',
#                 'area': 44.9,
#                 'living_area': 29.5,
#                 'kitchen_area': 7.8
#             },
#             {
#                 'url': 'https://dom.ria.com/uk/realty-perevireno-prodaja-kvartira'
#                        '-lvov-lyichakovskiy-begovaya-ulitsa-15431656.html',
#                 'markup': await load('fixtures/test_parse_offer/dom_ria_flat5.html'),
#                 'avatar': None,
#                 'area': 57.2,
#                 'living_area': 39.2,
#                 'kitchen_area': 10.8
#             },
#             {
#                 'url': 'https://dom.ria.com/uk/realty-prodaja-kvartira-'
#                        'ochakov-ochakov-pervomayskaya-13179860.html',
#                 'markup': await load('fixtures/test_parse_offer/dom_ria_flat6.html'),
#                 'avatar': 'https://cdn.riastatic.com/photosnew/dom/photo/prodaja-'
#                           'kvartira-ochakov-ochakov-pervomayskaya__74444903fl.jpg',
#                 'area': 35,
#                 'living_area': 19,
#                 'kitchen_area': 8
#             },
#             {
#                 'url': 'https://dom.ria.com/uk/realty-perevireno-prodaja-kvartira-'
#                        'vinnitsa-blijnee-zamoste-vyacheslava-chernovola-ulitsa-14797413.html',
#                 'markup': await load('fixtures/test_parse_offer/dom_ria_flat7.html'),
#                 'avatar': 'https://cdn.riastatic.com/photosnewr/dom/photo/realty__98129585-300x200x80.webp',
#                 'area': 73.5,
#                 'living_area': None,
#                 'kitchen_area': 25
#             },
#             {
#                 'url': 'https://dom.ria.com/uk/realty-prodaja-kvartira-zaporoje-dneprovskiy-leninskiy-12440307.html',
#                 'markup': await load('fixtures/test_parse_offer/dom_ria_flat8.html'),
#                 'avatar': None,
#                 'area': 169,
#                 'living_area': None,
#                 'kitchen_area': None
#             }
#         )
#         structs = [
#             Flat(
#                 url='https://dom.ria.com/uk/realty-perevireno-prodaja-kvartira'
#                     '-odessa-primorskiy-italyanskiy-bulvar-15546830.html',
#                 avatar='https://cdn.riastatic.com/photosnew/dom/photo/perevireno-'
#                        'prodaja-kvartira-odessa-primorskiy-italyanskiy-bulvar__97597766fl.jpg',
#                 published=date(2019, 4, 15),
#                 geolocation={'point': (30.75220862914432, 46.46768691411673)},
#                 price=decimalize('78000.000'),
#                 area=47.7,
#                 living_area=22.0,
#                 kitchen_area=15.0,
#                 rooms=1,
#                 floor=13,
#                 total_floor=14,
#                 details=[
#                     'brick', 'individual heating', 'separate planning', 'authorial project',
#                     'external and internal insulation', 'gas is absent', 'armored door',
#                     'adjacent bathrooms', '1 passenger elevator', 'secondary housing'
#                 ]
#             ),
#             Flat(
#                 url='https://dom.ria.com/uk/realty-perevireno-prodaja-kvartira'
#                     '-vinnitsa-staryiy-gorod-pokryishkina-ulitsa-15223903.html',
#                 avatar='https://cdn.riastatic.com/photosnew/dom/photo/perevireno'
#                        '-prodaja-kvartira-vinnitsa-staryiy-gorod-pokryishkina-ulitsa__94899036fl.jpg',
#                 published=date(2019, 4, 10),
#                 geolocation={'address': 'Вінниця, Старе місто, Покришкіна вулиця'},
#                 price=decimalize('19900.000'),
#                 area=52,
#                 living_area=32,
#                 kitchen_area=14,
#                 rooms=2,
#                 floor=4,
#                 total_floor=12,
#                 ceiling_height=2.71,
#                 details=[
#                     'brick', 'without heating', 'separate planning', 'repair required',
#                     'internal insulation', 'gas is present', 'metal-plastic windows',
#                     'adjacent bathrooms', '1 passenger elevator', 'secondary housing'
#                 ]
#             ),
#             Flat(
#                 url='https://dom.ria.com/uk/realty-perevireno-prodaja-'
#                     'kvartira-odessa-primorskiy-italyanskiy-bulvar-15591101.html',
#                 avatar='https://cdn.riastatic.com/photosnew/dom/photo/perevireno-prodaja-'
#                        'kvartira-odessa-primorskiy-italyanskiy-bulvar__97910469fl.jpg',
#                 published=date(2019, 4, 25),
#                 geolocation={'point': (30.752294459832797, 46.467716472633796)},
#                 price=decimalize('96000.000'),
#                 area=65,
#                 rooms=2,
#                 floor=12,
#                 total_floor=15,
#                 details=[
#                     'brick', 'individual heating', 'separate planning', 'repair required',
#                     'gas is absent', 'armored door', 'metal-plastic windows', 'separate bathrooms',
#                     '1 passenger elevator', 'secondary housing'
#                 ]
#             ),
#             Flat(
#                 url='https://dom.ria.com/uk/realty-perevireno-prodaja-'
#                     'kvartira-kiev-dneprovskiy-prajskaya-ulitsa-15581555.html',
#                 avatar='https://cdn.riastatic.com/photosnew/dom/photo/perevireno-'
#                        'prodaja-kvartira-kiev-dneprovskiy-prajskaya-ulitsa__97897725fl.jpg',
#                 published=date(2019, 4, 22),
#                 geolocation={'point': (30.643568070947254, 50.43808004773596)},
#                 price=decimalize('45000.000'),
#                 area=44.9,
#                 living_area=29.5,
#                 kitchen_area=7.8,
#                 rooms=2,
#                 floor=1,
#                 total_floor=5,
#                 details=[
#                     'panel', 'centralized heating', 'adjacent-separate planning',
#                     'euro-standard design', 'external insulation', 'gas is present', 'metal door',
#                     'metal-plastic windows', 'adjacent bathrooms', 'secondary housing'
#                 ]
#             ),
#             Flat(
#                 url='https://dom.ria.com/uk/realty-prodaja-kvartira-ochakov-ochakov-pervomayskaya-13179860.html',
#                 avatar='https://cdn.riastatic.com/photosnew/dom/photo/prodaja'
#                        '-kvartira-ochakov-ochakov-pervomayskaya__74444903fl.jpg',
#                 published=date(2019, 5, 23),
#                 geolocation={'point': (31.52812112850194, 46.62593951428682)},
#                 price=decimalize('11500.000'),
#                 area=35,
#                 living_area=19,
#                 kitchen_area=8,
#                 rooms=1,
#                 floor=8,
#                 total_floor=9,
#                 ceiling_height=2.7,
#                 details=[
#                     'brick', 'built in 1990-2000', 'centralized heating', 'separate planning',
#                     'good state', 'gas is present', 'metal-plastic windows', 'adjacent bathrooms',
#                     'without passenger elevators', 'secondary housing'
#                 ]
#             ),
#             Flat(
#                 url='https://dom.ria.com/uk/realty-perevireno-prodaja-kvartira-'
#                     'vinnitsa-blijnee-zamoste-vyacheslava-chernovola-ulitsa-14797413.html',
#                 avatar='https://cdn.riastatic.com/photosnewr/dom/photo/realty__98129585-300x200x80.webp',
#                 published=date(2019, 5, 6),
#                 geolocation={'point': (28.477062352423104, 49.24405425158156)},
#                 price=decimalize('47000.000'),
#                 area=73.5,
#                 kitchen_area=25,
#                 rooms=2,
#                 floor=6,
#                 total_floor=12,
#                 ceiling_height=2.8,
#                 details=[
#                     'brick', 'commissioning in 2019', 'individual heating', 'separate planning',
#                     'drilling/construction work', 'external insulation', 'gas is present', 'metal door',
#                     'metal-plastic windows', 'adjacent bathrooms', '1 passenger elevator', 'primary housing'
#                 ]
#             )
#         ]
#         self.assertListEqual(list(await parser.parse_offers(offers)), structs)
#
#     def test_parse_address(self):
#         shaft = DomRiaFlatParser._Shaft()
#         cases = (
#             (
#                 {
#                     'city_name_uk': 'Київ',
#                     'pid': 134058,
#                     'district_name_uk': 'Святошинський',
#                     'street_name_uk': 'Монгольська вулиця'
#                 },
#                 'Київ, Святошинський, Монгольська вулиця'
#             ),
#             (
#                 {
#                     'city_name_uk': 'Київ',
#                     'district_name': 'Святошинский',
#                     'street_name': 'Победы проспект, 231'
#                 },
#                 'Київ, Святошинский, Победы проспект, 231'
#             ),
#             (
#                 {
#                     'state_name_uk': 'Київська',
#                     'city_name_uk': 'Київ',
#                     'rev_': '@lkejrhfhj938747jjif834+3029r3',
#                     'district_name': 'Святошинский',
#                     'district_name_uk': 'Святошинський',
#                     'street_name': 'Зодчих ул., 70'
#                 },
#                 'Київ, Святошинський, Зодчих, 70'
#             ),
#             (
#                 {
#                     'state_name_uk': 'Львівська',
#                     'city_name_uk': 'Львів',
#                     'city_name': 'Львов',
#                     'a_weight': 0.9876456,
#                     'district_name': 'Галицкий',
#                     'district_name_uk': 'Галицький',
#                     'street_name_uk': 'Альтаїра вулиця, буд. 13'
#                 },
#                 'Львів, Галицький, Альтаїра вулиця, 13'
#             )
#         )
#         for case in cases:
#             self.assertEqual(shaft._parse_address(case[0]), case[1])
#
#     def test_ceiling_height(self):
#         shaft = DomRiaFlatParser._Shaft()
#         self.assertIsNone(shaft._ceiling_height(None))
#         self.assertIsNone(shaft._ceiling_height('sdfgh'))
#         cases = ((' 2. 5 ', 2.5), ('   2 .87', 2.87), ('   27', 2.7), ('330 ', 3.3), (' 2 800 ', 2.8))
#         for case in cases:
#             self.assertAlmostEqual(shaft._ceiling_height(case[0]), case[1], 3)
#
#     @processtest
#     async def test_parse_junks(self, executor, scribbler):
#         parser = DomRiaFlatParser(executor, scribbler)
#         junks = (
#             {
#                 'url': 'https://dom.ria.com/uk/realty-prodaja-kvartira-kiev-goloseevskiy-15695319.html',
#                 'markup': await load('fixtures/test_parse_junk/dom_ria_flat0.html')
#             },
#             {
#                 'url': 'https://dom.ria.com/uk/realty-prodaja-kvartira-odessa-'
#                        'kievskiy-lyustdorfskaya-dor-chernomorskaya-dor-15699660.html',
#                 'markup': await load('fixtures/test_parse_junk/dom_ria_flat1.html')
#             },
#             {
#                 'url': 'https://dom.ria.com/uk/realty-prodaja-kvartira-odessa-malinovskiy-komarova-15699670.html',
#                 'markup': await load('fixtures/test_parse_junk/dom_ria_flat2.html')
#             },
#             {
#                 'url': 'https://dom.ria.com/uk/realty-perevireno-prodaja-kvartira-'
#                        'odessa-primorskiy-italyanskiy-bulvar-15546830.html',
#                 'markup': await load('fixtures/test_parse_junk/dom_ria_flat3.html')
#             }
#         )
#         urls = {
#             'https://dom.ria.com/uk/realty-prodaja-kvartira-kiev-goloseevskiy-15695319.html',
#             'https://dom.ria.com/uk/realty-prodaja-kvartira-odessa-'
#             'kievskiy-lyustdorfskaya-dor-chernomorskaya-dor-15699660.html',
#             'https://dom.ria.com/uk/realty-prodaja-kvartira-odessa-malinovskiy-komarova-15699670.html'
#         }
#         self.assertSetEqual(await parser.parse_junks(junks), urls)
