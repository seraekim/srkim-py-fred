# from common.config import *
# urls= ==============================================================================================================

api_key = 'api'

# url #
fred_domain = 'api.stlouisfed.org'
fred_root = 'https://api.stlouisfed.org'

fred_common_url = '?api_key='+api_key+'&file_type=json'

# fred_cate_child_url -> categories.csv(cate_id list), categories.json (cate_id json array)
fred_cate_child_url = '/fred/category/children'+fred_common_url+'&category_id='

# fred_cate_series_url -> series.csv(series_id list), fred_cate_file_path/cate_id.json (cate 별 매핑된 session json)
fred_cate_series_url = '/fred/category/series'+fred_common_url+'&category_id='

# fred_series_file_path/series_id.json (series meta json)
fred_series_url = '/fred/series'+fred_common_url+'&series_id='

# fred_series_observ_url -> fred_observ_file_path/series_id.json (series 별 시계열 json)
fred_series_observ_url = '/fred/series/observations'+fred_common_url + '&series_id='
# 빈티지 모니터링 해볼거라면.. &realtime_start=yyyy-mm-dd 추가
#fred_series_observ_url = '/fred/series/observations'+fred_common_url + '&realtime_start=2017-08-01&series_id='

fred_series_update_url = '/fred/series/updates'+fred_common_url

# files ==============================================================================================================

# file path #
_home = 'l:/python'  # get_config('local', 'HOME')
_init = _home + '/data/fred/init/'
_update = _home + '/data/fred/update/'

init_ids_path = _init + 'ids/'
init_cate_path = _init + 'category/'

init_series_path = _init + 'series/'
init_observ_path = init_series_path + 'observ/'

# update 경로, seriess 메타 및 observations
update_series_path = _update + 'series/'
update_observ_path = update_series_path + 'observ/'

# parsed 경로
parsed_init_series_path = str.replace(init_series_path, '/data/', '/parsed/')
parsed_init_observ_path = str.replace(init_observ_path, '/data/', '/parsed/')
parsed_update_series_path = str.replace(update_series_path, '/data/', '/parsed/')
parsed_update_observ_path = str.replace(update_observ_path, '/data/', '/parsed/')

# file #
ids_cate_csv = init_ids_path + 'categories.csv'
ids_cate_json = init_ids_path + 'categories.json'
ids_series_csv = init_ids_path + 'series.csv'
last_update_time = _update + 'last_update_start_time.txt'

