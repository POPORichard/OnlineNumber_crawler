import threading

import requests
import re
import time
from bs4 import BeautifulSoup

List = [
    {'platform': 'bilibili', 'name': '姥爷互殴模拟器', 'url': 'https://live.bilibili.com/737562'}
]

Platform_List = {
    'bilibili': 180
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/71.0.3578.98 Safari/537.36'
}


def write(file_name, online_num):
    file = open('data/' + file_name + '.txt', 'a')
    data = str(time.time()) + ':' + str(online_num) + '\n'
    file.write(data)


def get_online_num_func(platform, response):
    func = {
        'bilibili': re.search(r'"online":(.+?),', response.text),
    }
    online = func.get(platform, "unknown platform")
    if online:
        return online.group(1)
    else:
        return -1


def get_online_num(webcast_msg):
    response = requests.get(webcast_msg['url'], headers=headers)
    response.encoding = 'uft8'
    write(webcast_msg['name'], get_online_num_func(webcast_msg['platform'], response))


def limiter(webcast_msg, sleep_time):
    while True:
        get_online_num(webcast_msg)
        time.sleep(sleep_time)


def main(webcast_list, platform_list):
    for i in webcast_list:
        sleep_time = platform_list[i['platform']]
        t = threading.Thread(target=limiter, args=(i, sleep_time))
        t.start()


if __name__ == '__main__':
    main(List, Platform_List)
