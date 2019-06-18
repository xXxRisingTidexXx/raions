from datetime import date
from unittest import TestCase
from asynctest import CoroutineMock
from core.decorators import processtest
from core.utils import decimalize, load
from core.structs import Flat
from core.parsers import OlxFlatParser, DomRiaFlatParser


class OlxFlatParserTestCase(TestCase):
    @processtest
    async def test_parse_stop(self, executor):
        parser = OlxFlatParser(executor, CoroutineMock())
        self.assertEqual(await parser.parse_stop(await load('fixtures/test_parse_stop/olx_flat0.html')), 500)
        with self.assertRaises(TypeError):
            await parser.parse_stop(None)

    @processtest
    async def test_parse_pages(self, executor):
        parser = OlxFlatParser(executor, CoroutineMock())
        pages = (
            await load('fixtures/test_parse_page/olx_flat0.html'),
            await load('fixtures/test_parse_page/olx_flat1.html')
        )
        offers = [
            {
                'url': 'https://www.olx.ua/obyavlenie/prodam-1kom-ts-rynok-IDBQKL8.html'
            },
            {
                'url': 'https://www.olx.ua/obyavlenie/otlichnaya-tsena-3-'
                       'k-kv-dobryninskiy-prodazha-ot-sobstvennika-IDDvwN6.html'
            },
            {
                'url': 'https://www.olx.ua/obyavlenie/prodam-2k-gostinku-'
                       'vozle-metro-armeyskaya-IDDviJO.html'
            },
            {
                'url': 'https://www.olx.ua/obyavlenie/z-mozhlivstyu-v-kre'
                       'dit-prodatsya-3-oh-kmnatna-kvartira-IDkLjoi.html'
            },
            {
                'url': 'https://www.olx.ua/obyavlenie/prodam-3-h-komnatnuy'
                       'u-kvartiru-105-kv-m-luchshee-predlozhenie-IDDtmOz.html'
            },
            {
                'url': 'https://www.olx.ua/obyavlenie/prodazha-vidovoy-3-'
                       'h-komnatnoy-kvartiry-v-g-borispol-IDDvIVS.html'
            },
            {
                'url': 'https://www.olx.ua/obyavlenie/prodam-1-'
                       'k-kvartiru-s-remontom-v-nezhine-IDm7RQK.html'
            },
            {
                'url': 'https://www.olx.ua/obyavlenie/j-prodam-1-kom-gost'
                       'inku-tsentralnyy-rayon-21-zhmr-8-9-IDCzGUE.html'
            },
            {
                'url': 'https://www.olx.ua/obyavlenie/prodam-3-h-kom-kvart-vozle'
                       '-m-geroev-dnepr-evrorem-pereplanir-otl-sos-IDDw6G2.html'
            },
            {
                'url': 'https://www.olx.ua/obyavlenie/tsentr-terasa-dva-rvnya'
                       '-sirets-vano-frankvsk-vul-belvederska-IDAK91A.html'
            },
            {
                'url': 'https://www.olx.ua/obyavlenie/prodam-IDDHmwf.html'
            },
            {
                'url': 'https://www.olx.ua/obyavlenie/2-k-kvartira-zhk-andorra-pospeshite-IDz5jxs.html'
            },
            {
                'url': 'https://www.olx.ua/obyavlenie/1-komnatnaya-metro'
                       '-pechersk-konovaltsa-schorsa-36e-IDDrTaz.html'
            },
            {
                'url': 'https://www.olx.ua/obyavlenie/prodam-3-h-'
                       'komnatnuyu-kvartiru-po-ul-urlovskaya-34-IDDs3FA.html'
            },
            {
                'url': 'https://www.olx.ua/obyavlenie/2-komnatnaya-'
                       'kvartira-v-irpen-zhk-sinergiya-IDDERLd.html'
            },
            {
                'url': 'https://www.olx.ua/obyavlenie/2-uh-komnatnaya-kvartira-nagorka-IDDHh5k.html'
            },
            {
                'url': 'https://www.olx.ua/obyavlenie/superpropozitsya'
                       '-3-i-kmnatna-po-vulits-zv-yazku-IDC2em8.html'
            },
            {
                'url': 'https://www.olx.ua/obyavlenie/prodatsya-kvartira'
                       '-pd-komertsyne-primschennya-IDDFQkO.html'
            },
            {
                'url': 'https://www.olx.ua/obyavlenie/2-k-kvartira'
                       '-naberezhnyy-kvartal-novostroy-IDCMArz.html'
            },
            {
                'url': 'https://www.olx.ua/obyavlenie/prodam-3-h-kmnatnu-kvartiru-IDDHmsY.html'
            },
            {
                'url': 'https://www.olx.ua/obyavlenie/kvartira-IDDHmsS.html'
            },
            {
                'url': 'https://www.olx.ua/obyavlenie/v-prodazhe-'
                       'vidovaya-3k-kvartira-v-dome-s-rotondami-IDDxujM.html'
            },
            {
                'url': 'https://www.olx.ua/obyavlenie/prodazha-kvartiry-IDDHmsj.html'
            },
            {
                'url': 'https://www.olx.ua/obyavlenie/1-komnatnaya-kvartira-IDnfDzk.html'
            },
            {
                'url': 'https://www.olx.ua/obyavlenie/prodam-2-kom-vidovuyu-kvartiru'
                       '-v-zhk-rivera-riviera-hozyain-kiev-IDDgPWY.html'
            },
            {
                'url': 'https://www.olx.ua/obyavlenie/eksklyuzivnaya-3-komn-'
                       'kv-ra-zhk-izumrudnyy-gorod-pavlovo-pole-IDDCaZX.html'
            },
            {
                'url': 'https://www.olx.ua/obyavlenie/dvuhkomnatnaya-53-m-charivnaya-lo-IDBT3PD.html'
            },
            {
                'url': 'https://www.olx.ua/obyavlenie/prodam-2k-kvartiru-v-afgantsev-1a-IDDHmpf.html'
            },
            {
                'url': 'https://www.olx.ua/obyavlenie/narodnogo-opolcheniya-'
                       '7-kachestvennyy-remont-vysota-potolka-n-4-2-m-IDCEN7X.html'
            },
            {
                'url': 'https://www.olx.ua/obyavlenie/vladimiro-lybedskaya-16-'
                       'metro-palats-ukraina-4-minuty-srochno-IDCE8TQ.html'
            },
            {
                'url': 'https://www.olx.ua/obyavlenie/prodam-kvartiru-'
                       'himmash-srochno-ili-obmen-torg-IDDHmoG.html'
            },
            {
                'url': 'https://www.olx.ua/obyavlenie/1-komnatnaya-metro'
                       '-pecherskaya-konovaltsa-schorsa-36e-IDDrTz0.html'
            },
            {
                'url': 'https://www.olx.ua/obyavlenie/3-h-kom-kvartira'
                       '-r-n-tsentralnaya-mytnitsa-IDDsk4R.html'
            },
            {
                'url': 'https://www.olx.ua/obyavlenie/prodam-studio-v-'
                       'zhk-yaskravyy-ul-kulzhenko-rbs-m-IDDHmlE.html'
            },
            {
                'url': 'https://www.olx.ua/obyavlenie/prodam-kvartiru-v-tsentre-dnepra-IDDsk3P.html'
            },
            {
                'url': 'https://www.olx.ua/obyavlenie/4-komnatnaya-'
                       'kvartira-v-tsentre-ot-vladeltsa-IDC2RYT.html'
            },
            {
                'url': 'https://www.olx.ua/obyavlenie/2-k-kvartira'
                       '-ul-p-zaporozhtsya-novostroy-agv-IDAiw3q.html'
            },
            {
                'url': 'https://www.olx.ua/obyavlenie/kvartira-s'
                       '-remontom-i-mebelyu-tsentr-odessy-IDBtfjE.html'
            },
            {
                'url': 'https://www.olx.ua/obyavlenie/vidovaya-1-k-elitnyy-'
                       'dom-tsentr-metro-lukyanovskaya-zhk-andersen-IDDsypW.html'
            },
            {
                'url': 'https://www.olx.ua/obyavlenie/1-komnatnaya-kv-61m2-per'
                       '-baltiyskiy-23-zhk-navigator-bez-komissii-IDDxuc3.html'
            },
            {
                'url': 'https://www.olx.ua/obyavlenie/odnokmnatna-kvartira-IDyGtTe.html'
            },
            {
                'url': 'https://www.olx.ua/obyavlenie/prodam-2-h-'
                       'komnatnuyu-kvartiru-v-s-snezhkov-IDyH49c.html'
            },
            {
                'url': 'https://www.olx.ua/obyavlenie/prodatsya-kvartira-vul-mikolaychuka-IDDHmit.html'
            },
            {
                'url': 'https://www.olx.ua/obyavlenie/prodam-2-h-kom-na-pr-pravdy'
                       '-kirpichnyy-dom-3-9-et-an-v-IDDxu9N.html'
            },
            {
                'url': 'https://www.olx.ua/obyavlenie/prodam-2h-yarusnuyu-'
                       '3h-kom-kvartiru-v-novostroe-s-novym-remontom-IDCazDu.html'
            },
            {
                'url': 'https://www.olx.ua/obyavlenie/prodaetsya-2-kom-kv-'
                       'ra-5-min-st-m-dvorets-ukraina-ul-konovaltsa-15-1-IDDcxi7.html'
            },
            {
                'url': 'https://www.olx.ua/obyavlenie/srochno-prodam-'
                       '3k-66-4m2-33-500-dom-zaselen-IDkZwfq.html'
            },
            {
                'url': 'https://www.olx.ua/obyavlenie/2-h-kom-kv-s-novym'
                       '-kap-remontom-tsentr-m-nauchnaya-12min-klochkovskaya-IDCemoX.html'
            },
            {
                'url': 'https://www.olx.ua/obyavlenie/srochno-prodam-1-'
                       'k-kvartiru-v-kievskom-rayone-IDDn6TJ.html'
            },
            {
                'url': 'https://www.olx.ua/obyavlenie/3k-'
                       'kvartira-na-lushpy-IDDI7Vc.html'
            },
            {
                'url': 'https://www.olx.ua/obyavlenie/stilnaya-2-k-chavdar-1-metro-osokorki-IDDhOmk.html'
            },
            {
                'url': 'https://www.olx.ua/obyavlenie/1-kv-tsentr-ulukrainskaya'
                       '-295-str-div-6-9kirpich37-2-19-8-polnogabaritnaya-IDx41N4.html'
            },
            {
                'url': 'https://www.olx.ua/obyavlenie/prodam-kvartiru-IDCKoJw.html'
            },
            {
                'url': 'https://www.olx.ua/obyavlenie/rassrochka-grn-loyalnyy'
                       '-pervyy-vznos-dlya-kazhdogo-bez-komissii-9-IDDy7rn.html'
            },
            {
                'url': 'https://www.olx.ua/obyavlenie/luchshiy-podarok-kvartira'
                       '-v-odesse-na-uspenskoy-IDyHzia.html'
            },
            {
                'url': 'https://www.olx.ua/obyavlenie/kvartira-v-zdano-dome-zhk-sofiya-rezydens-IDCZIYa.html'
            },
            {
                'url': 'https://www.olx.ua/obyavlenie/1-komnatnaya-kvartira'
                       '-s-dizaynerskim-remontom-kiev-harkovskoe-shosse-IDDxx6u.html'
            },
            {
                'url': 'https://www.olx.ua/obyavlenie/edinstvennaya-2-kom-81m2'
                       '-kak-treshka-na-zhabinskogo-2d-ot-zastroyschika-IDwRQ62.html'
            },
            {
                'url': 'https://www.olx.ua/obyavlenie/dvuhurovnevaya-kvartira'
                       '-zhk-ideal-na-ul-zabolotnogo-63-g-odessa-IDBPE67.html'
            },
            {
                'url': 'https://www.olx.ua/obyavlenie/srochno-tolko-eta-nedelya'
                       '-tsentr-realnomu-pokupatelyu-torg-IDzPAPC.html'
            },
            {
                'url': 'https://www.olx.ua/obyavlenie/prodam-3h-kv-pod-biznes-IDyi7Ma.html'
            },
            {
                'url': 'https://www.olx.ua/obyavlenie/dokumenty-gotovy-otlichnaya'
                       '-gostinka-s-udobstv-dk-metallurgov-IDBELxj.html'
            },
            {
                'url': 'https://www.olx.ua/obyavlenie/srochno-prodam-1k-kvartiru-v-novom'
                       '-dome-ost-steklozavod-IDDxvXJ.html'
            },
            {
                'url': 'https://www.olx.ua/obyavlenie/z-komnatnaya-kvartira-kiev-IDDI6DV.html'
            },
            {
                'url': 'https://www.olx.ua/obyavlenie/termnovo-prodam-kvartiru-'
                       'z-kapremontom-ta-meblyami-IDDy7nQ.html'
            },
            {
                'url': 'https://www.olx.ua/obyavlenie/edinstvennaya-1-kom-'
                       '47m2-na-zhabinskogo-v-rassrochku-ot-zastroyschika-IDwQ8AE.html'
            },
            {
                'url': 'https://www.olx.ua/obyavlenie/srochnoprodam1-komnatnuyu'
                       '-kvartiru5-min-ot-metrozhk-familykiev-IDDxvBt.html'
            },
            {
                'url': 'https://www.olx.ua/obyavlenie/prodam-dvuhurovnevuyu'
                       '-kvartiru-64-kv-m-v-s-milaya-IDDBjTl.html'
            },
            {
                'url': 'https://www.olx.ua/obyavlenie/prodam-odnokomnatnuyu'
                       '-kvartiru-rayon-megatsentra-IDDoMHS.html'
            },
            {
                'url': 'https://www.olx.ua/obyavlenie/kvartira-1-k-v-novostroe'
                       '-zhk-evropeyskiy-kvartal-remont-IDDy7kd.html'
            },
            {
                'url': 'https://www.olx.ua/obyavlenie/prodam-1-k-kvartiru-zhk'
                       '-lyubovi-maloy-holodnaya-gora-IDDt5c1.html'
            },
            {
                'url': 'https://www.olx.ua/obyavlenie/1k-v-novobudov-z-agv-vro-IDDxvUc.html'
            },
            {
                'url': 'https://www.olx.ua/obyavlenie/roskoshnaya-4k-v-elitnom'
                       '-royal-tower-saksaganskogo-37k-IDDxvTE.html'
            },
            {
                'url': 'https://www.olx.ua/obyavlenie/dvuhurovnevaya-kvartira'
                       '-175-kv-m-na-podole-naprotiv-sinagogi-IDCOlb5.html'
            },
            {
                'url': 'https://www.olx.ua/obyavlenie/vlasnik-prodam-'
                       'novobudova-2km-kvartira-vistavka-kovpaka-konovaltsya-IDuSED4.html'
            },
            {
                'url': 'https://www.olx.ua/obyavlenie/malopoverhova-85m2-'
                       'novobudova-v-rayon-z-du-kvarts-1062-500-grn-IDC4FmV.html'
            },
            {
                'url': 'https://www.olx.ua/obyavlenie/svoya-kvartira-s-'
                       'avtonomkoy-i-remontom-v-kirpiche-IDDxvVh.html'
            },
            {
                'url': 'https://www.olx.ua/obyavlenie/super-tsena-ot-zastroyschika'
                       '-na-3-kom-kv-pr-mira-271-v-dom-sdan-IDBXy6p.html'
            },
            {
                'url': 'https://www.olx.ua/obyavlenie/malopoverhova-novobudova'
                       '-2-h-k-kv-63m2-875-700grn-1-2-3-km-kv-IDC04vl.html'
            },
            {
                'url': 'https://www.olx.ua/obyavlenie/prodam-2-h-kom-kvartiru-v-leninskom-r-ne-IDDI7PN.html'
            },
            {
                'url': 'https://www.olx.ua/obyavlenie/2h-komnatnaya-v-tsentre'
                       '-s-avtonomnym-otopleniem-IDDxvUB.html'
            },
            {
                'url': 'https://www.olx.ua/obyavlenie/3-h-kmnatna-u-'
                       'malopoverhovy-novobudov-85m2-IDC02b7.html'
            },
            {
                'url': 'https://www.olx.ua/obyavlenie/prodam-1-novostroy-vid-'
                       'na-dnepr-malanyuka-ul-101-levoberezhnaya-metro-IDDn9hk.html'
            },
            {
                'url': 'https://www.olx.ua/obyavlenie/srochno-2-kom-kvartira-'
                       'metro-alekseevskaya-1-minuta-IDDy7hF.html'
            },
            {
                'url': 'https://www.olx.ua/obyavlenie/z-d-kvarts-vd-12-500-grn'
                       '-m2-1-2-3-h-kmnatn-malopoverhova-novob-IDDr4L2.html'
            },
            {
                'url': 'https://www.olx.ua/obyavlenie/prodam-srochno-kvartiru-IDDI7OW.html'
            },
            {
                'url': 'https://www.olx.ua/obyavlenie/3-h-komnatnaya-kvartira-'
                       '82-kv-m-s-remontom-i-mebelyu-bez-komissii-IDDlKDG.html'
            },
            {
                'url': 'https://www.olx.ua/obyavlenie/kvartira-studiya-ot-hozyaina'
                       '-s-dokumentami-v-zhk-pokrovskiy-IDzd4D0.html'
            }
        ]
        self.assertListEqual(list(await parser.parse_pages(pages)), offers)

    @processtest
    async def test_parse_offers(self, executor):
        parser = OlxFlatParser(executor, CoroutineMock())
        offers = (
            {
                'url': 'https://www.olx.ua/obyavlenie/prodam-2k-kvartiru-v-tsentre-1000-melochey-IDDqNsA.html',
                'markup': await load('fixtures/test_parse_offer/olx_flat0.html')
            },
            {
                'url': 'https://www.olx.ua/obyavlenie/2-komnatnaya-kvartira-74-met'
                       'ra-v-novopecherskoy-vezhe-po-ul-kikvidze-41-IDCqiKk.html',
                'markup': await load('fixtures/test_parse_offer/olx_flat1.html')
            },
            {
                'url': 'https://www.olx.ua/obyavlenie/bolshaya-kvartira-v-samom-tsentre-irpenya-IDDJbxi.html',
                'markup': await load('fixtures/test_parse_offer/olx_flat2.html')
            },
            {
                'url': 'https://www.olx.ua/obyavlenie/prodam-2-komnatnuyu-kvartir'
                       'u-v-32-zhemchuzhine-arkadiya-dom-sdan-IDBbRIG.html',
                'markup': await load('fixtures/test_parse_offer/olx_flat3.html')
            },
            {
                'url': 'https://www.olx.ua/obyavlenie/prodam-3-k-'
                       'kvartiru-ul-uzhviy-10-podolskiy-r-n-IDDIwaX.html',
                'markup': await load('fixtures/test_parse_offer/olx_flat4.html')
            },
            {
                'url': 'https://www.olx.ua/obyavlenie/prodazha-obmen-nedvizhimosti'
                       '-v-kieve-na-nedvizhimost-v-sankt-peterburge-IDypRFA.html',
                'markup': await load('fixtures/test_parse_offer/olx_flat5.html')
            }
        )
        structs = [
            Flat(
                url='https://www.olx.ua/obyavlenie/prodam-2k-kvartiru-v-tsentre-1000-melochey-IDDqNsA.html',
                avatar='https://apollo-ireland.akamaized.net:443/v1/files/atbs10v8fzy43-UA/image;s=644x461',
                published=date(2019, 2, 25),
                geolocation={'point': (37.56492189, 47.13203091)},
                price=decimalize('18200.000'),
                area=46.0,
                kitchen_area=6.0,
                rooms=2,
                floor=5,
                total_floor=5,
                details=[]
            ),
            Flat(
                url='https://www.olx.ua/obyavlenie/2-komnatnaya-kvartira-74-metra-v-'
                    'novopecherskoy-vezhe-po-ul-kikvidze-41-IDCqiKk.html',
                avatar='https://apollo-ireland.akamaized.net:443/v1/files/nyj7wonmwpf9-UA/image;s=644x461',
                published=date(2019, 2, 27),
                geolocation={'point': (30.55172926, 50.4070917)},
                price=decimalize('1850000.000'),
                currency='грн.',
                area=74.0,
                kitchen_area=28.0,
                rooms=2,
                floor=8,
                total_floor=26,
                details=[
                    'under construction', 'monolith', 'separate planning', 'separate bathrooms',
                    'own boiler room', 'after construction', 'no furniture'
                ]
            ),
            Flat(
                url='https://www.olx.ua/obyavlenie/bolshaya-kvartira-v-samom-tsentre-irpenya-IDDJbxi.html',
                avatar='https://apollo-ireland.akamaized.net:443/v1/files/37oo82mm73sv3-UA/image;s=644x461',
                published=date(2019, 3, 23),
                geolocation={'point': (30.2593, 50.51752)},
                price=decimalize('30500.000'),
                area=75.0,
                kitchen_area=16.0,
                rooms=1,
                floor=9,
                total_floor=10,
                details=[
                    'the tsar project', 'brick', 'adjacent through planning',
                    'adjacent bathrooms', 'own boiler room'
                ]
            ),
            Flat(
                url='https://www.olx.ua/obyavlenie/prodam-2-komnatnuyu-kvartiru'
                    '-v-32-zhemchuzhine-arkadiya-dom-sdan-IDBbRIG.html',
                avatar='https://apollo-ireland.akamaized.net:443/v1/files/p5fbluxbefad3-UA/image;s=644x461',
                published=date(2019, 3, 12),
                geolocation={'point': (30.76142585, 46.42438896)},
                price=decimalize('50000.000'),
                area=52.0,
                kitchen_area=9.0,
                rooms=2,
                floor=4,
                total_floor=24,
                details=[
                    'under construction', 'free layout', 'separate bathrooms',
                    'own boiler room', 'after construction'
                ]
            ),
            Flat(
                url='https://www.olx.ua/obyavlenie/prodam-3-k-kvartiru-ul-uzhviy-10-podolskiy-r-n-IDDIwaX.html',
                avatar='https://apollo-ireland.akamaized.net:443/v1/files/b45v2qziwxkp3-UA/image;s=644x461',
                published=date(2019, 3, 22),
                geolocation={'point': (30.43441159, 50.50743121)},
                price=decimalize('60000.000'),
                area=74.0,
                kitchen_area=9.0,
                rooms=3,
                floor=5,
                total_floor=9,
                details=[
                    'separate planning', 'separate bathrooms', 'euro-standard design', 'furniture is present'
                ]
            ),
            Flat(
                url='https://www.olx.ua/obyavlenie/prodazha-obmen-nedvizhimosti'
                    '-v-kieve-na-nedvizhimost-v-sankt-peterburge-IDypRFA.html',
                avatar='https://apollo-ireland.akamaized.net:443/v1/files/34mlkr9opvr2-UA/image;s=644x461',
                published=date(2019, 5, 20),
                geolocation={'point': (30.50188948, 50.39525513)},
                price=decimalize('71051.200'),
                area=62.1,
                kitchen_area=7.2,
                rooms=3,
                floor=2,
                total_floor=5,
                details=[]
            )
        ]
        self.assertListEqual(list(await parser.parse_offers(offers)), structs)


