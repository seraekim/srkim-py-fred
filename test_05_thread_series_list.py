import os
from http.client import HTTPSConnection
from config import *
from threading import Thread, Lock
from queue import Queue

"""
전제조건 : categories.csv(01_init_category.py 를 실행) 가 존재하여야 함.
"""

cate_id_list = [line.rstrip('\n') for line in open(fred_ids_file_cate_csv)]
cate_id_list_len = len(cate_id_list)

series_id_list = []
cate_cnt = 0
concurrent = 200
lock = Lock()


def run():
    global cate_cnt
    global series_id_list
    while True:
        cate_id = q.get()
        with lock:
            cate_cnt += 1
            print('[series] %s %d/%d' % (cate_id, cate_cnt, cate_id_list_len))

        filename = fred_cate_file_path + str(cate_id) + '.json'
        if os.path.isfile(filename):
            print('[파일존재]', filename)
        else:
            # 파일이 존재하면 실행되지 않음. 강제로 지우고 하면 됨.
            conn = HTTPSConnection(fred_domain)
            ret = req(conn, fred_cate_series_url + str(cate_id))['seriess']
            result_len = len(ret)

            if result_len:
                # 카테고리별 seriess 저장
                series_ids_of_cate = [sub['id'] for sub in ret]
                series = {'categories': cate_id, 'seriess': series_ids_of_cate}
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(json.dumps(series))

                series_id_list += series_ids_of_cate
                for sub in ret:
                    series_id = sub['id']
                    series_id_list.append(series_id)
        q.task_done()


q = Queue(concurrent * 2)
for i in range(concurrent):
    t = Thread(target=run)
    t.daemon = True
    t.start()

for cate_id in cate_id_list:
    q.put(cate_id)

q.join()


# series id만 따로 저장
if series_id_list:
    print('series id만 따로 저장')
    with open(fred_ids_file_series_csv, 'w', encoding='utf-8') as f:
        for series_id in sorted(set(series_id_list)):
            f.write("%s\n" % series_id)
