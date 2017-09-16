"""
마지막 업데이트 : 2017-09-13
파일명 : 04_init_observ_thread.py

command line 에서 인자를 아무거나 하나 주면, 사용자 정의 카테고리를 가지고,
아니라면 전체 카테고리를 가지고서 해당 되는 observation을
{{series_id}}.json 으로 저장한다.

혹시라도 인자를 주는 것에서 매우 모호하다 판단되면, 사용자 정의 카테고리 전용의
py 파일을 작성하여 분리해도 좋다.
"""
import glob
import sys

from queue import Queue
from threading import Thread, Lock

from fred.path import *
from fred.util import *

"""
전제조건 : series.csv(02_init_seriess_thread.py 실행) 존재해야 함.
thread를 쓰지 않겠다면 concurrent = 1 로 지정.
"""

# path 없으면 자동 생성
if not os.path.exists(init_observ_path):
    os.makedirs(init_observ_path)

# observation은 init 이어도 무조건 다 지우고 새로 받는다.
delete_init_files(init_observ_path, is_clean=True)


series_id_list = []
series_id_list_len = 0

# 그냥 전체 category의 obs를 받을지, 사용자 정의 category로 부터 obs를 받을지..
if len(sys.argv) > 1:
    # 아무 인자나 추가로 넣으면... categories_product.csv 를 쓰는 것으로 간주
    cate_list = [line.rstrip('\n') for line in open(ids_cate_product_csv)]
    for cate in cate_list:
        f_n = init_cate_path + cate + '.json'
        if os.path.isfile(f_n):
            j = json.loads(open(f_n).read())
            if 'series' in j:
                series_id_list += j['series']
    series_id_list_len = len(series_id_list)
else:
    series_id_list = [line.rstrip('\n') for line in open(ids_series_csv)]
    series_id_list_len = len(series_id_list)



series_cnt = 0
lock = Lock()

run_count = 0

chunk_unit = 100000

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
            pfx = 'observ retry ' + str(run_count)
        else:
            pfx = 'observ'
        while True:
            series_id = q.get()
            with lock:
                series_cnt += 1
                print('[%s] %s %d/%d' % (pfx, series_id, series_cnt, series_id_list_len))

            filename = init_observ_path + series_id + '.json'
            if not retry and os.path.isfile(filename):
                print('[파일존재]', filename)
            else:
                try:
                    ret = req(fred_series_observ_url + series_id + '&limit=' + str(chunk_unit) + '&offset=' + str(0))
                    # print(ret)
                    observ_count = ret['count']
                    v = observ_count // chunk_unit
                    if observ_count % chunk_unit:
                        v += 1
                    o_l = []
                    o_l += ret['observations']
                    for mult in range(1, v):
                        # print(series_id, mult, v)
                        off = chunk_unit * mult
                        o_l += req(fred_series_observ_url + series_id + '&limit=' + str(chunk_unit) + '&offset='
                                   + str(off))['observations']

                    ret['observations'] = o_l
                    # ret 가져오기가 성공한다면 fail 된 파일을 지운다.
                    if retry:
                        os.remove(filename + '_fail')
                except:
                    print('cannot get observation from series_id', series_id)
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
    for series_json_fail in glob.glob(init_observ_path + "*.json_fail"):
        series_id_list.append(os.path.basename(series_json_fail).replace('.json_fail', ''))
    series_id_list_len = len(series_id_list)

    # json_fail 이 존재하면, fail만 다시 시도한다.
    if series_id_list:
        main(retry=True)

main()
