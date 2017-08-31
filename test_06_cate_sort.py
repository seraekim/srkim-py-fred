from config import *

cate_id_list = [int(line.rstrip('\n')) for line in open(fred_ids_file_path + 'category.csv')]

with open(fred_ids_file_cate_csv, 'w', encoding='utf-8') as f:
    for cate_id in sorted(set(cate_id_list)):
        f.write("%s\n" % cate_id)
