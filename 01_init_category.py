from http.client import HTTPSConnection
from config import *

# 테스트 용으로, 값을 넣으면 해당 숫자만큼만 category id를 가져옴.
# 테스트가 아니라면 None을 입력
# category_limit = None
category_limit = 200

cnt = 0
cate_id_list = []
cate_json_list = []

conn = HTTPSConnection(fred_domain)


def categories(cate_id):

    global cnt
    global cate_json_list
    ret = req(conn, fred_cate_child_url + str(cate_id))['categories']

    if len(ret):
        cate_id_list.append(cate_id)
        cate_json_list.append(ret)
        cnt += 1
        print('[cate] %d cate_id: %d, child cnt: %d' % (cnt, cate_id, len(ret)))
        for sub in ret:
            if category_limit and cnt == category_limit:
                break
            # time.sleep(.200)
            categories(sub['id'])


# 크롤링 시작
categories(0)

# 카테고리 ID 값만 리스트 저장
with open(fred_ids_file_cate_csv, 'w', encoding='utf-8') as f:
    for cate_id in sorted(set(cate_id_list)):
        f.write("%s\n" % cate_id)

# 카테고리 ID JSON Array 저장
with open(fred_ids_file_cate_json, 'w', encoding='utf-8') as f:
    f.write(json.dumps(cate_json_list))

