# coding: utf-8
__author__ = 'ZFTurbo: https://kaggle.com/zfturbo'


from a1_common_functions import *
import requests
import zipfile


def update_current_data():
    store_file1 = INPUT_PATH + 'data_rus_latest.html'

    try:
        os.remove(store_file1)
    except:
        print('Already removed')

    download_url('https://xn--80aesfpebagmfblc0a.xn--p1ai/', store_file1)

    html = open(store_file1, 'r', encoding='utf8').read()
    search1 = '</svg></cv-map-virus><div class="d-map__list"><table><tr>'
    search2 = '</table></div></div></cv-popup>'
    r1 = html.find(search1)
    r2 = html.find(search2)
    if r1 == -1 or r2 == -1:
        print('Parse file failed!')
        exit()
    part = html[r1+len(search1):r2]
    part = part.split('<tr>')

    parsed_data = []
    for p in part:
        p = p.replace('</tr>', '')
        p = p.split('<td>')
        cleaned = []
        for p1 in p:
            p1 = p1.replace('<th>', '')
            p1 = p1.replace('</th>', '')
            p1 = p1.replace('</td>', '')
            p1 = p1.replace('<span class="d-map__indicator d-map__indicator_sick"></span>', '')
            p1 = p1.replace('<span class="d-map__indicator d-map__indicator_healed"></span>', '')
            p1 = p1.replace('<span class="d-map__indicator d-map__indicator_die"></span>', '')
            cleaned.append(p1)
        if len(cleaned) != 4:
            print('Incorrect length of list: {}'.format(cleaned))
            exit()
        for i in range(1, 4):
            cleaned[i] = int(cleaned[i])
        print(cleaned)
        parsed_data.append(cleaned)

    iso_names = get_russian_regions_names_v2()
    iso_names2 = get_russian_regions_names()
    out1 = open(FEATURES_PATH + 'time_table_flat_for_rus_latest_{}.csv'.format('confirmed'), 'w')
    out2 = open(FEATURES_PATH + 'time_table_flat_for_rus_latest_{}.csv'.format('deaths'), 'w')
    out1.write('name,date,cases\n')
    out2.write('name,date,cases\n')
    dt = datetime.datetime.now().strftime("%Y.%m.%d")
    for arr in parsed_data:
        name, confirmed, deaths = arr[0].strip(), int(arr[1]), int(arr[3])
        name2 = iso_names[name]
        for el in iso_names2:
            if iso_names2[el] == name2:
                name2 = el
                break
        out1.write('{},{},{}\n'.format(name2, dt, confirmed))
        out2.write('{},{},{}\n'.format(name2, dt, deaths))
        print(arr)
    out1.close()
    out2.close()


def check_if_updated():
    path1 = INPUT_PATH + 'time_series_covid19_confirmed_RU.csv'
    path2 = FEATURES_PATH + 'time_table_flat_for_rus_latest_{}.csv'.format('confirmed')
    s1 = pd.read_csv(path1)
    latest_date1 = s1.columns.values[-1]
    s2 = pd.read_csv(path2)
    latest_date2 = sorted(list(s2['date'].unique()))[-1]

    part1 = s1[s1['Combined_Key'] == 'Moscow,Russia'][latest_date1].values[0]
    part2 = s2[s2['name'] == 'Moscow_Russia']['cases'].values[0]
    print('Value for Moscow in {} and last date {}: {}'.format(os.path.basename(path1), latest_date1, part1))
    print('Value for Moscow in {} and last date {}: {}'.format(os.path.basename(path2), latest_date2, part2))
    if part2 > part1:
        print('Looks OK')
    else:
        print('Failed! Looks like you need to wait')


if __name__ == '__main__':
    update_current_data()
    check_if_updated()