import requests
import re
import shutil
import os
import json
import parsel
from tqdm import tqdm

if os.path.exists('video'):
    shutil.rmtree(path='video')

os.mkdir('video')

top_url = 'https://www.acfun.cn'
headers = {
    'Referer': 'https://www.acfun.cn/',
    'User-Agent': ''
}


def one(url):
    response = requests.get(url=url, headers=headers)
    title = re.findall('<title >(.*?)</title>', response.text)[0]
    title = re.sub(r'[\n\\/:*?<>|]', '', title)
    if title in os.listdir(path='video'):
        pass
    else:
        data = re.findall('window.pageInfo = window.videoInfo = \{(.*?)};', response.text)[0]
        data = '{' + data + '}'

        data = json.loads(data)
        json_data = data['currentVideoInfo']['ksPlayJson']

        ksplay = json.loads(json_data)

        play_url = ksplay['adaptationSet'][0]['representation'][0]['url']
        print('请耐心等待，正在爬取', title)
        # play_url = ksplay['adaptationSet'][0]['representation'][0]['backupUrl'][0]

        url_home = play_url.split('m3u8')[0]
        response = requests.get(url=play_url, headers=headers)
        lis = re.sub('#.*', '', response.text).split()
        for li in tqdm(lis):
            li = re.findall('\.(.*)', li)[0]

            url = url_home + li

            response = requests.get(url=url, headers=headers)
            with open('video\\' + title + '.mp4', mode='ab') as f:
                f.write(response.content)
        print('爬取完成', title, '\n')


def page_(url, page):
    url = f'{url}?quickViewId=ac-space-video-list&reqID=1&ajaxpipe=1&type=video&order=newest&page={page}&pageSize=20'
    response = requests.get(url=url, headers=headers)
    response = re.sub('/\*<!-- fetch-stream -->\*/', '', response.text)
    response = json.loads(response)
    data = response['html']
    data = parsel.Selector(text=data)

    href = data.css('.ac-space-video.weblog-item::attr(href)').getall()
    for href in href:
        url = top_url + href
        one(url=url)


url = input('网址: ')

if 'www.acfun.cn/v/' in url:
    one(url=url)
elif 'www.acfun.cn/u/' in url:
    response = requests.get(url=url, headers=headers)
    span = re.findall('视频<span>(.*?)</span>', response.text)[0]
    page = int(span) / 20
    if int(str(page).split('.')[1]) > 1:
        page = int(str(page).split('.')[0]) + 1
    else:
        page = int(str(page).split('.')[0])

    user = input('全部/自定义: ')
    if user == '全部':
        for page in range(1, page + 1):
            page_(url=url, page=page)

            print('第二页')
    elif user == '自定义':
        home = int(input('起始页: '))
        end = int(input('结束页: '))
        for page in range(home, end + 1):
            page_(url=url, page=page)
