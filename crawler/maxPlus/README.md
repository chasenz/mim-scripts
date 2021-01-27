# MAX+ - 用户反查

MAX+ 社区是针对DOTA2和CSGO玩家的数据统计平台，同时也是玩家交流的论坛。用户可以根据steam id，steam 名称查询个人战绩，或者通过MAX+ 用户主界面查看游戏的数据。但是MAX+无法直接通过steam id查找到对应的MAX+账户，这样设计应该是为了保护用户隐私。

有时候游戏中和别人对喷，但碍于无法从STEAM账户中获取有效信息，从MAX+社区是个不错的方法，但前面也说了，steam id无法直接查找到MAX+用户，MAX+用户主页可以显示STEAM账户，所以用户反查思路就是遍历所有社区用户，绑定MAX+ ID和STEAM ID，~~便于以后游戏对喷完可以社工玩家。~~

## 实现方法

根据抓包分析，MAX+的用户接口没有鉴权，也就是没有登录的用户也可以使用搜索接口。

接口案例：[http://news.maxjia.com/bbs/app/profile/user/profile?&userid=1083123](http://news.maxjia.com/bbs/app/profile/user/profile?&userid=1083123)

根据测试，用户ID(userid)大致分布范围在一百万到一千万之间的数值。

### 工作流程

- 设定用户ID读取起点
- 读取用户ID的json格式数据，主要获得userid（MAX+社区ID）和steam_id（STEAM账号ID）的对应关系

把脚本部署到服务器，因为多线程写的比较烂，大概用了4天时间读取完百万条用户数据。


## 后记

MAX+ 用户体量也有百万级了，但是安全和隐私方法还是比较薄弱的，对应接口一没有做鉴权，二没有做次数限制，可以说把社区数据拱手让给别人抓取和分析。

