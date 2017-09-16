"""
마지막 업데이트 : 2017-09-13
파일명 : 08_db_init.py

몽고디비에 init 데이터를 적재한다. 다 지우고 넣는다고 가정하였기에 upsert가 고려되어 있지 않다.
디비가 자동으로 지워지게 하는 것은 위험하다 판단되어, 드롭하는 것은 mongo에 직접 접속하여 실행하면 된다.
"""
import glob

from fred.path import *
from fred.util import *

# category
file_content = open(parsed_ids_cate_json).read()
if file_content:
    json_list = json.loads(file_content)
    if json_list:
        mongo_insert_many('category', json_list)

# category_series
json_list = []
for file_path in glob.glob(init_cate_path + "*.json"):
    json_list.append(json.loads(open(file_path).read()))
if json_list:
    mongo_insert_many('category_series', json_list)

# series
json_list = []
cnt = 0
for file_path in glob.glob(parsed_init_series_path + "*.json"):
    json_list.append(json.loads(open(file_path).read()))
    cnt += 1
    if not cnt % 10000:
        mongo_insert_many('series', json_list)
        json_list = []
if json_list:
    mongo_insert_many('series', json_list)

# observation
json_list = []
cnt = 0
for file_path in glob.glob(parsed_init_observ_path + "*.json"):
    json_list.append(json.loads(open(file_path).read()))
    cnt += 1
    if not cnt % 10000:
        mongo_insert_many('series', json_list)
        json_list = []
if json_list:
    mongo_insert_many('observation', json_list)

# bulk....
#     bulk = collection.initialize_ordered_bulk_op()
#     for file_path in glob.glob(parsed_init_observ_path + "*.json"):
#         file_content = open(file_path).read()
#         if file_content:
#             json_content = json.loads(file_content)
#             mongo_bulk_upsert(bulk, json_content)
#     print('observation', len(bulk.execute()))
