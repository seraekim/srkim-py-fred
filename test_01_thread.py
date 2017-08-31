from threading import Thread
import http.client
from queue import Queue

concurrent = 200


def run():
    while True:
        url = q.get()
        conn = http.client.HTTPSConnection('api.stlouisfed.org')
        conn.request("GET", url)
        res = conn.getresponse()
        print(res.read())
        q.task_done()


q = Queue(concurrent * 2)
for i in range(concurrent):
    t = Thread(target=run)
    t.daemon = True
    t.start()

path = '/fred/series/observations?api_key=831824c743ac50595faa38ddd29ae7c5&file_type=json&series_id='

for url in [path+'EQTA',path+'EQTA']:
    q.put(url)

q.join()

