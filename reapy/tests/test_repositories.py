from datetime import date, timedelta
from unittest import TestCase
from asynctest import CoroutineMock
from asyncio import gather
from core.repositories import FlatRepository
from core.structs import Flat
from core.utils import decimalize


# class FlatRepositoryTestCase(TestCase):
#     @dbtest
#     async def test_delete_all_expired(self, pool, scribbler):
#         repository = FlatRepository(pool, scribbler)
#         async with pool.acquire() as connection:
#             user = await connection.fetchrow('''
#                 INSERT INTO core_user (password, email, is_active, is_staff)
#                 VALUES ('abcd', 'email@gmail.com', TRUE, FALSE) RETURNING id
#             ''')
#         async with pool.acquire() as connection:
#             geolocations = await connection.fetch('''
#                 INSERT INTO geolocations (locality, point) VALUES
#                 ('Kyiv', st_setsrid(st_point(48.0987, 53.5098), 4326)),
#                 ('Cherkasy', st_setsrid(st_point(48.98765, 51.0987), 4326))
#                 RETURNING id
#             ''')
#         async with pool.acquire() as connection:
#             detail = await connection.fetchrow('''
#                 INSERT INTO details (feature, value, "group") VALUES ('f1', 'v1', 'g1') RETURNING id
#             ''')
#         async with pool.acquire() as connection:
#             flats = await connection.fetch(
#                 '''
#                 INSERT INTO flats (
#                 url, published, price, rate, area, rooms, floor, total_floor, geolocation_id
#                 ) VALUES
#                 ('url1', '2018-11-15', 35000, 500, 70, 3, 7, 10, $1),
#                 ('url2', '2019-01-30', 38400, 600, 64, 2, 4, 9, $2),
#                 ('url3', current_date - INTERVAL '2 months 3 days', 72000, 900, 80, 3, 15, 16, $1)
#                 RETURNING id
#                 ''',
#                 geolocations[0]['id'], geolocations[1]['id']
#             )
#         async with pool.acquire() as connection:
#             await connection.execute(
#                 'INSERT INTO flats_details (flat_id, detail_id) VALUES ($1, $2), ($3, $4)',
#                 flats[1]['id'], detail['id'], flats[0]['id'], detail['id']
#             )
#         async with pool.acquire() as connection:
#             await connection.execute(
#                 'INSERT INTO core_user_saved_flats (user_id, flat_id) VALUES ($1, $2), ($3, $4)',
#                 user['id'], flats[1]['id'], user['id'], flats[2]['id']
#             )
#         await repository.delete_all_expired(timedelta(days=120))
#         async with pool.acquire() as connection:
#             deleted = await connection.fetch(
#                 'SELECT id FROM flats_details WHERE flat_id IN ($1)', flats[0]['id']
#             )
#         self.assertEqual(deleted, [])
#         async with pool.acquire() as connection:
#             flat = await connection.fetchrow(
#                 'SELECT url, geolocation_id FROM flats WHERE id = $1', flats[2]['id']
#             )
#         self.assertEqual(flat['url'], 'url3')
#         self.assertEqual(flat['geolocation_id'], geolocations[0]['id'])
#         async with pool.acquire() as connection:
#             deleted = await connection.fetch('SELECT url FROM flats WHERE id IN ($1)', flats[0]['id'])
#         self.assertEqual(deleted, [])
#
#     @dbtest
#     async def test_delete_all_junks(self, pool, scribbler):
#         repository = FlatRepository(pool, scribbler)
#         async with pool.acquire() as connection:
#             user = await connection.fetchrow('''
#                 INSERT INTO core_user (password, email, is_active, is_staff)
#                 VALUES ('abcd', 'email@gmail.com', TRUE, FALSE) RETURNING id
#             ''')
#         async with pool.acquire() as connection:
#             geolocations = await connection.fetch('''
#                 INSERT INTO geolocations (locality, point) VALUES
#                 ('Kyiv', st_setsrid(st_point(48.0987, 53.5098), 4326)),
#                 ('Cherkasy', st_setsrid(st_point(48.98765, 51.0987), 4326)),
#                 ('Poltava', st_setsrid(st_point(49.01293, 50.916733), 4326))
#                 RETURNING id
#             ''')
#         async with pool.acquire() as connection:
#             detail = await connection.fetchrow('''
#                 INSERT INTO details (feature, value, "group") VALUES ('f1', 'v1', 'g1') RETURNING id
#             ''')
#         async with pool.acquire() as connection:
#             flats = await connection.fetch(
#                 '''
#                 INSERT INTO flats (
#                 url, published, price, rate, area, rooms, floor, total_floor, geolocation_id
#                 ) VALUES
#                 ('https://pornhub.com/url0', '2018-11-15', 35000, 500, 70, 3, 7, 10, $1),
#                 ('https://pornhub.com/url1', '2019-01-30', 38400, 600, 64, 2, 4, 9, $2),
#                 ('https://pornhub.com/url2', '2019-06-04', 72000, 900, 80, 3, 15, 16, $3),
#                 ('https://droch.io/url3', '2019-03-31', 40000, 800, 50, 2, 7, 16, $2),
#                 ('https://pornhub.com/url3', '2019-05-31', 40000, 800, 50, 2, 4, 16, $2)
#                 RETURNING id
#                 ''',
#                 geolocations[0]['id'], geolocations[1]['id'], geolocations[2]['id']
#             )
#         async with pool.acquire() as connection:
#             await connection.execute(
#                 'INSERT INTO flats_details (flat_id, detail_id) VALUES ($1, $2), ($3, $4), ($5, $6)',
#                 flats[0]['id'], detail['id'], flats[1]['id'], detail['id'], flats[2]['id'], detail['id']
#             )
#         async with pool.acquire() as connection:
#             await connection.execute(
#                 'INSERT INTO core_user_saved_flats (user_id, flat_id) VALUES ($1, $2), ($3, $4)',
#                 user['id'], flats[2]['id'], user['id'], flats[3]['id']
#             )
#         sieve = CoroutineMock(return_value={flats[0], flats[4]})
#         await repository.delete_all_junks('https://pornhub.com', sieve)
#         async with pool.acquire() as connection:
#             deleted = await connection.fetch(
#                 'SELECT url FROM flats WHERE id IN ($1, $2)', flats[0]['id'], flats[4]['id']
#             )
#         self.assertEqual(deleted, [])
#
#     @dbtest
#     async def test_find_record(self, pool, scribbler):
#         repository = FlatRepository(pool, scribbler)
#         async with pool.acquire() as connection:
#             geolocations = await connection.fetch('''
#                 INSERT INTO geolocations (point) VALUES
#                 (st_setsrid(st_point(44.290987, 32.053208), 4326)),
#                 (st_setsrid(st_point(38.0000345002, 33.0023001), 4326))
#                 RETURNING id
#             ''')
#         async with pool.acquire() as connection:
#             flats = await connection.fetch(
#                 '''
#                 INSERT INTO flats (
#                 url, avatar, published, price, rate, area, living_area, kitchen_area,
#                 rooms, floor, total_floor, ceiling_height, geolocation_id
#                 ) VALUES
#                 ('xx1', NULL, DATE '2019-04-03', 35000, 500, 70, NULL, NULL, 2, 7, 9, NULL, $1),
#                 ('xx2', 'ava2', DATE '2018-12-18', 50000, 500, 100, 60, 19.5, 3, 8, 9, 2.75, $2)
#                 RETURNING id
#                 ''',
#                 geolocations[0]['id'], geolocations[1]['id']
#             )
#         structs = (
#             Flat(
#                 url='xx3', geolocation={'point': (34.23, 35.0765)}, area=50,
#                 kitchen_area=15.7, rooms=2, floor=4, total_floor=9
#             ),
#             Flat(
#                 url='xx4', geolocation={'point': (51.3, 52.97)}, area=70,
#                 kitchen_area=24.9, rooms=2, floor=7, total_floor=9
#             ),
#             Flat(
#                 url='xx5', geolocation={'point': (44.290986, 32.0532)}, area=58,
#                 kitchen_area=18, rooms=2, floor=7, total_floor=9
#             ),
#             Flat(
#                 url='xx6', geolocation={'point': (44.290986, 32.0532)}, area=70,
#                 kitchen_area=18, rooms=2, floor=3, total_floor=9
#             ),
#             Flat(
#                 url='xx7', geolocation={'point': (44.3043, 32.09542)}, area=69.5,
#                 rooms=2, floor=7, total_floor=9
#             )
#         )
#         for struct in structs:
#             async with pool.acquire() as connection:
#                 self.assertIsNone(await repository._find_record(connection, struct))
#         cases = (
#             (
#                 flats[1],
#                 Flat(
#                     url='xx2', geolocation={'point': (38.0000345, 33.0023)}, area=100,
#                     kitchen_area=58.9, living_area=19, rooms=3, floor=8, total_floor=9
#                 )
#             ),
#             (
#                 flats[0],
#                 Flat(
#                     url='xx11', avatar='ava11', geolocation={'point': (44.29099, 32.05321)},
#                     area=71.1, kitchen_area=18.3, rooms=2, floor=7, total_floor=9
#                 )
#             )
#         )
#         await gather(*(self.__find(repository, pool, c) for c in cases))
#
#     async def __find(self, repository, pool, case):
#         async with pool.acquire() as connection:
#             self.assertEqual(case[0][0], (await repository._find_record(connection, case[1]))[0])
#
#     @dbtest
#     async def test_update_record(self, pool, scribbler):
#         repository = FlatRepository(pool, scribbler)
#         async with pool.acquire() as connection:
#             geolocations = await connection.fetch('''
#                 INSERT INTO geolocations (locality, point) VALUES
#                 ('Kyiv', st_setsrid(st_point(48.0987, 53.5098), 4326)),
#                 ('Cherkasy', st_setsrid(st_point(48.98765, 51.0987), 4326))
#                 RETURNING id
#             ''')
#         async with pool.acquire() as connection:
#             details = await connection.fetch('''
#                 INSERT INTO details (feature, value, "group")
#                 VALUES ('f1', 'v1', 'g1'), ('f2', 'v2', 'g2'), ('f3', 'v3', 'g3')
#                 RETURNING id
#             ''')
#         async with pool.acquire() as connection:
#             flats = await connection.fetch(
#                 '''
#                 INSERT INTO flats (
#                 url, published, price, rate, area, living_area, kitchen_area,
#                 rooms, floor, total_floor, ceiling_height, geolocation_id
#                 ) VALUES
#                 ('url1', '2019-5-15', 35000, 500, 70, 52.8, 13.54, 3, 7, 10, 3, $1),
#                 ('url2', '2019-04-30', 38400, 600, 64.3, NULL, 14.6, 2, 4, 9, NULL, $2)
#                 RETURNING id, price
#                 ''',
#                 geolocations[0]['id'], geolocations[1]['id']
#             )
#         async with pool.acquire() as connection:
#             await connection.execute(
#                 'INSERT INTO flats_details (flat_id, detail_id) VALUES ($1, $2), ($3, $4), ($5, $6)',
#                 flats[0]['id'], details[0]['id'], flats[1]['id'], details[0]['id'], flats[1]['id'], details[1]['id']
#             )
#         structs = (
#             Flat(
#                 url='durl1', published=date(2019, 5, 17), geolocation={'point': (48.0987, 53.5098)},
#                 price=decimalize(37400), rate=decimalize(534.29), area=70, rooms=3, floor=7, total_floor=10
#             ),
#             Flat(
#                 url='url2', published=date(2019, 4, 30), geolocation={'point': (48.98765, 51.0987)},
#                 price=decimalize(36480), rate=decimalize(570), area=64, living_area=43, kitchen_area=14.5,
#                 rooms=2, floor=4, total_floor=9, ceiling_height=2.7, details=['v3']
#             )
#         )
#         async with pool.acquire() as connection:
#             await repository._update_record(connection, flats[0], structs[0])
#             old = await connection.fetchrow('''
#                 SELECT f.id, price FROM flats f
#                 JOIN flats_details fd ON f.id = fd.flat_id
#                 JOIN details d ON fd.detail_id = d.id
#                 JOIN geolocations g ON f.geolocation_id = g.id
#                 WHERE locality = 'Kyiv' AND feature = 'f1' AND value = 'v1' AND
#                 url = 'url1' AND rooms = 3 AND floor = 7 AND total_floor = 10 AND
#                 price = 35000 AND rate = 500
#             ''')
#         self.assertIsNotNone(old)
#         self.assertEqual(flats[0]['id'], old['id'])
#         async with pool.acquire() as connection:
#             await repository._update_record(connection, flats[1], structs[1])
#             new = await connection.fetchrow('''
#                 SELECT f.id, price FROM flats f
#                 JOIN flats_details fd ON f.id = fd.flat_id
#                 JOIN details d ON fd.detail_id = d.id
#                 JOIN geolocations g ON f.geolocation_id = g.id
#                 WHERE locality = 'Cherkasy' AND feature = 'f3' AND value = 'v3' AND
#                 url = 'url2' AND rooms = 2 AND floor = 4 AND total_floor = 9 AND
#                 area = 64 AND living_area = 43 AND kitchen_area = 14.5 AND
#                 ceiling_height = 2.7 AND price = 36480 AND rate = 570
#             ''')
#         self.assertIsNotNone(new)
#         self.assertEqual(flats[1]['id'], new['id'])
#
#     @dbtest
#     async def test_distinct_all(self, pool, scribbler):
#         repository = FlatRepository(pool, scribbler)
#         async with pool.acquire() as connection:
#             geolocations = await connection.fetch('''
#                 INSERT INTO geolocations (point) VALUES
#                 (st_setsrid(st_point(44.29, 32.05), 4326)),
#                 (st_setsrid(st_point(38.000000002, 33.000000001), 4326)),
#                 (st_setsrid(st_point(51.18181818, 48.5506), 4326))
#                 RETURNING id
#             ''')
#         async with pool.acquire() as connection:
#             details = await connection.fetch('''
#                 INSERT INTO details (feature, value, "group") VALUES
#                 ('f1', 'v1', 'g1'), ('f2', 'v2', 'g2'), ('f3', 'v3', 'g3')
#                 RETURNING id
#             ''')
#         async with pool.acquire() as connection:
#             flats = await connection.fetch(
#                 '''
#                 INSERT INTO flats (
#                 url, avatar, published, price, rate, area, living_area, kitchen_area,
#                 rooms, floor, total_floor, ceiling_height, geolocation_id
#                 ) VALUES
#                 ('xx1', NULL, DATE '2019-04-03', 35000, 500, 70, NULL, NULL, 2, 7, 9, NULL, $1),
#                 ('xx2', 'ava2', DATE '2018-12-18', 70000, 700, 100, 60, 19.5, 3, 8, 9, 2.75, $1),
#                 ('xx3', 'ava3', DATE '2018-12-03', 42000, 600, 70, NULL, 22, 2, 5, 9, NULL, $1),
#                 ('xx4', NULL, DATE '2019-05-05', 135000, 1200, 112.5, 72, 34, 3, 21, 24, NULL, $2),
#                 ('xx5', 'ava5', DATE '2018-05-02', 180000, 1560, 115.38, NULL, NULL, 3, 18, 21, 3, $3)
#                 RETURNING id
#                 ''',
#                 geolocations[0][0], geolocations[1][0], geolocations[2][0]
#             )
#         async with pool.acquire() as connection:
#             await connection.execute(
#                 'INSERT INTO flats_details (detail_id, flat_id) VALUES ($1, $2), ($3, $4), ($5, $6)',
#                 details[0][0], flats[4][0], details[1][0], flats[4][0], details[2][0], flats[3][0]
#             )
#         structs = (
#             Flat(
#                 url='o1', avatar='im1', published=date(2019, 4, 3), geolocation={'point': (48, 33)},
#                 price=decimalize(40000), rate=decimalize(800), area=50, rooms=2, floor=5, total_floor=16
#             ),
#             Flat(
#                 url='dr1', avatar='im2', published=date(2019, 1, 4), geolocation={'point': (44.29, 32.05)},
#                 price=decimalize(60000), rate=decimalize(600), area=100, living_area=60.6, rooms=3, floor=8,
#                 total_floor=9, details=['v1']
#             ),
#             Flat(
#                 url='dr2', published=date(2019, 2, 18), geolocation={'point': (43.35, 41.5867)},
#                 price=decimalize(80000), rate=decimalize(1600), area=50, living_area=38, kitchen_area=11,
#                 rooms=2, floor=10, total_floor=14, details=['vx']
#             ),
#             Flat(
#                 url='o2', published=date(2019, 4, 17), geolocation={'point': (38.00004, 33.00003)},
#                 price=decimalize(130000), rate=decimalize(1000), area=130, rooms=3, floor=21, total_floor=24
#             ),
#             Flat(
#                 url='o3', avatar='im5', published=date(2018, 5, 2), geolocation={'point': (51.18181818, 48.5506)},
#                 price=decimalize(185000), rate=decimalize(1603.397), area=115.38, rooms=3, floor=18,
#                 total_floor=21, details=['v4']
#             )
#         )
#         expectations = [
#             Flat(
#                 url='o1', avatar='im1', published=date(2019, 4, 3), geolocation={'point': (48, 33)},
#                 price=decimalize(40000), rate=decimalize(800), area=50, rooms=2, floor=5, total_floor=16
#             ),
#             Flat(
#                 url='dr2', published=date(2019, 2, 18), geolocation={'point': (43.35, 41.5867)},
#                 price=decimalize(80000), rate=decimalize(1600), area=50, living_area=38, kitchen_area=11,
#                 rooms=2, floor=10, total_floor=14, details=['vx']
#             ),
#             Flat(
#                 url='o2', published=date(2019, 4, 17), geolocation={'point': (38.00004, 33.00003)},
#                 price=decimalize(130000), rate=decimalize(1000), area=130, rooms=3, floor=21, total_floor=24
#             )
#         ]
#         self.assertEqual(list(await repository.distinct_all(structs)), expectations)
#         async with pool.acquire() as connection:
#             new = await connection.fetchrow('''
#                 SELECT f.id, price FROM flats f
#                 JOIN flats_details fd ON f.id = fd.flat_id
#                 JOIN details d ON fd.detail_id = d.id
#                 JOIN geolocations g ON f.geolocation_id = g.id
#                 WHERE feature = 'f1' AND value = 'v1' AND url = 'dr1' AND rooms = 3 AND
#                 floor = 8 AND total_floor = 9 AND area = 100 AND living_area = 60.6 AND
#                 kitchen_area IS NULL AND avatar = 'im2' AND price = 60000 AND rate = 600
#             ''')
#         self.assertIsNotNone(new)
#         self.assertEqual(flats[1]['id'], new['id'])
#
#     @dbtest
#     async def test_create_all(self, pool, scribbler):
#         logging.disable()
#         repository = FlatRepository(pool, scribbler)
#         repository._scribbler.add = CoroutineMock()
#         async with pool.acquire() as connection:
#             geolocations = await connection.fetch('''
#                 INSERT INTO geolocations (point) VALUES
#                 (st_setsrid(st_point(44.0672520115, 43.0985213187), 4326)),
#                 (st_setsrid(st_point(41.000820002, 39.065000001), 4326))
#                 RETURNING id
#             ''')
#         async with pool.acquire() as connection:
#             details = await connection.fetch('''
#                 INSERT INTO details (feature, value, "group") VALUES
#                 ('state', 'excellent state', 'interior'),
#                 ('wall_type', 'brick', 'building'),
#                 ('bathrooms', '2 bathrooms', 'supplies')
#                 RETURNING id
#             ''')
#         async with pool.acquire() as connection:
#             flats = await connection.fetch(
#                 '''
#                 INSERT INTO flats (
#                 url, avatar, published, price, rate, area, living_area, kitchen_area,
#                 rooms, floor, total_floor, ceiling_height, geolocation_id
#                 ) VALUES
#                 ('url1', 'ava1', DATE '2019-05-10', 35000, 500, 70, 58, 10, 2, 3, 5, NULL, $1),
#                 ('url2', 'ava2', DATE '2019-03-18', 50000, 556, 90, 60, 24, 3, 10, 12, 2.85, $2)
#                 RETURNING id
#                 ''',
#                 geolocations[0]['id'], geolocations[1]['id']
#             )
#         async with pool.acquire() as connection:
#             await connection.execute(
#                 'INSERT INTO flats_details (detail_id, flat_id) VALUES ($1, $2), ($3, $4), ($5, $6)',
#                 details[1]['id'], flats[0]['id'], details[1]['id'], flats[1]['id'], details[0]['id'], flats[1]['id']
#             )
#         structs = (
#             Flat(
#                 url='url4',
#                 avatar='ava4',
#                 published=date(2019, 5, 11),
#                 geolocation={
#                     'point': (44.0672520115, 43.0985213187), 'state': None, 'locality': None,
#                     'county': None, 'neighbourhood': None, 'road': None, 'house_number': None
#                 },
#                 price=decimalize(35000),
#                 rate=decimalize(500),
#                 area=70,
#                 living_area=58,
#                 kitchen_area=10,
#                 rooms=2,
#                 floor=7,
#                 total_floor=12,
#                 details=['3 passenger elevators', '2 bathrooms']
#             ),
#             Flat(
#                 url='url5',
#                 published=date(2019, 5, 11),
#                 geolocation={
#                     'point': (51.342123403, 47.345045433), 'state': None, 'locality': 'Одеса',
#                     'county': 'Приморський', 'neighbourhood': None, 'road': None, 'house_number': None
#                 },
#                 price=decimalize(35000),
#                 rate=decimalize(500),
#                 area=70,
#                 living_area=51,
#                 kitchen_area=12,
#                 rooms=2,
#                 floor=8,
#                 total_floor=9,
#                 ceiling_height=2.75,
#                 details=['brick']
#             ),
#             Flat(
#                 url='url6',
#                 avatar='ava6',
#                 published=date(2019, 2, 1),
#                 geolocation={
#                     'point': (46.0987646, 53.578901), 'state': None, 'locality': 'Львів',
#                     'county': None, 'neighbourhood': None, 'road': None, 'house_number': None
#                 },
#                 price=decimalize(50000),
#                 rate=decimalize(1000),
#                 area=50,
#                 rooms=2,
#                 floor=13,
#                 total_floor=21,
#                 ceiling_height=2.8,
#                 details=['excellent state']
#             )
#         )
#         await repository.create_all(structs)
#         async with pool.acquire() as connection:
#             new_geolocation = await connection.fetchrow('''
#                 SELECT id FROM geolocations
#                 WHERE locality = 'Одеса' AND county = 'Приморський' AND
#                 point = st_setsrid(st_point(51.342123403, 47.345045433), 4326)
#             ''')
#         self.assertIsNotNone(new_geolocation)
#         async with pool.acquire() as connection:
#             remote_flat = await connection.fetchrow(
#                 "SELECT id FROM flats WHERE url = 'url5' AND geolocation_id = $1", new_geolocation[0]
#             )
#         self.assertIsNotNone(remote_flat)
#         async with pool.acquire() as connection:
#             detail = await connection.fetchrow("SELECT value FROM details WHERE feature = 'wall_type'")
#         self.assertEqual(detail['value'], 'brick')
#         async with pool.acquire() as connection:
#             flat = await connection.fetchrow('''
#                 SELECT f.id
#                 FROM flats f JOIN geolocations g ON f.geolocation_id = g.id
#                 WHERE url = 'url4' AND price = 35000 AND rooms = 2
#                 AND point = st_setsrid(st_point(44.0672520115, 43.0985213187), 4326)
#             ''')
#         self.assertIsNotNone(flat)
#         async with pool.acquire() as connection:
#             all_flats = await connection.fetch('SELECT id FROM flats')
#         self.assertEqual(len(all_flats), 5)
#         async with pool.acquire() as connection:
#             flats_details = await connection.fetch('''
#                 SELECT fd.id
#                 FROM flats_details fd JOIN details d ON fd.detail_id = d.id
#                 WHERE d.feature = 'wall_type' AND d.value = 'brick'
#             ''')
#         self.assertEqual(len(flats_details), 3)
