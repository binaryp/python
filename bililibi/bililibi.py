import requests
import parsel
import json
import subprocess
import shutil
import os
import re
from urllib.parse import urljoin
import time

url = input('网址: ')
headers = {
    'Cookie': '',
    'Referer': url,
    'User-Agent': ''
}

if os.path.exists('mp3'):
    shutil.rmtree(path='mp3')
if os.path.exists('mp4'):
    shutil.rmtree(path='mp4')

if not os.path.exists('mp3'):
    os.mkdir('mp3')
if not os.path.exists('mp4'):
    os.mkdir('mp4')
if not os.path.exists('video'):
    os.mkdir('video')


def one(url):
    response = requests.get(url=url, headers=headers)
    response = parsel.Selector(text=response.text)

    title = response.css('title::text').get()
    title = re.sub(r'[/\n\<>|":：*?# - - 【】]', '', title)
    files = os.listdir(path='video')
    if title + '.mp4' in files:
        print(f'重复标题  {title}  如果需要可以单独采集')
        pass

    elif title == "B读好书":
        bvid = url.split('video/')[1]
        url = f'https://www.bilibili.com/festival/bilibilibook?bvid={bvid}'

        response = requests.get(url=url, headers=headers)
        video_info = re.findall('"videoInfo":\{(.*?)}', response.text)[0]
        aid = re.findall('"aid":(.*?),"cid"', video_info)[0]
        cid = re.findall(',"cid":(.*?),"title":"', video_info)[0]
        title = re.findall(',"title":"(.*?)","bvid"', video_info)[0]
        title = re.sub(r'[/\n\<>|":：*?# - - 【】]', '', title)

        url = f'https://api.bilibili.com/x/player/playurl?avid={aid}&bvid={bvid}&cid={cid}&qn=80&fnver=0&fnval=4048&fourk=1&session=e3be23f5fa7cb593dbdbec32922579fc'
        response = requests.get(url=url, headers=headers).json()

        audio_url = response['data']['dash']['audio'][0]['baseUrl']
        video_url = response['data']['dash']['video'][0]['baseUrl']

        over(audio_url=audio_url, video_url=video_url, title=title)

    else:
        data_json = response.re_first('<script>window.__playinfo__=(.*?)</script>')
        try:
            data = json.loads(data_json)
            audio_url = data['data']['dash']['audio'][0]['baseUrl']
            video_url = data['data']['dash']['video'][0]['baseUrl']
        except:
            try:
                data_json = response.re_first('<script id="__NEXT_DATA__" type="application/json">(.*?)</script>')
                data = json.loads(data_json)
                aid = data['props']['pageProps']['dehydratedState']['queries'][0]['state']['data']['initSections'][0][
                    'epList'][0]['aid']
                cid = data['props']['pageProps']['dehydratedState']['queries'][0]['state']['data']['initSections'][0][
                    'epList'][0]['cid']

                url = f'https://api.bilibili.com//pgc/player/web/v2/playurl?support_multi_audio=true&avid={aid}&cid={cid}&qn=80&fnver=0&fnval=4048&fourk=1&gaia_source=&from_client=BROWSER&ep_id=703793'
                response = requests.get(url=url, headers=headers).json()

                audio_url = response['result']['video_info']['dash']['audio'][0]['baseUrl']
                video_url = response['result']['video_info']['dash']['video'][0]['baseUrl']
            except:
                try:
                    if 'video' in url:
                        bvid = url.split('video/')[1]
                    else:
                        bvid = re.findall(
                            'https://www\.bilibili\.com/festival/kaixuejiehuotujian\?bvid=(.*?)&spm_id_from=333\.999\.0.0',
                            url)[0]

                    response = requests.get(url=url, headers=headers)
                    data = \
                        re.findall('<script>window.__INITIAL_STATE__=\{(.*?)}};\(function\(\)\{var s;\(',
                                   response.text)[0]
                    data = re.findall('"videoInfo":\{"aid":(.*?),"cid":(.*?),"title":"(.*?)","bvid":"', data)[0]
                    url = f'https://api.bilibili.com/x/player/playurl?avid={data[0]}&bvid={bvid}&cid={data[1]}&qn=80&fnver=0&fnval=4048&fourk=1'
                    title = data[2]
                    title = re.sub(r'[/\n\<>|":：*?# - - 【】]', '', title)

                    response = requests.get(url=url, headers=headers)

                    audio_url = response.json()['data']['dash']['audio'][0]['baseUrl']
                    video_url = response.json()['data']['dash']['video'][0]['baseUrl']
                except:
                    if 'video' in url:
                        bvid = url.split('video/')[1]
                    else:
                        bvid = re.findall(
                            'https://www\.bilibili\.com/festival/talktalk\?bvid=(.*?)&spm_id_from=333\.999\.0\.0', url)[
                            0]

                    data = response.re_first('<script>window.__INITIAL_STATE__=\{(.*?)}};\(function\(\)\{var s;\(')
                    data = re.findall('"videoInfo":\{"aid":(.*?),"cid":(.*?),"title":"(.*?)","bvid":"', data)[0]

                    url = f'https://api.bilibili.com/x/player/playurl?avid={data[0]}&bvid={bvid}&cid={data[1]}&qn=80&fnver=0&fnval=4048&fourk=1&session=748f001adf2564f46e6d0f587b1a7248'
                    response = requests.get(url=url, headers=headers)
                    title = data[2]
                    title = re.sub(r'[/\n\<>|":：*?# - - 【】]', '', title)

                    audio_url = response.json()['data']['dash']['audio'][0]['baseUrl']
                    video_url = response.json()['data']['dash']['video'][0]['baseUrl']

        over(title=title, audio_url=audio_url, video_url=video_url)


