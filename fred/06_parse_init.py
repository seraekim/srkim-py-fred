# json 표준화 하여 parsed에 쌓기

import glob

from fred.path import *
from fred.util import *

path_list = [parsed_init_series_path, parsed_init_observ_path]

# path 없으면 자동 생성
for path in path_list:
    if not os.path.exists(path):
        os.makedirs(path)

delete_update_files(parsed_init_series_path)
delete_update_files(parsed_init_observ_path)

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