class DomRiaFlatParserTestCase(TestCase):
    @processtest
    async def test_parse_stop(self, executor):
        parser = DomRiaFlatParser(executor, CoroutineMock())
        self.assertEqual(
            await parser.parse_stop(await load('fixtures/test_parse_stop/dom_ria_flat0.html')), 5664
        )
        with self.assertRaises(TypeError):
            await parser.parse_stop(None)

    @processtest
    async def test_parse_pages(self, executor):
        parser = DomRiaFlatParser(executor, CoroutineMock())
        pages = (await load('fixtures/test_parse_page/dom_ria_flat0.html'),)
        offers = [
            {
                'area': 44.5,
                'avatar': 'https://cdn.riastatic.com/photosnewr/dom/photo/realty__97544760-300x200x80.webp',
                'kitchen_area': 21,
                'living_area': 18,
                'url': 'https://dom.ria.com/uk/realty-perevireno-prodaja-kvartira'
                       '-vinnitsa-sverdlovskiy-massiv-sverdlova-ulitsa-15556698.html'
            },
            {
                'area': 73.0,
                'avatar': 'https://cdn3.riastatic.com/photosnewr/dom/photo/realty__98744213-300x200x80.webp',
                'kitchen_area': 20,
                'living_area': 42,
                'url': 'https://dom.ria.com/uk/realty-perevireno-prodaja-kvartira'
                       '-vinnitsa-zamoste-50letiya-pobedyi-ulitsa-15688237.html'
            },
            {
                'area': 52.0,
                'avatar': 'https://cdn1.riastatic.com/photosnewr/dom/photo/realty__97472381-300x200x80.webp',
                'kitchen_area': 15,
                'living_area': 30,
                'url': 'https://dom.ria.com/uk/realty-perevireno-prodaja-kvartira'
                       '-vinnitsa-staryiy-gorod-pokryishkina-ulitsa-15540541.html'
            },
            {
                'area': 46.0,
                'avatar': 'https://cdn2.riastatic.com/photosnewr/dom/photo/realty__98504337-300x200x80.webp',
                'kitchen_area': 14,
                'living_area': 22,
                'url': 'https://dom.ria.com/uk/realty-perevireno-prodaja-kvartira-'
                       'vinnitsa-sverdlovskiy-massiv-sverdlova-ulitsa-15627514.html'
            },
            {
                'area': 43.0,
                'avatar': 'https://cdn4.riastatic.com/photosnewr/dom/photo/realty__99057354-300x200x80.webp',
                'kitchen_area': 14,
                'living_area': 18,
                'url': 'https://dom.ria.com/uk/realty-perevireno-prodaja-kvartira'
                       '-vinnitsa-staryiy-gorod-pokryishkina-ulitsa-15731411.html'
            },
            {
                'area': 43.7,
                'avatar': 'https://cdn2.riastatic.com/photosnewr/dom/photo/realty__97216697-300x200x80.webp',
                'kitchen_area': 11,
                'living_area': 18,
                'url': 'https://dom.ria.com/uk/realty-perevireno-prodaja-kvartira-kiev-'
                       'goloseevskiy-yasinovatskiy-pereulok-15514751.html'
            },
            {
                'area': 125.0,
                'avatar': 'https://cdn4.riastatic.com/photosnewr/dom/photo/realty__98415934-300x200x80.webp',
                'kitchen_area': 13,
                'living_area': 80,
                'url': 'https://dom.ria.com/uk/realty-perevireno-prodaja-kvartira-'
                       'vinnitsa-sverdlovskiy-massiv-litvinenko-ulitsa-15636114.html'
            },
            {
                'area': 75.0,
                'avatar': 'https://cdn2.riastatic.com/photosnewr/dom/photo/realty__98735197-300x200x80.webp',
                'kitchen_area': None,
                'living_area': None,
                'url': 'https://dom.ria.com/uk/realty-perevireno-prodaja-kvartira-'
                       'vinnitsa-agronomichnoe-michurina-ulitsa-15702463.html'
            },
            {
                'area': 65.0,
                'avatar': 'https://cdn3.riastatic.com/photosnewr/dom/photo/realty__98734323-300x200x80.webp',
                'kitchen_area': None,
                'living_area': None,
                'url': 'https://dom.ria.com/uk/realty-perevireno-prodaja-kvartira-'
                       'vinnitsa-agronomichnoe-michurina-ulitsa-15702369.html'
            },
            {
                'area': 87.0,
                'avatar': 'https://cdn4.riastatic.com/photosnewr/dom/photo/realty__98733749-300x200x80.webp',
                'kitchen_area': None,
                'living_area': None,
                'url': 'https://dom.ria.com/uk/realty-perevireno-prodaja-kvartira-'
                       'vinnitsa-agronomichnoe-michurina-ulitsa-15702313.html'
            },
            {
                'area': 65.0,
                'avatar': 'https://cdn4.riastatic.com/photosnewr/dom/photo/realty__97435174-300x200x80.webp',
                'kitchen_area': 13,
                'living_area': 38,
                'url': 'https://dom.ria.com/uk/realty-perevireno-prodaja-kvartira-vinnitsa'
                       '-barskoe-shosse-odesskaya-ulitsa-15521626.html'
            },
            {
                'area': 44.0,
                'avatar': 'https://cdn.riastatic.com/photosnewr/dom/photo/realty__98027540-300x200x80.webp',
                'kitchen_area': 13,
                'living_area': 23,
                'url': 'https://dom.ria.com/uk/realty-perevireno-prodaja-kvartira'
                       '-vinnitsa-staryiy-gorod-jk-evropeyskiy-kvartal-15579915.html'
            },
            {
                'area': 45.0,
                'avatar': 'https://cdn3.riastatic.com/photosnewr/dom/photo/realty__97758973-300x200x80.webp',
                'kitchen_area': 16,
                'living_area': 20,
                'url': 'https://dom.ria.com/uk/realty-perevireno-prodaja-kvartira-'
                       'vinnitsa-zamoste-olega-antonova-ulitsa-15579936.html'
            },
            {
                'area': 61.6,
                'avatar': 'https://cdn1.riastatic.com/photosnewr/dom/photo/realty__97747186-300x200x80.webp',
                'kitchen_area': 15,
                'living_area': 37,
                'url': 'https://dom.ria.com/uk/realty-perevireno-prodaja-kvartira-'
                       'vinnitsa-sverdlovskiy-massiv-sverdlova-ulitsa-15585429.html'
            },
            {
                'area': 78.0,
                'avatar': 'https://cdn1.riastatic.com/photosnewr/dom/photo/realty__97943841-300x200x80.webp',
                'kitchen_area': 15,
                'living_area': 46,
                'url': 'https://dom.ria.com/uk/realty-perevireno-prodaja-kvartira'
                       '-vinnitsa-sverdlovskiy-massiv-knyazey-koriatovichey-ulitsa-15609009.html'
            },
            {
                'area': 56.26,
                'avatar': 'https://cdn3.riastatic.com/photosnewr/dom/photo/realty__98794643-300x200x80.webp',
                'kitchen_area': 14,
                'living_area': 20,
                'url': 'https://dom.ria.com/uk/realty-perevireno-prodaja-kvartira'
                       '-vinnitsa-zamoste-50letiya-pobedyi-ulitsa-15672070.html'
            },
            {
                'area': 50.5,
                'avatar': 'https://cdn.riastatic.com/photosnewr/dom/photo/realty__97337415-300x200x80.webp',
                'kitchen_area': 18,
                'living_area': 23,
                'url': 'https://dom.ria.com/uk/realty-perevireno-prodaja-kvartira'
                       '-vinnitsa-sverdlovskiy-massiv-knyazey-koriatovichey-ulitsa-15506576.html'
            },
            {
                'area': 73.0,
                'avatar': 'https://cdn1.riastatic.com/photosnewr/dom/photo/realty__83999686-300x200x80.webp',
                'kitchen_area': 46,
                'living_area': 27,
                'url': 'https://dom.ria.com/uk/realty-perevireno-prodaja-kvartira'
                       '-vinnitsa-podole-svobodyi-bulvar-14149728.html'
            },
            {
                'area': 49.0,
                'avatar': 'https://cdn1.riastatic.com/photosnewr/dom/photo/realty__98237561-300x200x80.webp',
                'kitchen_area': 17,
                'living_area': 15,
                'url': 'https://dom.ria.com/uk/realty-perevireno-prodaja-kvartira'
                       '-vinnitsa-zamoste-chehova-ulitsa-15646353.html'
            },
            {
                'area': 65.0,
                'avatar': 'https://cdn.riastatic.com/photosnewr/dom/photo/realty__97707270-300x200x80.webp',
                'kitchen_area': 9,
                'living_area': 40,
                'url': 'https://dom.ria.com/uk/realty-perevireno-prodaja-kvartira-'
                       'vinnitsa-vishenka-keletskaya-ulitsa-15582553.html'
            }
        ]
        self.assertListEqual(list(await parser.parse_pages(pages)), offers)

    @processtest
    async def test_parse_offers(self, executor):
        parser = DomRiaFlatParser(executor, CoroutineMock())
        offers = (
            {
                'url': 'https://dom.ria.com/uk/realty-perevireno-prodaja-kvartira-'
                       'odessa-primorskiy-italyanskiy-bulvar-15546830.html',
                'markup': await load('fixtures/test_parse_offer/dom_ria_flat0.html'),
                'avatar': 'https://cdn.riastatic.com/photosnew/dom/photo/perevireno-prodaja'
                          '-kvartira-odessa-primorskiy-italyanskiy-bulvar__97597766fl.jpg',
                'area': 47.7,
                'living_area': 22.0,
                'kitchen_area': 15.0
            },
            {
                'url': 'https://dom.ria.com/uk/novostroyka-km-vyshnevyi-khutir-4972/',
                'markup': await load('fixtures/test_parse_offer/dom_ria_flat1.html'),
                'avatar': None,
                'area': 26,
                'living_area': 14.6,
                'kitchen_area': 8.3
            },
            {
                'url': 'https://dom.ria.com/uk/realty-perevireno-prodaja-kvartira-'
                       'vinnitsa-staryiy-gorod-pokryishkina-ulitsa-15223903.html',
                'markup': await load('fixtures/test_parse_offer/dom_ria_flat2.html'),
                'avatar': 'https://cdn.riastatic.com/photosnew/dom/photo/perevireno-prodaja'
                          '-kvartira-vinnitsa-staryiy-gorod-pokryishkina-ulitsa__94899036fl.jpg',
                'area': 52,
                'living_area': 32,
                'kitchen_area': 14
            },
            {
                'url': 'https://dom.ria.com/uk/realty-perevireno-prodaja-kvartira-'
                       'odessa-primorskiy-italyanskiy-bulvar-15591101.html',
                'markup': await load('fixtures/test_parse_offer/dom_ria_flat3.html'),
                'avatar': 'https://cdn.riastatic.com/photosnew/dom/photo/perevireno-prodaja'
                          '-kvartira-odessa-primorskiy-italyanskiy-bulvar__97910469fl.jpg',
                'area': 65,
                'living_area': None,
                'kitchen_area': None
            },
            {
                'url': 'https://dom.ria.com/uk/realty-perevireno-prodaja-kvartira-'
                       'kiev-dneprovskiy-prajskaya-ulitsa-15581555.html',
                'markup': await load('fixtures/test_parse_offer/dom_ria_flat4.html'),
                'avatar': 'https://cdn.riastatic.com/photosnew/dom/photo/perevireno-prodaja'
                          '-kvartira-kiev-dneprovskiy-prajskaya-ulitsa__97897725fl.jpg',
                'area': 44.9,
                'living_area': 29.5,
                'kitchen_area': 7.8
            },
            {
                'url': 'https://dom.ria.com/uk/realty-perevireno-prodaja-kvartira'
                       '-lvov-lyichakovskiy-begovaya-ulitsa-15431656.html',
                'markup': await load('fixtures/test_parse_offer/dom_ria_flat5.html'),
                'avatar': None,
                'area': 57.2,
                'living_area': 39.2,
                'kitchen_area': 10.8
            },
            {
                'url': 'https://dom.ria.com/uk/realty-prodaja-kvartira-'
                       'ochakov-ochakov-pervomayskaya-13179860.html',
                'markup': await load('fixtures/test_parse_offer/dom_ria_flat6.html'),
                'avatar': 'https://cdn.riastatic.com/photosnew/dom/photo/prodaja-'
                          'kvartira-ochakov-ochakov-pervomayskaya__74444903fl.jpg',
                'area': 35,
                'living_area': 19,
                'kitchen_area': 8
            },
            {
                'url': 'https://dom.ria.com/uk/realty-perevireno-prodaja-kvartira-'
                       'vinnitsa-blijnee-zamoste-vyacheslava-chernovola-ulitsa-14797413.html',
                'markup': await load('fixtures/test_parse_offer/dom_ria_flat7.html'),
                'avatar': 'https://cdn.riastatic.com/photosnewr/dom/photo/realty__98129585-300x200x80.webp',
                'area': 73.5,
                'living_area': None,
                'kitchen_area': 25
            }
        )
        structs = [
            Flat(
                url='https://dom.ria.com/uk/realty-perevireno-prodaja-kvartira'
                    '-odessa-primorskiy-italyanskiy-bulvar-15546830.html',
                avatar='https://cdn.riastatic.com/photosnew/dom/photo/perevireno-'
                       'prodaja-kvartira-odessa-primorskiy-italyanskiy-bulvar__97597766fl.jpg',
                published=date(2019, 4, 15),
                geolocation={'point': (30.75220862914432, 46.46768691411673)},
                price=decimalize('78000.000'),
                area=47.7,
                living_area=22.0,
                kitchen_area=15.0,
                rooms=1,
                floor=13,
                total_floor=14,
                details=[
                    'brick', 'individual heating', 'separate planning', 'authorial project',
                    'external and internal insulation', 'gas is absent', 'armored door',
                    'adjacent bathrooms', '1 passenger elevator', 'secondary housing'
                ]
            ),
            Flat(
                url='https://dom.ria.com/uk/realty-perevireno-prodaja-kvartira'
                    '-vinnitsa-staryiy-gorod-pokryishkina-ulitsa-15223903.html',
                avatar='https://cdn.riastatic.com/photosnew/dom/photo/perevireno'
                       '-prodaja-kvartira-vinnitsa-staryiy-gorod-pokryishkina-ulitsa__94899036fl.jpg',
                published=date(2019, 4, 10),
                geolocation={'address': 'Вінниця, Старе місто, Покришкіна вулиця'},
                price=decimalize('19900.000'),
                area=52,
                living_area=32,
                kitchen_area=14,
                rooms=2,
                floor=4,
                total_floor=12,
                ceiling_height=2.71,
                details=[
                    'brick', 'without heating', 'separate planning', 'repair required',
                    'internal insulation', 'gas is present', 'metal-plastic windows',
                    'adjacent bathrooms', '1 passenger elevator', 'secondary housing'
                ]
            ),
            Flat(
                url='https://dom.ria.com/uk/realty-perevireno-prodaja-'
                    'kvartira-odessa-primorskiy-italyanskiy-bulvar-15591101.html',
                avatar='https://cdn.riastatic.com/photosnew/dom/photo/perevireno-prodaja-'
                       'kvartira-odessa-primorskiy-italyanskiy-bulvar__97910469fl.jpg',
                published=date(2019, 4, 25),
                geolocation={'point': (30.752294459832797, 46.467716472633796)},
                price=decimalize('96000.000'),
                area=65,
                rooms=2,
                floor=12,
                total_floor=15,
                details=[
                    'brick', 'individual heating', 'separate planning', 'repair required',
                    'gas is absent', 'armored door', 'metal-plastic windows', 'separate bathrooms',
                    '1 passenger elevator', 'secondary housing'
                ]
            ),
            Flat(
                url='https://dom.ria.com/uk/realty-perevireno-prodaja-'
                    'kvartira-kiev-dneprovskiy-prajskaya-ulitsa-15581555.html',
                avatar='https://cdn.riastatic.com/photosnew/dom/photo/perevireno-'
                       'prodaja-kvartira-kiev-dneprovskiy-prajskaya-ulitsa__97897725fl.jpg',
                published=date(2019, 4, 22),
                geolocation={'point': (30.643568070947254, 50.43808004773596)},
                price=decimalize('45000.000'),
                area=44.9,
                living_area=29.5,
                kitchen_area=7.8,
                rooms=2,
                floor=1,
                total_floor=5,
                details=[
                    'panel', 'centralized heating', 'adjacent-separate planning',
                    'euro-standard design', 'external insulation', 'gas is present', 'metal door',
                    'metal-plastic windows', 'adjacent bathrooms', 'secondary housing'
                ]
            ),
            Flat(
                url='https://dom.ria.com/uk/realty-prodaja-kvartira-ochakov-ochakov-pervomayskaya-13179860.html',
                avatar='https://cdn.riastatic.com/photosnew/dom/photo/prodaja'
                       '-kvartira-ochakov-ochakov-pervomayskaya__74444903fl.jpg',
                published=date(2019, 5, 23),
                geolocation={'point': (31.52812112850194, 46.62593951428682)},
                price=decimalize('11500.000'),
                area=35,
                living_area=19,
                kitchen_area=8,
                rooms=1,
                floor=8,
                total_floor=9,
                ceiling_height=2.7,
                details=[
                    'brick', 'built in 1990-2000', 'centralized heating', 'separate planning',
                    'good state', 'gas is present', 'metal-plastic windows', 'adjacent bathrooms',
                    'without passenger elevators', 'secondary housing'
                ]
            ),
            Flat(
                url='https://dom.ria.com/uk/realty-perevireno-prodaja-kvartira-'
                    'vinnitsa-blijnee-zamoste-vyacheslava-chernovola-ulitsa-14797413.html',
                avatar='https://cdn.riastatic.com/photosnewr/dom/photo/realty__98129585-300x200x80.webp',
                published=date(2019, 5, 6),
                geolocation={'point': (28.477062352423104, 49.24405425158156)},
                price=decimalize('47000.000'),
                area=73.5,
                kitchen_area=25,
                rooms=2,
                floor=6,
                total_floor=12,
                ceiling_height=2.8,
                details=[
                    'brick', 'commissioning in 2019', 'individual heating', 'separate planning',
                    'drilling/construction work', 'external insulation', 'gas is present', 'metal door',
                    'metal-plastic windows', 'adjacent bathrooms', '1 passenger elevator', 'primary housing'
                ]
            )
        ]
        self.assertListEqual(list(await parser.parse_offers(offers)), structs)

    def test_parse_address(self):
        shaft = DomRiaFlatParser._Shaft()
        cases = (
            (
                {
                    'city_name_uk': 'Київ',
                    'pid': 134058,
                    'district_name_uk': 'Святошинський',
                    'street_name_uk': 'Монгольська вулиця'
                },
                'Київ, Святошинський, Монгольська вулиця'
            ),
            (
                {
                    'city_name_uk': 'Київ',
                    'district_name': 'Святошинский',
                    'street_name': 'Победы проспект, 231'
                },
                'Київ, Святошинский, Победы проспект, 231'
            ),
            (
                {
                    'state_name_uk': 'Київська',
                    'city_name_uk': 'Київ',
                    'rev_': '@lkejrhfhj938747jjif834+3029r3',
                    'district_name': 'Святошинский',
                    'district_name_uk': 'Святошинський',
                    'street_name': 'Зодчих ул., 70'
                },
                'Київ, Святошинський, Зодчих, 70'
            ),
            (
                {
                    'state_name_uk': 'Львівська',
                    'city_name_uk': 'Львів',
                    'city_name': 'Львов',
                    'a_weight': 0.9876456,
                    'district_name': 'Галицкий',
                    'district_name_uk': 'Галицький',
                    'street_name_uk': 'Альтаїра вулиця, буд. 13'
                },
                'Львів, Галицький, Альтаїра вулиця, 13'
            )
        )
        for case in cases:
            self.assertEqual(shaft._parse_address(case[0]), case[1])

    def test_ceiling_height(self):
        shaft = DomRiaFlatParser._Shaft()
        self.assertIsNone(shaft._ceiling_height(None))
        self.assertIsNone(shaft._ceiling_height('sdfgh'))
        cases = ((' 2. 5 ', 2.5), ('   2 .87', 2.87), ('   27', 2.7), ('330 ', 3.3), (' 2 800 ', 2.8))
        for case in cases:
            self.assertAlmostEqual(shaft._ceiling_height(case[0]), case[1], 3)

    @processtest
    async def test_parse_junks(self, executor):
        parser = DomRiaFlatParser(executor, CoroutineMock())
        junks = (
            {
                'url': 'https://dom.ria.com/uk/realty-prodaja-kvartira-kiev-goloseevskiy-15695319.html',
                'markup': await load('fixtures/test_parse_junk/dom_ria_flat0.html')
            },
            {
                'url': 'https://dom.ria.com/uk/realty-prodaja-kvartira-odessa-'
                       'kievskiy-lyustdorfskaya-dor-chernomorskaya-dor-15699660.html',
                'markup': await load('fixtures/test_parse_junk/dom_ria_flat1.html')
            },
            {
                'url': 'https://dom.ria.com/uk/realty-prodaja-kvartira-odessa-malinovskiy-komarova-15699670.html',
                'markup': await load('fixtures/test_parse_junk/dom_ria_flat2.html')
            },
            {
                'url': 'https://dom.ria.com/uk/realty-perevireno-prodaja-kvartira-'
                       'odessa-primorskiy-italyanskiy-bulvar-15546830.html',
                'markup': await load('fixtures/test_parse_junk/dom_ria_flat3.html')
            }
        )
        urls = {
            'https://dom.ria.com/uk/realty-prodaja-kvartira-kiev-goloseevskiy-15695319.html',
            'https://dom.ria.com/uk/realty-prodaja-kvartira-odessa-'
            'kievskiy-lyustdorfskaya-dor-chernomorskaya-dor-15699660.html',
            'https://dom.ria.com/uk/realty-prodaja-kvartira-odessa-malinovskiy-komarova-15699670.html'
        }
        self.assertSetEqual(await parser.parse_junks(junks), urls)
