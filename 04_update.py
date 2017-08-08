import time
from http.client import HTTPSConnection
from config import *

"""
전제조건 : last_update_start_time.txt 에 마지막 지난 업데이트 시작 시간이 있어야 함.
init 단계만 진행된 경우 만들어져 있지 않다. 그렇게 한 이유는 나눠서 init한다 치면, 최초로 들어간 시간을 모르기 때문.
init이 완료되면 알아서 가장 오래된 파일의 mtime을 체크하고 넣으면 된다. (업데이트 정보 텀은 2주니까 2주내로 init
해야만 한다.)
"""

conn = HTTPSConnection(fred_domain)

cnt = 0
is_end = False

# api 상 1000이 기본값, 바꾸게되면 limit, offset도 동일하게 적용해야 데이터 안 꼬인다.
chunk_unit = 10
update_limit = chunk_unit
update_offset = 0

# 업데이트 시작 시간을 담아둠
this_start_time = time.strftime('%Y-%m-%d %H:%M:%S')
print(this_start_time)

# 마지막 지난 업데이트 시작 시간을 가져옴
last_start_time = open(fred_ids_file_last_update_time).read()
print(last_start_time)


def get_update_series(series_list):
    print('[method] get_update_series start!!!')
    global cnt
    global update_limit
    global update_offset
    global is_end

    for series_item in series_list:
        cnt += 1
        update_id = series_item['id']
        update_time = series_item['last_updated']

        # last_update_start_time.txt 보다 last_updated 가 이전이 되면 더 이상 업데이트는 없는 걸로 판단
        is_end = update_time < last_start_time
        print(is_end, update_time, last_start_time)
        if is_end:
            # 업데이트 '시작'을 기록하고 종료.. 업데이트 '종료' 시간이 아닌 이유는, 기록 되는 동안에도 시간이
            # 흘러가기 때문에,..
            with open(fred_ids_file_last_update_time, 'w', encoding='utf-8') as f:
                f.write(this_start_time)
            break
        else:
            ret = req(conn, fred_series_observ_url + update_id)
            with open(fred_series_file_path + update_id + '.json', 'w', encoding='utf-8') as f:
                f.write(json.dumps(ret))

    if not is_end:
        # is_end가 아니면 여기까지 도달.. limit offset 활용..
        update_limit += chunk_unit
        update_offset += chunk_unit
        update_series = req(conn, fred_series_update_url + '&limit=' + update_limit + '&offset=' + update_offset)['seriess']
        get_update_series(update_series)


# 업데이트 시작
update_series = req(conn, fred_series_update_url)['seriess']
get_update_series(update_series)