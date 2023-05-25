import requests
import execjs
import json
import os
import shutil

a = 1
if os.path.exists('img'):
    shutil.rmtree('img')
os.mkdir('img')

dome = open('dome.js', mode='r', encoding='utf-8').read()
obj = execjs.compile(dome)

url = 'https://api.zzzmh.cn/bz/v3/getData'
headers = {
    'Referer': 'https://bz.zzzmh.cn/',
    'User-Agent': ''
}
json_dic = {
    """
        排序_sort: [0:推荐,1:最热,2:最新,3:随机]
        分辨率_resolution: [0:不限,1:1080p,2:2k,3:4k,4:8k]
        比例_ratio: [0:不限,1:1比1m,2:3比4,3:16比9,4:18比9,5:21比9,6:更大]
        分类_category: [0:不限,1:精选,2:人物,3:二次元]
        等等可以抓包https://api.zzzmh.cn/bz/v3/getData链接把json放到json_dic
        ……
    """
    'category': '0',
    'categoryId': '0',
    'color': '0',
    'current': '2',
    'ratio': '0',
    'resolution': '0',
    'size': '24',
    'sort': '0'
}
response = requests.post(url=url, headers=headers, json=json_dic)
result = response.json()['result']

result = obj.call('doc', result)
result = json.loads(result)
list_data = result['list']
for lis in list_data:
    i = lis['i']
    img_home_url = f'https://api.zzzmh.cn/bz/v3/getUrl/{i}29'

    content = requests.get(url=img_home_url, headers=headers)
    if content.status_code == 404:
        img_home_url = f'https://api.zzzmh.cn/bz/v3/getUrl/{i}19'
        content = requests.get(url=img_home_url, headers=headers)
    with open('img\\' + i + '.png', mode='wb') as f:
        f.write(content.content)
        print(a, img_home_url)
        a += 1
