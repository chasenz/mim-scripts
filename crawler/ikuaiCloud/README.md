# ikuai 技术云盘 - 批量下载脚本

[ikuai技术云盘](http://ikuai9.com:555/home.html)保存有爱快技术文档，实用工具，系统文件等，该文件云盘不具有文件夹直接下载的功能，且文件下载地址没有放置于html源码中，无法用IDM或其他工具抓取页面数据进而批量下载，因此需要手动编写脚本批量下载。

## 实现方法

### 获取文件和文件夹内容

文件和文件夹都有对应ID，向`http://ikuai9.com:555/homeController/getFolderView.ajax` POST请求文件夹ID，可以获取到当前目录下的文件和目录信息。 向`http://ikuai9.com:555/homeController/downloadFile.do?fileId=` GET请求文件ID，可以下载到文件。

### 工作流程

- 创建一个ID池（id_pool），存放文件和目录信息，包含ID，类型，名称和上级目录
- 创建线程读取ID池，如果类型为文件则执行下载操作，反之为目录执行POST请求获取该目录下的文件和目录信息，并将信息保存到ID池中
- 下载操作会调用系统中的IDM，如果用原生的requests下载，速度感人，IDM可以极大解决下载中的诸多问题，个人感觉胜于`wget`库

创建多线程执行上述操作

## 技术总结

> 该脚本对于多线程下载有比较大的要求，如果自己造轮子效果可能难以超越IDM。
> 
Python调用IDM方法：

![20210127224558](https://raw.githubusercontent.com/chasenz/PicGo/main/images/20210127224558.png)

实例一 os.system()
```python
def IDMdownload(DownUrl, DownPath, FileName):
    IDMPath = "D:\下载工具\IDM6.31.3\Internet Download Manager\\"
    os.chdir(IDMPath)
    IDM = "IDMan.exe"
    command = ' '.join([IDM, '/d', DownUrl, '/p', DownPath, '/f', FileName, '/q', '/n'])
    print(command)
    os.system(command)
```

实例二 subprocess
```python
from subprocess import call

def IDMdown(DownUrl, DownPath, FileName):
    IDMPath = "D:\下载工具\IDM6.31.3\Internet Download Manager\\"
    os.chdir(IDMPath)
    IDM = "IDMan.exe"
    call([IDM, '/d', DownUrl, '/p', DownPath, '/f', FileName, '/q', '/n'])
    call([IDM, '/s'])
```

在IDM设置项目中，进入下载-自定义下载进度对话框-编辑-启动界面-不显示，这样可以减少IDM的不必要弹窗，让它安静地在后台下载。

这样还是无法避免所有弹窗，如果文件名冲突也会弹出提示，如果下载太慢或者失败也会弹窗，这里还需要优化。