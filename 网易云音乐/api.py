import requests
import execjs

with open('dome.js', mode='r', encoding='utf-8') as f:
    js = f.read()

url = 'https://music.163.com/weapi/song/enhance/player/url/v1'

cookies = {
}

headers = {
    'authority': 'music.163.com',
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'content-type': 'application/x-www-form-urlencoded',
    # 'cookie': '',
    'origin': 'https://music.163.com',
    'referer': 'https://music.163.com/',
    'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': '',
}

params = {
    'csrf_token': '',
}

music_id = 1830744059
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

response = requests.post(url=url, params=params, cookies=cookies, headers=headers, data=data, )
music_url = response.json()['data'][0]['url']
print(music_url)
