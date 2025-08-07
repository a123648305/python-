import requests
from bs4 import BeautifulSoup



def save_html(html, path):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)


def get_html(url):
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "en,zh-CN;q=0.9,zh;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "priority": "u=0, i",
        "sec-ch-ua": "\"Not)A;Brand\";v=\"8\", \"Chromium\";v=\"138\", \"Microsoft Edge\";v=\"138\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "cross-site",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1"
    }
    response = requests.get(url)
    # 检查请求是否成功
    if response.status_code == 200:
        # 解析网页内容
        soup = BeautifulSoup(response.text, 'html.parser')
        # save_html(soup.text, 'jin10.txt')
        #print(soup)
        # 提取名言和作者
        quotes = soup.find_all('div', class_='quote')
        
       

        for quote in quotes:
            text = quote.find('span', class_='text').text
            author = quote.find('small', class_='author').text
            print(f'名言: {text}')
            print(f'作者: {author}\n')
    else:
        print(f'请求失败，状态码: {response.status_code}')


# get_html('https://www.jin10.com/')
# get_html('https://www.toutiao.com/')


import json
import time

def fetch_hotboard():
    url = 'https://www.toutiao.com/hot-event/hot-board/'
    params = {
        'origin': 'toutiao_pc',
        '_signature': '_02B4Z6wo00f01pOGVHQAAIDBBqmXHjM78a6TolDAAMx0xx8WLJpWWrvhqjrX8Pe4HwnfUNS0EfwRGgKPyMwSU5iMa5nhJh0uOWS5sPsr4ZgR.86IXbREVaYUyXV3AE4xuhMSRr0RT9ON4yfTa3',
    }
    response = requests.get(url,params=params)
    if response.status_code == 200:
        result = ''
        list = json.loads(response.text)
        for item in list['data']:
            str =  f"{time.strftime('%Y-%m-%d %H:%M:%S')} : {item['Title']}\n"
            print(str)
            result += str
        save_html(result,'toutiao.txt')



# get_html('https://www.toutiao.com/')




import time
import threading

def task():
    """要定时执行的任务"""
    print("任务执行中...", time.strftime("%H:%M:%S"))
    # 再次启动定时器（实现循环执行）
    fetch_hotboard()
    threading.Timer(1, task).start()

task()