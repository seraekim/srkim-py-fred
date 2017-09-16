"""
마지막 업데이트 : 2017-09-13
파일명 : 03_init_seriess_meta_thread.py

series.csv 로부터 가져온 series list 들을 thread를 활용하여
시리즈 메타 파일을 {{series_id}}.json으로 저장한다.
"""
import glob

from queue import Queue
from threading import Thread, Lock

from fred.path import *
from fred.util import *

"""
전제조건 : series.csv(02_init_seriess_thread.py 실행) 존재해야 함.
thread를 쓰지 않겠다면 concurrent = 1 로 지정.
"""
# path 없으면 자동 생성
if not os.path.exists(init_series_path):
    os.makedirs(init_series_path)

delete_init_files(init_series_path)

series_id_list = [line.rstrip('\n') for line in open(ids_series_csv)]
series_id_list_len = len(series_id_list)

series_cnt = 0
lock = Lock()

run_count = 0


def main(retry=False):
    global series_id_list
    global series_id_list_len
    global run_count
    global series_cnt

    def run():
        global run_count
        global series_cnt
        series_cnt = 0
        if retry:
            pfx = 'series meta retry ' + str(run_count)
        else:
            pfx = 'series meta'
        while True:
            series_id = q.get()
            with lock:
                series_cnt += 1
                print('[%s] %s %d/%d' % (pfx, series_id, series_cnt, series_id_list_len))

            filename = init_series_path + series_id + '.json'
            if not retry and os.path.isfile(filename):
                print('[파일존재]', filename)
            else:
                try:
                    ret = req(fred_series_url + series_id)['seriess'][0]
                    geo_ret = req(fred_series_geo_url + str(series_id))

                    geo = ''
                    for it in geo_ret['tags']:
                        if it['group_id'] == 'geo':
                            geo = it['name']
                            break
                    ret['geo'] = geo

                    # time.sleep(sleep_time)
                    # ret 가져오기가 성공한다면 fail 된 파일을 지운다.
                    if retry:
                        os.remove(filename + '_fail')
                except:
                    print('cannot get series meta from series_id', series_id)
                    open(filename + '_fail', 'a').close()
                    q.task_done()
                    continue

                result_len = len(ret)

                if result_len:
                    with open(filename, 'w', encoding='utf-8') as f:
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

    run_count += 1

    series_id_list = []
    for series_json_fail in glob.glob(init_series_path + "*.json_fail"):
        series_id_list.append(os.path.basename(series_json_fail).replace('.json_fail', ''))
    series_id_list_len = len(series_id_list)

    # json_fail 이 존재하면, fail만 다시 시도한다.
    if series_id_list:
        main(retry=True)

main()
