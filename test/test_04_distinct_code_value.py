import json
import os

series_file_list = os.listdir(fred_series_file_path)
f_list = []
u_list = []
s_list = []

for fname in series_file_list:
    if fname.endswith(".json"):
        with open(fred_series_file_path + fname) as f:
            try:
                js = json.loads(f.read())
                js2 = js['series_attr']
                #to_stand_json(js)
                f = js['frequency'] + '|' + js2['frequency_short']
                u = js['unit'] + '|' + js2['units_short']
                s = js['seasonal_adjustment'] + '|' + js2['seasonal_adjustment_short']

                f_list.append(f)
                u_list.append(u)
                s_list.append(s)

                print(f)
            except:
                print('[error]', fname)


with open(fred_ids_file_path + 'short_map.txt', 'w', encoding='utf-8') as f:
    for sub in sorted(set(f_list)):
        f.write("%s\n" % sub)

    f.write('\n')
    f.write('\n')
    for sub in sorted(set(u_list)):
        f.write("%s\n" % sub)

    f.write('\n')
    f.write('\n')
    for sub in sorted(set(s_list)):
        f.write("%s\n" % sub)


print()
print()
