"""
마지막 업데이트 : 2017-09-13
파일명 : api.py

파일서버로 부터 REST 서비스가 제공된다 가정하고 만든 파이선 전용 api 이다.
몽고디비 또는 검색엔진 등을 활용하게 되면 어차피 처음부터 만들어야 할 것이다.
"""
from http.client import HTTPConnection
import json

# 간이 파일 서버 테스를 위해...
# browsepy 127.0.0.1 8080 --directory D:/srkim/python/project/data
# db에 넣어서 서비스하게 되면 url 경로등은 무조건 바뀔 것...

conn = HTTPConnection('localhost:8080')


def req(url):
    conn.request("GET", url)
    res = conn.getresponse()
    return json.loads(res.read().decode('utf-8'))


def get_cate(cate_id='100'):
    return req('open/fred/category/%s.json' % cate_id)


def get_series_meta(series_id=''):
    return req('open/fred/series/%s.json' % series_id)


def get_series_observ(series_id=''):
    return req('open/fred/series/observ/%s.json' % series_id)

