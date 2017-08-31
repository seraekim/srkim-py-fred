from http.client import HTTPSConnection
from config import *
import os

"""
전제조건 : series.csv(02_init_seriess.py 를 실행) 가 존재하여야 함.
"""
conn = HTTPSConnection(fred_domain)

series_id_list = [line.rstrip('\n') for line in open(fred_ids_file_series_csv)]
series_id_list_len = len(series_id_list)

series_cnt = 0
for series_id in series_id_list:
    series_cnt += 1
    filename = fred_series_file_path + series_id + '.json'
    if os.path.isfile(filename):
        print('[파일존재]', filename)
    else:
        with open(filename, 'w', encoding='utf-8') as f2:
            ret2 = req(conn, fred_series_url + series_id)['seriess'][0]
            # series 메타 json 표준화
            #to_stand_json(ret2)
            f2.write(json.dumps(ret2))

        ret = req(conn, fred_series_observ_url + series_id)
        print('[observ] %s %d/%d' % (series_id, series_cnt, series_id_list_len))
        # series 별 observ json 저장
        with open(fred_observ_file_path + series_id + '.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(ret))
