import json
import os
import requests
import logging
import threading
import wget

# iKuai Cloud Homepage
# http://ikuai9.com:555/home.html
save_path = os.getcwd()
url = 'http://ikuai9.com:555/homeController/getFolderView.ajax'
download_url = 'http://ikuai9.com:555/homeController/downloadFile.do?fileId='

def IDMdownload(DownUrl, DownPath, FileName):
    IDMPath = "C:\Program Files (x86)\Internet Download Manager"
    os.chdir(IDMPath)
    IDM = "IDMan.exe"
    command = ' '.join([IDM, '/d', DownUrl, '/p', DownPath, '/f', FileName, '/q', '/n'])
    print(command)
    os.system(command)

class ikuaiDownloader:
    id_pool = []
    rlock = threading.RLock()

    def __init__(self, root_fid, threadNum):
        self.root_fid = root_fid
        self.threadNum = threadNum

    def getHTMLText(self, fid):
        try:
            r = requests.post(url, data={'fid':fid}, timeout=60)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            return r.text
        except Exception as e:
            logging.exception(e)

    def fillIdPoolList(self, html, cur_path):
        print(html)
        file_json = json.loads(html)
        logging.info(file_json)
        folder_name = file_json['folder']['folderName']

        # Parse fileList
        for file in file_json['fileList']:
            cur_dic = {}
            cur_dic['fid'] = file['fileId']
            cur_dic['type'] = 'file'
            cur_dic['fname'] = file['fileName']
            cur_dic['parent'] = os.path.join(cur_path, folder_name)
            self.id_pool.append(cur_dic)

        # Parse folderList
        for folder in file_json['folderList']:
            cur_dic = {}
            cur_dic['fid'] = folder['folderId']
            cur_dic['type'] = 'folder'
            cur_dic['fname'] = folder['folderName']
            cur_dic['parent'] = os.path.join(cur_path, folder_name)
            self.id_pool.append(cur_dic)

    def downloader(self, cur_dic):
        print("downlong:" + cur_dic['fname'])
        file_url = download_url + cur_dic['fid']
        folder_path = os.path.join(save_path, cur_dic['parent'])
        file_svae_path = os.path.join(folder_path, cur_dic['fname'])
        # r = requests.get(file_url)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        # with open(file_svae_path, 'wb') as f:
        #     f.write(r.content)
        try:
            # wget.download(file_url, file_svae_path)
            IDMdownload(file_url, folder_path, cur_dic['fname'])
        except Exception as e:
            print(e)
        print("finished:" + cur_dic['fname'])

    def run_fillpool(self):
        while True:
            print(self.id_pool)
            ikuaiDownloader.rlock.acquire()
            if len(self.id_pool) == 0:
                if len(self.root_fid) != 0:
                    html = self.getHTMLText(self.root_fid)
                    self.fillIdPoolList(html, '')
                    self.root_fid = ''
                    ikuaiDownloader.rlock.release()
                else:
                    ikuaiDownloader.rlock.release()
                    break
            else:
                cur_dic = self.id_pool.pop()
                # Download file
                if cur_dic['type'] == 'file':
                    ikuaiDownloader.rlock.release()
                    self.downloader(cur_dic)
                # Traverse folder
                else:
                    html = self.getHTMLText(cur_dic['fid'])
                    self.fillIdPoolList(html, cur_dic['parent'])
                    ikuaiDownloader.rlock.release()

    def run(self):
        logging.info("Creating Running Thread")
        for run_th in range(self.threadNum):
            run_add_th = threading.Thread(target=self.run_fillpool())
            run_add_th.start()

if __name__ == '__main__':
    ikuai = ikuaiDownloader(root_fid='root', threadNum=10)
    ikuai.run()