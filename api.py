from http.client import HTTPConnection
import json

# 간이 파일 서버 테스를 위해...
# browsepy 127.0.0.1 8080 --directory D:/srkim/python/project/data

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

