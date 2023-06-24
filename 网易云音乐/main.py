import requests
import execjs
import re
import os
import shutil

if os.path.exists(path='audio'):
    shutil.rmtree(path='audio')
os.mkdir(path='audio')

with open('dome.js', mode='r', encoding='utf-8') as f:
    js = f.read()

search = input('请输入需要搜索的歌曲: ')
print('\n')
url = 'https://music.163.com/weapi/cloudsearch/get/web'


def get_main(get_url, get_music_info):
    cookies = {

    }

    headers = {
        'authority': 'music.163.com',
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'content-type': 'application/x-www-form-urlencoded',
        # 'cookie': '',
        'origin': 'https://music.163.com',
        'referer': 'https://music.163.com/search/',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': '',
    }

    params = {
        # 如果是爬虫用户，知道可以填写(鉴别vip)
        'csrf_token': '',
    }

    key_info = execjs.compile(js).call('musicapi', music_info)

    data = {
        'params': f'{key_info[0]}',
        'encSecKey': f'{key_info[1]}',
    }

    response = requests.post(url=url, params=params, cookies=cookies, headers=headers, data=data)
    return response


def music_data(response):
    for music_data in response.json()['result']['songs']:
        author_name = music_data['ar'][0]['name']
        audio_name = music_data['name']
        audio_id = music_data['id']
        print('作者:', author_name, '歌曲名:', audio_name, '歌曲id', audio_id)


music_info = {
    "hlpretag": "<span class=\"s-fc7\">",
    "hlposttag": "</span>",
    "s": f"{search}",
    "type": "1",
    "offset": "0",
    "total": "true",
    "limit": "30",
    "csrf_token": ""
}

response = get_main(get_url=url, get_music_info=music_info)

music_data(response=response)

number = 30
try:
    while True:
        print('\n')
        user = input('如果需要请输入’下一页/歌曲链接: ')
        print('\n')
        if user == "下一页":
            music_info = {
                "hlpretag": "<span class=\"s-fc7\">",
                "hlposttag": "</span>",
                "s": f"{search}",
                "type": "1",
                "offset": f"{number}",
                "total": "false",
                "limit": "30",
                "csrf_token": ""
            }
            response = get_main(get_url=url, get_music_info=music_info)
            music_data(response=response)

            number += 30
        if user == "歌曲链接":
            while True:
                music_id = input('请输入上面选定的歌曲id: ')
                try:
                    music_info = {
                        "ids": f"[{music_id}]",
                        "level": "standard",
                        "encodeType": "aac",
                        "csrf_token": ""
                    }

                    key = execjs.compile(js).call('musicapi', music_info)

                    data = {
                        'params': f'{key[0]}',
                        'encSecKey': f'{key[1]}',
                    }

                    url = 'https://music.163.com/weapi/song/enhance/player/url/v1'
                    response = get_main(get_url=url, get_music_info=music_info)
                    music_url = response.json()['data'][0]['url']
                    print(music_url)

                    download = input('是否下载: ')
                    if download == "是":
                        response = requests.get(url=f'https://music.163.com/song?id={music_id}', headers={
                            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}).text
                        title = re.findall('<title>(.*?) - 单曲 - 网易云音乐</title>', response)[0]
                        content = requests.get(url=music_url).content
                        with open('audio\\' + title + '.mp3', mode='wb') as f:
                            f.write(content)
                            print('下载完成', '\n')
                            cont = input('是否继续获取歌曲链接: ')
                            if cont == '否':
                                exit()
                except Exception as e:
                    print('你输入的歌曲id有误', e)

except Exception as e:
    print('很抱歉,没有更多歌曲了/当前歌曲出现错误', e)
