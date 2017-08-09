import json

# urls= ==============================================================================================================

api_key = 'your_api_key'

# url #
fred_domain = 'api.stlouisfed.org'
fred_root = 'https://api.stlouisfed.org'

fred_common_url = '?api_key='+api_key+'&file_type=json'

# fred_cate_child_url -> categories.csv(cate_id list), categories.json (cate_id json array)
fred_cate_child_url = '/fred/category/children'+fred_common_url+'&category_id='

# fred_cate_series_url -> series.csv(series_id list), fred_cate_file_path/cate_id.json (cate 별 매핑된 session json)
fred_cate_series_url = '/fred/category/series'+fred_common_url+'&category_id='

# fred_series_observ_url -> fred_series_file_path/series_id.json (series 별 시계열 json)
fred_series_observ_url = '/fred/series/observations'+fred_common_url+'&series_id='

fred_series_update_url = '/fred/series/updates'+fred_common_url

# files ==============================================================================================================

# file path #
fred_ids_file_path = '../data/fred/ids/'
fred_cate_file_path = '../data/fred/category/'
fred_series_file_path = '../data/fred/series/'

# file #
fred_ids_file_cate_csv = fred_ids_file_path + 'categories.csv'
fred_ids_file_cate_json = fred_ids_file_path + 'categories.json'
fred_ids_file_series_csv = fred_ids_file_path + 'series.csv'
fred_ids_file_last_update_time = fred_ids_file_path + 'last_update_start_time.txt'

# 만들어지는 파일 순서대로 다시 정리

# 1. categories.csv(cate_id list)
# 2. categories.json (cate_id json array)
# 3. fred_cate_file_path/cate_id.json (cate 별 매핑된 session json)
# 4. fred_series_file_path/series_id.json (series 별 시계열 json)
# 5. series.csv(series_id list)

# methods =============================================================================================================

def req(conn, url):
    conn.request("GET", url)
    res = conn.getresponse()
    return json.loads(res.read().decode('utf-8'))

# tips ===============================================================================================================
"""업데이트 관련 : 금요일 오후 4~5시 까지 하고 업데이트 안함..
월요일 오전 6시부터 업데이트 시작...
주말은 업데이트를 안하는 것을 알 수 있는데 공휴일 처리는 어찌 될지 ...
어차피 매일 한번씩 업데이트 돌린다하면 신경 쓸 필요가 없긴 함..

하루 한번 돌린다는 가정하에
last_updated의 날짜가 이전날짜로 바뀌는 순간까지 update가 이루어 지도록 로직을 짜면 될 듯

최근 2주간의 업데이트 정보만을 보여주며 3만여건 정도됨
last_updated 값을 desc 하여 본결과 하루치 업데이트는 2000건 정도 임.

따라서 2주 이상 업데이트를 하지 못하게 된다면, 전체 데이터 쌓기를 또 해야 함.

또한 현재시간을 기준으로 api를 날리면, 가장 최근 업데이트 된 것이 14시간 전에 된 것을 보았는데, 항상 그런지는 모름.
"""

# 1. 하나의 cate 는 여러 seriess를 갖고, 하나의 seriess 는 여러 cate를 가진다. 즉 다대다 관계이다.
# 2. update api 는 seriess에 해당하는 cate를 제공하지 않는다.

# 위 두가지 이유로 인해, /카테고리id/seriessid.json 과 같은 구조로 경로를 구성할 수 없다.
# 따라서 그냥 카테고리id.json(하위 seriess 가짐), seriesid.json(하위 observ 가짐) 파일만 각 경로에 넣는다.

