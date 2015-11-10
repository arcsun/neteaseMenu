#coding=utf-8
import time
import urllib
import re
import cPickle as pickle
from codepy import menulog

pattern_title = r"<title>(.+)</title>"
pattern_weekday = ur"（星期(.)）"
pattern_year = ur'20(\d\d)-'
pattern_monthday = r'>(\d+)</span>'
urlhead = 'http://numenplus.yixin.im/singleNewsWap.do?materialId='

class Background:
    def __init__(self):
        self.frequency = 3600         # 间隔(秒)
        self.interval = 150           # 每次爬的id数量
        self.firstRun = True          # 是否在程序开始后先执行一次
        self.running = False          # 是否正在运行(否则同一秒会重复执行多次)
        self.count = 0

        self.today = int(time.strftime('%y%m%d',time.localtime()))
        self.startId = 15500
        self.usedId  = 0   # 记录中间最大的非空id
        self.nowId = self.startId
        self.result = u'未找到菜单'
        self.lastQuery = self.getTime()
        self.cache = {}         # {151019:15163}  # 日期:id
        self.maybe = []         # 爬到的报错的页面


    def getTime(self):
        return int(time.time())


    def schedule(self):
        if self.firstRun:
            self.firstRun = False
            self.process()
            self.schedule()
        else:
            while True:
                time.sleep(0.1)
                if self.getTime() % self.frequency == 0 and not self.running:
                    self.running = True
                    # time.sleep(1)   # 加上标志位仍会触发多次, sleep可保证只触发一次
                    self.process()
                elif self.getTime() % 60 == 0:
                    menulog.info('%s@%d'% (time.strftime('20%y-%m-%d %H:%M:%S', time.localtime()), self.getTime()))
                    time.sleep(1)

    def process(self):
        def save():
            try:
                fs = open('record.pkl', 'wb')
                pickle.dump(self.startId, fs, 0)
                pickle.dump(self.lastQuery, fs, 0)
                pickle.dump(self.cache, fs, 0)
                pickle.dump(self.maybe, fs, 0)
                fs.close()
            except IOError:
                menulog.debug(u'保存缓存失败')

        self.count += 1
        menulog.info(u'开始第%d次查找@%d'% (self.count, self.getTime()))

        try:
            f = file('record.pkl', 'rb')
            self.startId = pickle.load(f)
            self.nowId = self.startId
            self.lastQuery = pickle.load(f)    # 注意这里会覆盖为原来的值
            self.cache = pickle.load(f)
            self.maybe = pickle.load(f)
            f.close()
        except (IOError, EOFError):
            # 没有缓存文件 或 文件内容格式不对
            menulog.info(u'缓存读取异常, 重建')
            save()

        self.lastQuery = self.getTime()   # 重新覆盖为现在的时间
        while self.nowId - self.startId < self.interval:
            menulog.info(u'开始查找: %d'% self.nowId)
            page = urllib.urlopen(urlhead+ str(self.nowId))
            text = page.read().decode('utf-8')
            if text.find(u'今日菜单') != -1:
                try:
                    year = re.findall(pattern_year, text)[0]
                    month = re.findall(pattern_monthday, text)[0]
                    day = re.findall(pattern_monthday, text)[1]
                    thisday = int(year+month+day)
                    self.startId = self.nowId
                    self.cache[thisday] = self.nowId
                    menulog.info('find %d'% self.nowId)
                except (IndexError, ):
                    if text.find(u'风味小吃') != -1:
                        # 抓到了广州的菜单
                        pass
                    else:
                        if self.nowId not in self.maybe:
                            self.maybe.append(self.nowId)
                        menulog.debug('IndexError')
            else:
                if text.find(u'请求素材不存在') == -1:
                    # 搜索到的结果页有内容(不是菜单)
                    self.usedId = self.nowId
            self.nowId += 1

        if self.maybe and max(self.maybe) > max(self.cache.values()):
            # 例如先更新了15956但是样式错误, 然后用过的id更新至16xxx, 最后又把15958替换成了正确的菜单
            menulog.info(u'更新起点至可能的ID:%d'% max(self.maybe))
            self.startId = max(self.maybe)

        elif self.usedId > self.startId:
            menulog.info(u'更新起点至%d'% self.usedId)
            self.startId = self.usedId

        menulog.info(u'第%d次查找结束'% self.count)
        save()
        self.running = False


Background().schedule()

