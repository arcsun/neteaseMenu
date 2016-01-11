#coding=utf-8
import time
import copy
import anydbm as dbm
import menulog

urlhead = 'http://numenplus.yixin.im/singleNewsWap.do?materialId='
frequency = 5400

class Menu:
    def __init__(self, day= 0):
        self.today = int(time.strftime('%y%m%d',time.localtime(time.time())))  # 151022
        self.returnMaybe = False
        self.gotoid = False
        if 0 <= day <= 99:
            self.today = self.getNextDay(self.today, day)
        elif 100<= day <= 9999:
            self.returnMaybe = True
        elif 10000<= day < 99999:
            self.gotoid = True
            self.today = day
        elif 151027<= day < 991231:
            self.today = day

        self.startId = 0
        self.result = u'未找到菜单'
        self.lastQuery = 0
        self.now = int(time.time())
        self.cache = {}         # {151019:15163}  # 日期:id
        self.maybe = []         # 爬到的报错的页面
        self.maybeUrl = ''
        self.tmp = 0


    def getNextDay(self, today, step= 1):
        def calcu():
            lastDays = {'0131': '0201', '0229': '0301', '0331': '0401', '0430': '0501', '0531': '0601', '0630': '0701',
                        '0731': '0801', '0831': '0901', '0930': '1001', '1031': '1101', '1130': '1201', '1231': '0101'}  # 16年是闰年，暂把2月设成0229
            now = str(self.tmp)
            year = now[0:2]      # 15
            monthday = now[2:]   # 1221
            if monthday in lastDays.keys():
                if monthday == '1231':
                    year = str(int(year) + 1)
                tomorrow = lastDays[monthday]
                self.tmp = int(year + tomorrow)
            else:
                self.tmp = int(now)+1

        self.tmp = today
        for i in range(step):
            calcu()
        return self.tmp


    def process(self):
        def getTime():
            return time.strftime('20%y-%m-%d %H:%M:%S', time.localtime())

        def getUrl(targetday = self.today):
            return urlhead + str(self.cache.get(targetday))

        def getMaybe():
            backup = copy.deepcopy(self.maybe)
            backup.sort()
            backup.reverse()
            self.result += u'\t 可能的url: '
            first = True
            for mid in backup:
                if mid >= max(self.cache.values()):
                    if first:
                        first = False
                        self.result += u'\t' + urlhead+ str(mid)
                        if self.returnMaybe:
                            self.maybeUrl = urlhead+ str(mid)
                    else:
                        self.result += '\t' + str(mid)
                else:
                    self.maybe.remove(mid)
            if not self.maybe:
                self.result += 'None'
            else:
                menulog.debug(self.result)

        if self.gotoid:
            return urlhead + str(self.today)
        try:
            db = dbm.open('datafile', 'r')
            self.startId = eval(db['startId'])
            self.lastQuery = eval(db['lastQuery'])
            self.cache = eval(db['cache'])
            self.maybe = eval(db['maybe'])
            db.close()
        except (IOError, KeyError):
            msg = u'未找到缓存数据'
            menulog.debug(msg)
            return msg

        if self.today in self.cache.keys():
            # 缓存里有就直接返回url
            menulog.info('find cache @%s'% getTime())
            return getUrl()
        else:
            # 缓存中查不到
            menulog.info('cache not found @%s'% getTime())
            if self.result == u'未找到菜单':
                getMaybe()

            if self.returnMaybe and self.maybeUrl:
                return self.maybeUrl
            else:
                self.result += u'\t下次刷新:约%d秒后'% (self.lastQuery + frequency - self.now)
                self.result += u'\t日期:%s'% self.today
                return self.result
