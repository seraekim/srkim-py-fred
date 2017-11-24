"""
마지막 업데이트 : 2017-09-13
파일명 : 02_init_seriess_thread.py

카테고리와 series list 정보를 하나의 {{category_id}}.json 으로 저장하고,
또 series list 만을 따로 모아서 csv로 저장한다.
"""

import glob

from queue import Queue
from threading import Thread, Lock

from fred.path import *
from fred.util import *

"""
전제조건 : categories.csv(01_init_category.py 를 실행) 가 존재하여야 함.
thread를 쓰지 않겠다면 concurrent = 1 로 지정.
"""
# path 없으면 자동 생성
if not os.path.exists(init_cate_path):
    os.makedirs(init_cate_path)

delete_init_files(init_cate_path)

cate_id_list = [line.rstrip('\n') for line in open(ids_cate_csv)]
cate_id_list_len = len(cate_id_list)

cate_cnt = 0
lock = Lock()

run_count = 0

# maximum 1000
chunk_unit = 1000

def main(retry=False):

    global cate_id_list
    global cate_id_list_len
    global cate_cnt
    global run_count

    def run():
        global run_count
        global cate_cnt
        cate_cnt = 0
        if retry:
            pfx = 'series retry ' + str(run_count)
        else:
            pfx = 'series'
        while True:
            cate_id = q.get()
            with lock:
                cate_cnt += 1
                print('[%s] %s %d/%d' % (pfx, cate_id, cate_cnt, cate_id_list_len))

            filename = init_cate_path + str(cate_id) + '.json'
            # 파일이 존재하면 실행되지 않음.
            if not retry and os.path.isfile(filename):
                print('[파일존재]', filename)
            else:
                try:
                    ret = req(fred_cate_series_url + str(cate_id) +'&limit=' + str(chunk_unit) +'&offset='
                              + str(chunk_unit*0))
                    # print(ret)
                    series_count = ret['count']
                    v = series_count // chunk_unit
                    if series_count % chunk_unit:
                        v += 1
                    s_l = []
                    s_l += ret['seriess']
                    for mult in range(1, v):
                        # print(cate_id, mult, v)
                        off = chunk_unit * mult
                        s_l += req(fred_cate_series_url + str(cate_id) + '&limit=' + str(chunk_unit) + '&offset='
                                   + str(off))['seriess']

                    # time.sleep(sleep_time)
                    # ret 가져오기가 성공한다면 fail 된 파일을 지운다.
                    if retry:
                        os.remove(filename + '_fail')
                except:
                    print('cannot get series from cate_id', cate_id)
                    open(filename + '_fail', 'a').close()
                    q.task_done()
                    continue

                result_len = len(s_l)

                if result_len:
                    # 카테고리별 seriess 저장
                    series_ids_of_cate = [sub['id'] for sub in s_l]
                    series = {'_id': cate_id, 'series': series_ids_of_cate}
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(json.dumps(series))

            q.task_done()

    q = Queue(concurrent * 2)
    for i in range(concurrent):
        t = Thread(target=run)
        t.daemon = True
        t.start()

    for cate_id in cate_id_list:
        q.put(cate_id)

    q.join()

    run_count += 1

    cate_id_list = []
    for cate_json_fail in glob.glob(init_cate_path + "*.json_fail"):
        cate_id_list.append(os.path.basename(cate_json_fail).replace('.json_fail', ''))
    cate_id_list_len = len(cate_id_list)

    # json_fail 이 존재하면, fail만 다시 시도한다.
    if cate_id_list:
        main(retry=True)

main()

series_id_list = []
for cate_json in glob.glob(init_cate_path + "*.json"):
    js = json.loads(open(cate_json).read())
    series_id_list += js['seriess']

# series id만 따로 저장
if series_id_list:
    with open(ids_series_csv, 'w', encoding='utf-8') as f:
        for series_id in sorted(set(series_id_list)):
            f.write("%s\n" % series_id)