def over(audio_url, video_url, title):
    audio = requests.get(url=audio_url, headers=headers).content
    with open('mp3\\' + title + '.mp3', mode='wb') as f:
        f.write(audio)
    video = requests.get(url=video_url, headers=headers).content
    with open('mp4\\' + title + '.mp4', mode='wb') as f:
        f.write(video)

    print('文件正在合并>>>')
    cmd = f'ffmpeg -i mp4\\{title}.mp4 -i mp3\\{title}.mp3 -c:v copy -c:a aac -strict experimental video\\{title}.mp4'
    subprocess.run(cmd, shell=True)

    print('爬取完成', title, audio_url, video_url)


def mover():
    shutil.rmtree(path='mp3')
    shutil.rmtree(path='mp4')


def all_get(url):
    response = requests.get(url=url, headers=headers).json()

    bvid = response['data']['list']['vlist']
    for bvid in bvid:
        bvid = bvid['bvid']
        url = urljoin('https://www.bilibili.com/video/', bvid)
        one(url=url)


if 'space' and 'id=0&pn=' in url:
    mid_page = re.findall('https://space\.bilibili\.com/(.*?)/video\?tid=0&pn=(.*?)&keyword=&order=pubdate', url)[0]

    url = f'https://api.bilibili.com/x/space/wbi/arc/search?mid={mid_page[0]}&ps=30&tid=0&pn={mid_page[1]}&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true'
    all_get(url=url)

elif 'space' in url:
    while True:
        uer = input('是否保存全部: ')
        mid = re.findall('https://space.bilibili.com/(.*?)/video', url)[0]

        if uer == '是':
            mid = re.findall('https://space.bilibili.com/(.*?)/video', url)[0]
            url = f'https://api.bilibili.com/x/space/wbi/arc/search?mid={mid}&ps=30&tid=0&pn=1&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true'
            response = requests.get(url=url, headers=headers).json()

            bvid = response['data']['list']['vlist'][0]['bvid']
            page = response['data']['page']['count']
            page = page / 30
            page = str(page)
            page_ = page.split('.')[0]
            if page.split('.')[1] != '0':
                page = int(page_) + 1
            else:
                page = int(page_)

            for page_int in range(1, page + 1):
                url = f'https://api.bilibili.com/x/space/wbi/arc/search?mid={mid}&ps=30&tid=0&pn={page_int}&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=aa5a14ae4b1cbb284837d4038edab3ea&wts=1684317227'
                time.sleep(10)
                all_get(url=url)

            break
        elif uer == '否':
            uer = input('自定义/首页: ')
            if uer == '首页':
                mid = re.findall('https://space.bilibili.com/(.*?)/video', url)[0]
                url = f'https://api.bilibili.com/x/space/wbi/arc/search?mid={mid}&ps=30&tid=0&pn=1&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true'
                all_get(url=url)

                break
            elif uer == '自定义':
                home = int(input('开始页: '))
                end = int(input('结束页: '))
                for page in range(home, end + 1):
                    url = f'https://api.bilibili.com/x/space/wbi/arc/search?mid={mid}&ps=30&tid=0&pn={page}&keyword=&order=pubdate&platform=web&web_location=1550101&order_avoided=true&w_rid=aa5a14ae4b1cbb284837d4038edab3ea&wts=1684317227'
                    all_get(url=url)

                break

            break
        else:
            print('请输入是/否')
            print('程序会在3秒后重新运行')
            time.sleep(3)

            continue

elif 'www.bilibili.com/' in url:
    if 'book' in url:
        bvid = url.split('bvid=')[1]
        url = urljoin('https://www.bilibili.com/video/', bvid)
    one(url=url)

mover()
