from http.client import HTTPSConnection
from fred.path import fred_domain
import json
import os
import traceback
from datetime import datetime, timedelta
# var ======================
# init 시 기존 파일 다 지우고 하는가?
is_clean = False

# active thread count 조정
concurrent = 200

# thread sleep 조정, sec
sleep_time = 0

# time format
time_format = '%Y-%m-%d %H:%M:%S'
# methods =============================================================================================================


# conn 만들고 request 하는 것 모두를 관리함.
def req(url):
    try:
        conn = HTTPSConnection(fred_domain)
        conn.request("GET", url)
        res = conn.getresponse()
        return json.loads(res.read().decode('utf-8'))
    except:
        print('[exception url]', url, traceback.format_exc())
        #traceback.print_stack()
        #req(url)


# db 넣기전 표준화
def to_stand_series_meta(js):

    if not js:
        return

    id = js['id']
    js['id'] = 'FRED_' + id
    js['name'] = js.pop('title')
    js['agency_id'] = 'FRED'
    js['dataset_id'] = id
    js['frequency'] = js.pop('frequency_short', '')
    js['adjustment'] = js.pop('seasonal_adjustment_short', '')
    js['area_id'] = ''
    # js['unit'] = js.pop('units_short')
    js['unit_name'] = js.pop('units', '')
    js['obs_start'] = js.pop('observation_start')
    js['obs_end'] = js.pop('observation_end')
    d = js.pop('last_updated', '')
    if d:
        update_time = datetime.strptime(d[:d.rfind('-')], time_format) + timedelta(hours=9)
        js['last_update'] = update_time.strftime(time_format)
    else:
        js['last_update'] = ''

    js['note'] = js.pop('notes','')

    js.pop('realtime_start', '')
    js.pop('realtime_end', '')
    js.pop('units_short', '')
    js.pop('seasonal_adjustment', '')
    js.pop('popularity', '')


def to_stand_observ(js, id):

    if not js:
        return

    js['id'] = 'FRED_' + id

    js.pop('realtime_start', '')
    js.pop('realtime_end', '')
    js.pop('observation_start', '')
    js.pop('observation_end', '')
    js.pop('units', '')
    js.pop('output_type', '')
    js.pop('file_type', '')
    js.pop('order_by', '')
    js.pop('sort_order', '')
    js.pop('count', '')
    js.pop('offset', '')
    js.pop('limit', '')
    data_list = js.pop('observations', [])

    for data in data_list:
        data.pop('realtime_start')
        data.pop('realtime_end')

    js['observations'] = data_list
    # try:
    #     js['note'] = js.pop('notes')
    # except Exception:
    #     js['note'] = ''


# init 시 파일 지우기
def delete_init_files(path):
    if is_clean:
        for the_file in os.listdir(path):
            file_path = os.path.join(path, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    delete_init_files(file_path)
                #elif os.path.isdir(file_path): shutil.rmtree(file_path)
            except Exception as e:
                print(e)


# update 시 파일 지우기
# init은 is_clean으로 완전 지우고 다시 시작할 여부가 제공되지만
# update 는 무조건 지운다. crawl 시점이 초기화다 디비적재 기준이 아님..
def delete_update_files(path):
    for the_file in os.listdir(path):
        file_path = os.path.join(path, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                delete_update_files(file_path)
            #elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)

