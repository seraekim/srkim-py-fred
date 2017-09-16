"""
마지막 업데이트 : 2017-09-13
파일명 : 07_parse_update.py

크롤링한 데이터는 크게 init과 update로 분리되어 관리되는데, 이것은 update만을 파싱한다.
"""
import glob

from fred.path import *
from fred.util import *

path_list = [parsed_update_series_path, parsed_update_observ_path]

# path 없으면 자동 생성
for path in path_list:
    if not os.path.exists(path):
        os.makedirs(path)

delete_update_files(parsed_update_series_path)
delete_update_files(parsed_update_observ_path)

# update series meta parse
for file_path in glob.glob(update_series_path + "*.json"):
    file_content = open(file_path).read()
    if file_content:
        json_content = json.loads(file_content)
        to_stand_series_meta(json_content)
        parsed_file_path = parsed_update_series_path + os.path.basename(file_path)
        with open(parsed_file_path, 'w', encoding='utf-8') as f:
            f.write(json.dumps(json_content))

# update observation parse
for file_path in glob.glob(update_observ_path + "*.json"):
    file_content = open(file_path).read()
    if file_content:
        json_content = json.loads(file_content)
        to_stand_observ(json_content, os.path.basename(file_path).replace('.json', ''))
        parsed_file_path = parsed_update_observ_path + os.path.basename(file_path)
        with open(parsed_file_path, 'w', encoding='utf-8') as f:
            f.write(json.dumps(json_content))
