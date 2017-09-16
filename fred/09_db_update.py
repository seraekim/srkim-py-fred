"""
마지막 업데이트 : 2017-09-13
파일명 : 09_db_update.py

개수는 많지 않기에 하나하나 insert 확인 후 update 실행한다.
성능에 관심이 많다면, insert_many(array) 말고도 bulk upsert를 고려해도 좋다.
"""
import glob

from fred.path import *
from fred.util import *

# series
json_list = []
for file_path in glob.glob(parsed_update_series_path + "*.json"):
    json_list.append(json.loads(open(file_path).read()))
if json_list:
    mongo_upsert('series', json_list)

# observation
json_list = []
for file_path in glob.glob(parsed_update_observ_path + "*.json"):
    json_list.append(json.loads(open(file_path).read()))
if json_list:
    mongo_upsert('observation', json_list)