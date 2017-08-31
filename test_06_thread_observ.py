from http.client import HTTPSConnection
from config import *
import os
from threading import Thread, Lock
from queue import Queue
import traceback

"""
전제조건 : categories.csv(01_init_category.py 를 실행) 가 존재하여야 함.
"""

series_id_list = [line.rstrip('\n') for line in open(fred_ids_file_series_csv)]
series_id_list_len = len(series_id_list)
series_cnt = 0
concurrent = 200
lock = Lock()

def run():
    global series_cnt
    global series_id_list
    while True:
        series_id = q.get()
        with lock:
            series_cnt += 1
            print('[observ] %s %d/%d' % (series_id, series_cnt, series_id_list_len))

        filename = fred_series_file_path + series_id + '.json'
        if os.path.isfile(filename):
            print('[파일존재]', filename)
        else:
            try:
                with open(filename, 'w', encoding='utf-8') as f2:
                    conn = HTTPSConnection(fred_domain)
                    ret2 = req(conn, fred_series_url + series_id)['seriess'][0]
                    # series 메타 json 표준화
                    #to_stand_json(ret2)
                    f2.write(json.dumps(ret2))
            except:
                print(traceback.format_exc())
                traceback.print_stack()

            ret = req(conn, fred_series_observ_url + series_id)
            # series 별 observ json 저장
            with open(fred_observ_file_path + series_id + '.json', 'w', encoding='utf-8') as f:
                f.write(json.dumps(ret))
        q.task_done()


q = Queue(concurrent * 2)
for i in range(concurrent):
    t = Thread(target=run)
    t.daemon = True
    t.start()

for series_id in series_id_list:
    q.put(series_id)

q.join()

