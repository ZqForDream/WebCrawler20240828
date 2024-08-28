# -*- coding:utf-8 -*-
"""
@SoftWare: PyCharm
@Project: WebCrawler20240828
@Author: 蜀山徐长卿
@File: main.py
@Time: 2024/8/28 14:36
"""
import os
import re

import requests

base_url = "https://samples.adsbexchange.com/"
paths = ["readsb-hist/"]
header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0"}
data_dir = 'data'


def func(url):
    response = requests.get(url, headers=header)
    if response.status_code == 200:
        re_results = re.findall(r'.+?\n<span class="name"><a href="(\d{2,4})/">(\d{2,4})/</a></span>\n.+?', response.text)
        re_results.sort(reverse=True)
        if len(re_results) > 0:
            for i in re_results:
                if len(i) == 2 and i[0] == i[1]:
                    value = i[0]
                    func(os.path.join(url, value) + '/')
        else:
            re_results = re.findall(r'.+?\n<span class="name"><a href="(.+?\.json\.gz)">(.+?\.json\.gz)</a></span>\n.+?', response.text)
            for i in re_results:
                if len(i) == 2 and i[0] == i[1]:
                    file_name = i[0]
                    rp = requests.get(os.path.join(url, file_name), headers=header)
                    if response.status_code == 200:
                        download_dir = os.path.join(data_dir, url.replace(base_url, '').replace('/', '\\'))
                        if not os.path.exists(download_dir):
                            os.makedirs(download_dir)
                        download_file = os.path.join(download_dir, file_name)
                        if os.path.exists(download_file):
                            print(f'{download_file} is exists, skip download')
                            continue
                        print(f'download {os.path.join(url, file_name)}')
                        with open(download_file, "wb") as f:
                            f.write(rp.content)


if __name__ == '__main__':
    for path in paths:
        func(os.path.join(base_url, path))
