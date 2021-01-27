import json
import time
import logging
import pymysql
import threading
import requests
from queue import Queue
import sys
dbhost={
        "host":"127.0.0.1",
        "dbname":"maxplus",
        "user":"maxplus",
        "password":"max+"
    }

base_url="http://news.maxjia.com/"

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(threadName)s %(message)s')

class MaxProfileCrawler():
    jsonText = ''
    user_val = ()
    max_id = ''
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }

    def __init__(self, max_id, timeout):
        self.timeout = timeout
        self.max_id = str(max_id)

    def getProfileJson(self):
        url = base_url + "/bbs/app/profile/user/profile?&userid=" + self.max_id
        try:
            r = requests.get(url, timeout=self.timeout, headers=self.headers)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            self.jsonText = r.text
        except Exception as e:
            logging.error("request failed")
            return None

    def parseProfileJson(self):
        if(self.jsonText == ''):
            return None
        profile_json = json.loads(self.jsonText)
        status = profile_json['status']
        if (status == "failed"):
            logging.error("status failed")
            return None
        max_name = profile_json['user']['username']
        is_binded_steam_id = profile_json['bind_info']['steam']['is_binded_steam_id']
        if (max_name == "匿名玩家" and is_binded_steam_id == 0):
            logging.error("max_id不存在")
            return None
        try:
            max_id = profile_json['user']['userid']
            max_avatar_url = profile_json['user']['avartar']
            max_signature = profile_json['user']['signature']
            max_sex = profile_json['user']['sex']
            post_link_num = profile_json['user']['post_link_num'] if 'post_link_num' in profile_json else "0"
            news_comment_num = profile_json['user']['news_comment_num'] if 'news_comment_num' in profile_json else "0"
            post_comment_num = profile_json['user']['post_comment_num'] if 'post_comment_num' in profile_json else "0"
            qalink_answer_num = profile_json['user']['qalink_answer_num'] if 'qalink_answer_num' in profile_json else "0"
            steam_id = profile_json['bind_info']['steam']['steam_id']
            is_verified_steam_id = profile_json['bind_info']['steam']['is_verified_steam_id']
            steam_name = profile_json['bind_info']['steam']['personaname'] if 'personaname' in profile_json else ""
            realname = profile_json['bind_info']['steam']['realname'] if 'realname' in profile_json else ""
            steam_avatar_url = profile_json['bind_info']['steam']['avatar_url']

            self.user_val = (max_id, max_name, max_avatar_url, max_signature, max_sex, post_link_num, news_comment_num, post_comment_num, qalink_answer_num,
                             steam_id, is_verified_steam_id, is_binded_steam_id, steam_name, realname, steam_avatar_url)
        except Exception as e:
            logging.error(e)
            return None

    def insertProfile(self):
        if(len(self.user_val) == 0):
            return None
        db = pymysql.connect(dbhost.get("host"), dbhost.get("user"), dbhost.get("password"), dbhost.get("dbname"))
        cursor = db.cursor()

        sql = "INSERT IGNORE INTO mp_user (max_id, max_name, max_avatar_url, max_signature, max_sex, post_link_num, news_comment_num, post_comment_num, qalink_answer_num," \
              "steam_id, is_verified_steam_id, is_binded_steam_id, steam_name, realname, steam_avatar_url) " \
              "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

        try:
            # 执行sql语句
            cursor.execute(sql, self.user_val)
            # 提交到数据库执行
            db.commit()
        except:
            # 如果发生错误则回滚
            db.rollback()

        # 关闭数据库连接
        db.close()

    def run(self):
        self.getProfileJson()
        self.parseProfileJson()
        self.insertProfile()
        time.sleep(0.05)

lock = threading.Lock()
queue = Queue()
numTag = 0
def print_num(item):
    # 声明numTag是全局变量，所有的线程都可以对其进行修改
    global numTag
    with lock:
        numTag += 1
        percent = numTag*100 / 9899999
        # 输出的时候加上'\r'可以让光标退到当前行的开始处，进而实现显示进度的效果
        logging.info('\rQueue Item: {0}\tNumTag:{1:.5f}%'.format(str(item), percent))

def thread_run():
    while True:
        max_id = queue.get()
        if max_id is None:
            break
        else:
            mpc = MaxProfileCrawler(max_id=max_id, timeout=5)
            mpc.run()
            print_num(max_id)


if __name__ == '__main__':
    start = int(sys.argv[1])
    numTag = int(sys.argv[1])
    for id in range(start,10000000):
        queue.put(id)

    for num in range(20):
        threadName = "Thread_" + str(num)
        thread = threading.Thread(target=thread_run, name= threadName)
        thread.start()
