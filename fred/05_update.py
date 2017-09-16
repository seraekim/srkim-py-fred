"""
마지막 업데이트 : 2017-09-13
파일명 : 05_update.py

fred update url을 통해서 가져온 series_id 들을 가지고서
03, 04 파일을 thread 없이 실행하여 업데이트 한다. 하루의 업데이트 개수는 수천건 정도이다.
현재 이력(빈티지)관리에 대해서는 진행된 바 없으며, 파일을 받는 시점에서 깨끗이 지우고 받는다.
"""
from fred.path import *
from fred.util import *

# path 없으면 자동 생성
if not os.path.exists(update_observ_path):
    os.makedirs(update_observ_path)

delete_update_files(update_series_path)
delete_update_files(update_observ_path)

conn = HTTPSConnection(fred_domain)

cnt = 0
method_cnt = 0
is_end = False

# api 상 1000이 기본값, 바꾸게되면 limit, offset도 동일하게 적용해야 데이터 안 꼬인다.
chunk_unit = 1000
observ_chunk_unit = 100000
update_offset = 0

# 업데이트 시작 시간을 담아둠
this_start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
print(this_start_time)

# 마지막 지난 업데이트 시간 파일이 없으면 하루 전으로 생성
try:
    file = open(last_update_time, 'r')
except IOError:
    with open(last_update_time, 'w', encoding='utf-8') as f:
        d = datetime.now() - timedelta(days=1)
        f.write(d.strftime(time_format))

# 마지막 지난 업데이트 시작 시간을 가져옴
last_start_time = datetime.strptime(open(last_update_time).read().strip(), time_format)
print(last_start_time)


def get_update_series(series_list):
    global cnt
    global method_cnt
    global update_offset
    global is_end

    method_cnt += 1

    print('[method] get_update_series start count :', method_cnt)

    for series_item in series_list:
        cnt += 1
        update_id = series_item['id']
        d = series_item['last_updated']
        update_time = datetime.strptime(d[:d.rfind('-')], time_format) + timedelta(hours=9)

        # last_update_start_time.txt 보다 last_updated 가 이전이 되면 더 이상 업데이트는 없는 걸로 판단
        is_end = update_time < last_start_time
        print(cnt, update_time.strftime(time_format), update_id)

        if is_end:
            # 업데이트 '시작'을 기록하고 종료.. 업데이트 '종료' 시간이 아닌 이유는, 기록 되는 동안에도 시간이
            # 흘러가기 때문에,..
            # 다만 테스트로 돌린 경우라면 마지막 업데이트 시간을 갱신하지 않을 것.
            if chunk_unit == 1000:
                with open(last_update_time, 'w', encoding='utf-8') as f:
                    f.write(this_start_time)

            break
        else:
            try:
                # series meta 업데이트
                filename = update_series_path + update_id + '.json'

                with open(filename, 'w', encoding='utf-8') as f2:
                    ret2 = req(fred_series_url + update_id)['seriess'][0]
                    f2.write(json.dumps(ret2))
            except:
                print('cannot update series meta from series_id', update_id)

            try:
                # observ 업데이트
                ret = req(fred_series_observ_url + update_id + '&limit=' + str(observ_chunk_unit) + '&offset=' + str(0))
                observ_count = ret['count']
                v = observ_count // observ_chunk_unit
                if observ_count % observ_chunk_unit:
                    v += 1
                o_l = []
                o_l += ret['observations']
                for mult in range(1, v):
                    # print(series_id, mult, v)
                    off = observ_chunk_unit * mult
                    o_l += req(fred_series_observ_url + update_id + '&limit=' + str(observ_chunk_unit) + '&offset='
                               + str(off))['observations']

                ret['observations'] = o_l
                with open(update_observ_path + update_id + '.json', 'w', encoding='utf-8') as f:
                    f.write(json.dumps(ret))
            except:
                print('cannot update observation from series_id', update_id)

    if not is_end:
        # is_end가 아니면 여기까지 도달.. limit offset 활용..
        update_offset += chunk_unit
        update_series = req(fred_series_update_url + '&limit=' + str(chunk_unit) + '&offset=' + str(update_offset))['seriess']
        get_update_series(update_series)


# 업데이트 시작
update_series = req(fred_series_update_url)['seriess']
get_update_series(update_series)
