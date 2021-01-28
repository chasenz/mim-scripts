from datetime import datetime
import requests
import logging
import json
import time
import random
import matplotlib.pyplot as plt
import numpy as np
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(threadName)s %(message)s')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
    'Accept': '*/*',
    'Accept-Language': 'zh,zh-CN;q=0.9,en;q=0.8,en-US;q=0.7',
    'Accept-Encoding': 'gzip, deflate'
}

daytime = [0 for i in range(24)]

"""
函数说明:获取用户Json格式数据
Parameters:
    url - 用户动态地址入口
Returns:
    text - 用户动态数据
Modify:
    2020-9-04
"""
def getUserData(url):
    try:
        r = requests.get(url, headers = headers)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except Exception as e:
        logging.error(e)
        return None

def parseUserJson(jstr):
    try:
        userJson = json.loads(jstr)
        nextUrl = userJson['paging']['next']
        return nextUrl, userJson
    except Exception as e:
        logging.error(e)
        return None

def storeData(userJson):
    for i in range(len(userJson['data'])):
        timeStamp = userJson['data'][i]['created_time']
        # verb = userJson['data'][i]['verb']
        hour = (int)(datetime.fromtimestamp(timeStamp).strftime('%H:%M:%S')[:2])
        daytime[hour] = daytime[hour] + 1


def main():
    baseUrl = "https://www.zhihu.com/api/v3/feed/members/sun-shao-jun-73/activities"
    while(True):
        userData = getUserData(baseUrl)
        baseUrl, userJson = parseUserJson(userData)
        storeData(userJson)
        print(daytime)
        if(userJson['paging']['is_end']):
            break
        time.sleep(random.uniform(1,2))

def showPlot():
    dayList = [339, 302, 279, 278, 314, 297, 233, 204, 178, 193, 192, 163, 102, 60, 26, 17, 13, 14, 58, 216, 570, 404, 408, 366]
    x = np.arange(24)
    plt.bar(x, height=dayList)
    plt.xticks(x, [i for i in range(24)])
    plt.show()

# main()
showPlot()