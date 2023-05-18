import requests
import parsel
from urllib.parse import urljoin
import os
import shutil
import re

if os.path.exists('img'):
    shutil.rmtree('img')

if not os.path.exists('img'):
    os.mkdir('img')

for page in range(2, 4 + 1):
    url = f'http://www.netbian.com/index_{page}.htm'
    try:
        home_url = 'http://www.netbian.com/'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
        }
        response = requests.get(url=url, headers=headers)
        response = parsel.Selector(text=response.text)

        images_href = response.css('.list > ul > li > a::attr(href)').getall()
        for image in images_href:
            images_url = urljoin(home_url, image)

            response = requests.get(url=images_url, headers=headers)
            response = parsel.Selector(text=response.text)

            pic = response.css('.pic > p > a::attr(href)').get()
            pic = urljoin(home_url, pic)

            response = requests.get(url=pic, headers=headers)
            response = parsel.Selector(text=response.text)
            title = response.css('title::text').get()
            title = re.sub(r'[/\n\<>|":：*?# - - 【】]', '', title)

            img_url = response.xpath('//td[@align="left"]/a/@href').get()
            img = requests.get(url=img_url, headers=headers).content

            with open('img\\' + title + '.png', mode='wb') as f:
                f.write(img)
            print(title, img_url)
    except Exception as e:
        print(e)
        print('请输入正确')
