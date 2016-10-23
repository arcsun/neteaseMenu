# #coding=utf-8
import time
import urllib
import re
import anydbm as dbm
from codepy import menulog

'''
(python bgtask.py &)
用于抓取菜单信息
'''

pattern_title = r"<title>(.+)</title>"
pattern_weekday = ur"（星期(.)）"
pattern_year = ur'20(\d\d)-'
pattern_month_update = r'-(\d+)-'
pattern_month = r'>(\d+)</span>'
pattern_day = ur'月(\d+)日'
pattern_day2 = ur'>(\d+)日'
urlhead = 'http://numenplus.yixin.im/singleNewsWap.do?materialId='
datafile = 'datafile'
startId = 37000

class Background:
    def __init__(self):
        self.frequency = 10800        # 间隔(秒)
        self.interval = 150           # 每次爬的id数量
        self.back = 30                # 每次从self.startId - self.back开始查找，防止被占坑
        self.firstRun = True          # 是否在程序开始后先执行一次

        self.today = 0
        self.running = False          # 是否正在运行(否则同一秒会重复执行多次)
        self.startId = 0
        self.count = 0
        self.usedId  = 0              # 记录中间最大的非空id
        self.nowId = self.startId
        self.result = u'未找到菜单'
        self.lastQuery = 0
        self.cache = {}               # {151019:15163}  # 日期:id
        self.maybe = []               # 爬到的报错的页面
        self.empty = 0

    def getTime(self):
        return int(time.time())

    def schedule(self):
        if self.firstRun:
            self.firstRun = False
            self.process()
            self.schedule()        # 可用Timer().start()替换
        else:
            while True:
                time.sleep(0.1)    # 可以极大减少cpu占用
                if self.getTime() % self.frequency == 0 and not self.running:
                    self.running = True
                    self.process()
                elif self.getTime() % 3600 == 0:   # 每3600s记录一次存活信息
                    menulog.info('%s@%d'% (time.strftime('20%y-%m-%d %H:%M:%S', time.localtime()), self.getTime()))
                    time.sleep(1)

    def process(self):
        self.count += 1
        self.today = int(time.strftime('%y%m%d', time.localtime()))
        menulog.info(u'开始第%d次查找@%d'% (self.count, self.getTime()))

        try:
            db = dbm.open(datafile, 'c')
            if not len(db):
                # 没有之前的数据文件
                db['startId'] = str(startId)
                db['lastQuery'] = str(self.getTime())
                db['cache'] = str(self.cache)
                db['maybe'] = str(self.maybe)

            self.startId = eval(db['startId']) - self.back
            self.cache = eval(db['cache'])
            self.maybe = eval(db['maybe'])
            self.nowId = self.startId
            self.lastQuery = self.getTime()        # 保存最后搜索时间

            while self.nowId - self.startId < self.interval:
                menulog.info(u'开始查找: %d'% self.nowId)
                page = urllib.urlopen(urlhead+ str(self.nowId))
                text = page.read().decode('utf-8')
                if text.find(u'今日菜单') != -1:
                    self.empty = 0
                    try:
                        year = re.findall(pattern_year, text)[0]
                        monthday = re.findall(pattern_month, text)

                        if monthday[0] == '0' and len(monthday)> 2:
                            month = monthday[0]+monthday[1]
                            dayIndex = 2
                        else:
                            month = monthday[0]
                            dayIndex = 1

                        if len(monthday) > dayIndex:
                            day = monthday[dayIndex]
                            if len(day) == 1:
                                # 针对 1</span>...>5日&nbsp
                                # 上面的月份也有这种情况
                                day += re.findall(pattern_day2, text)[0]
                        else:
                            day = re.findall(pattern_day, text)[0]

                        update_month = re.findall(pattern_month_update, text)[0]  # 发布菜单的月份，用于跨年
                        if int(update_month) == 12 and int(month) == 1:
                            year = str(int(year)+1)
                        thisday = int(year+month+day)

                        self.startId = self.nowId
                        if self.cache.has_key(thisday):
                            menulog.info(u'更新%s的菜单id为%s'% (thisday, self.nowId))
                        self.cache[thisday] = self.nowId
                        menulog.info('find %d'% self.nowId)
                    except (IndexError, ):
                        if text.find(u'祝您用餐愉快') and text.find(u'农历'):
                            menulog.debug('gz menu')
                        elif self.nowId not in self.maybe:
                            self.maybe.append(self.nowId)
                            menulog.debug('IndexError add maybe')

                else:
                    if text.find(u'请求素材不存在') == -1:
                        # 搜索到的结果页有内容(不是菜单)
                        self.usedId = self.nowId
                        self.empty = 0
                    else:
                        self.empty += 1
                        if self.empty > 10:
                            menulog.debug('break this round')
                            break
                self.nowId += 1

            # if self.maybe and max(self.maybe) > max(self.cache.values()):
            #   # 取消这个设计, 格式变化太大, 很可能导致卡住
                # menulog.info(u'更新起点至可能的ID:%d'% max(self.maybe))
                # self.startId = max(self.maybe)
            if self.usedId > self.startId:
                menulog.info(u'更新起点至%d'% self.usedId)
                self.startId = self.usedId

            # 保存
            db['startId'] = str(self.startId)
            db['lastQuery'] = str(self.lastQuery)
            db['cache'] = str(self.cache)
            db['maybe'] = str(self.maybe)
            menulog.info(u'第%d次查找结束'% self.count)

            # 已更新的菜单
            self.cache = eval(db['cache'])
            future = []
            for day in self.cache.keys():
                if day >= self.today:
                    future.append(day)
            future.sort()
            db['future'] = str(future)
            menulog.info(u'更新今后已找到的菜单列表')
            db.close()
        except (IOError, EOFError):
            menulog.info(u'缓存读取/创建异常')
        finally:
            self.running = False

Background().schedule()


