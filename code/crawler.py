import requests
import json
import pandas as pd

# nation_list = ['美国', '巴西', '印度', '阿根廷', '印度尼西亚', '俄罗斯', '英国', '法国', '加拿大', '德国']

def initiate_request(url, para):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Host': 'api.inews.qq.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36'
    }

    url = url + para
    res = requests.get(url=url, headers=headers)
    text = res.text

    return text

def json_data_parse_save(jsondata, nation):
    info_table = pd.DataFrame(columns=['year', 'date', 'confirm_add', 'confirm', 'heal', 'dead'])

    text = json.loads(jsondata)
    for i in text['data']:
        itemdic = {'year': i['y'], 'date': i['date'], 'confirm_add': i['confirm_add'], 'confirm': i['confirm'], 'heal': i['heal'], 'dead': i['dead']}
        info_table = info_table.append(itemdic, ignore_index=True)

    info_table.to_csv('../data/' + nation + '.csv', encoding='utf-8', index=False)

if __name__ == '__main__':
    nation_list = open('../dependence/新建文本文档.txt', encoding='utf-8').read().split('、')
    print(nation_list)
    for nation in nation_list:
        try:
            jsondata = initiate_request(url='https://api.inews.qq.com/newsqa/v1/automation/foreign/daily/list?country=', para=nation)
            json_data_parse_save(jsondata, nation)
            print('finished: ', nation)
        except:
            pass