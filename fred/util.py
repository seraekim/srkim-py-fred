"""
마지막 업데이트 : 2017-09-13
파일명 : util.py

스레드 수, 타임포맷, 파일삭제여부 변수를 관리하며,
공통적으로 사용되는 메소드를 관리한다.
"""
from http.client import HTTPSConnection
from fred.path import fred_domain
import json
import os
import traceback
from datetime import datetime, timedelta
from pymongo import MongoClient
from common.config import *

# var ======================

# active thread count 조정
concurrent = 200

# thread sleep 조정, sec
sleep_time = 0

# time format
time_format = '%Y-%m-%d %H:%M:%S'
# methods =====================================================


# conn 만들고 request 하는 것 모두를 관리함.
def req(url):
    try:
        conn = HTTPSConnection(fred_domain)
        conn.request("GET", url)
        res = conn.getresponse()
        return json.loads(res.read().decode('utf-8'))
    except:
        print('[exception url]', url, traceback.format_exc())
        return {}
        #traceback.print_stack()
        #req(url)


# db 넣기전 표준화
def to_stand_series_meta(js):

    if not js:
        return

    new_js = {}
    id = js['id']
    new_js['_id'] = 'FRED_' + id
    new_js['name'] = js.pop('title', '')
    new_js['agency_id'] = 'FRED'
    new_js['dataset_id'] = id
    new_js['frequency'] = js.pop('frequency_short', '')
    new_js['adjustment'] = js.pop('seasonal_adjustment_short', '')
    new_js['area_id'] = js.pop('geo', '')
    new_js['unit_name'] = js.pop('units', '')
    new_js['obs_start'] = js.pop('observation_start', '')
    new_js['obs_end'] = js.pop('observation_end', '')
    d = js.pop('last_updated', '')
    if d:
        update_time = datetime.strptime(d[:d.rfind('-')], time_format) + timedelta(hours=9)
        new_js['last_update'] = update_time.strftime(time_format)
    else:
        new_js['last_update'] = ''

    new_js['note'] = js.pop('notes', '')

    js.clear()
    js.update(new_js)


def to_stand_observ(js, id):

    if not js:
        return

    js['_id'] = 'FRED_' + id

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
        data['period'] = data.pop('date')
        data['value'] = data.pop('value')
        data.pop('realtime_start')
        data.pop('realtime_end')

    js['observations'] = data_list


# init 시 파일 지우기
def delete_init_files(path, is_clean=False):
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


def mongo_insert_many(collection_name, js):
    mongo_conf = get_config('product', key='mongo')
    with MongoClient(mongo_conf['host'], mongo_conf['port']) as mongo:
        db = mongo['fred']
        collection = db[collection_name]
        print('mongo insert start:', collection_name)
        collection.insert_many(js)
        print('mongo insert end:', collection_name)


def mongo_upsert(collection_name, js):
    mongo_conf = get_config('product', key='mongo')
    with MongoClient(mongo_conf['host'], mongo_conf['port']) as mongo:
        db = mongo['fred']
        collection = db[collection_name]
        print('mongo upsert start:', collection_name)
        for j in js:
            if collection.find({'_id': j['_id']}).count():
                collection.update_one({'_id': j['_id']}, {'$set': j})
            else:
                collection.insert_one(j)
        print('mongo upsert end:', collection_name)


def mongo_upsert(db_name, js):
    mongo_conf = get_config(key='mongo')
    with MongoClient(mongo_conf['host'], mongo_conf['port']) as mongo:
        db = mongo['fred']
        collection = db[db_name]
        if isinstance(js, list):
            for j in js:
                collection.update_one({'_id': j['_id']}, {"$set": j}, upsert=True)
        else:
            collection.update_one({'_id': js['_id']}, {"$set": js}, upsert=True)


def mongo_bulk_upsert(bk, js):
    if isinstance(js, list):
        for j in js:
            bk.find({'_id': j['_id']}).upsert().update({"$set": j})
    else:
        bk.find({'_id': js['_id']}).upsert().update({"$set": js})
