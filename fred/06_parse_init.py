"""
마지막 업데이트 : 2017-09-13
파일명 : 06_parse_init.py

mongodb에 적재되는 형태로 파싱한다.
mongodb collection은 다음과 같이 이루어진다.
category : 카테고리 정보(category_id, name, parent_id)
category_series : 카테고리 - 시리즈 관계 (category_id, series_id)
series : 시리즈 메타 정보 (series_id, last_update, frequency ...)
observation : 실제 데이터 (series_id, period, value)

단 위 4가지 콜렉션에서 category_series 만큼은 파싱할 것이 없어서, data/init의 파일이 그대로 몽고디비에 적재된다.
"""
import glob

from time import time
from fred.path import *
from fred.util import *

_start = time()
print('start')

path_list = [parsed_init_cate_path, parsed_init_series_path, parsed_init_observ_path]

# path 없으면 자동 생성
for path in path_list:
    if not os.path.exists(path):
        os.makedirs(path)

delete_update_files(parsed_init_series_path)
delete_update_files(parsed_init_observ_path)

# categories.json parse
cate_json = json.loads(open(ids_cate_json).read())
for it in cate_json:
    it['_id'] = it.pop('id')
    it['name'] = it.pop('name')
    it['parent_id'] = it.pop('parent_id')
    it.pop('notes', '')

with open(parsed_ids_cate_json, 'w', encoding='utf-8') as f:
    f.write(json.dumps(cate_json))

# init series meta parse
for file_path in glob.glob(init_series_path + "*.json"):
    file_content = open(file_path).read()
    if file_content:
        json_content = json.loads(file_content)
        to_stand_series_meta(json_content)
        parsed_file_path = parsed_init_series_path + os.path.basename(file_path)
        with open(parsed_file_path, 'w', encoding='utf-8') as f:
            f.write(json.dumps(json_content))

# init observation parse
for file_path in glob.glob(init_observ_path + "*.json"):
    file_content = open(file_path).read()
    if file_content:
        json_content = json.loads(file_content)
        to_stand_observ(json_content, os.path.basename(file_path).replace('.json', ''))
        parsed_file_path = parsed_init_observ_path + os.path.basename(file_path)
        with open(parsed_file_path, 'w', encoding='utf-8') as f:
            f.write(json.dumps(json_content))

print(time() - _start)

