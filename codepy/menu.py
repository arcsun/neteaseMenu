#coding=utf-8
import time
import copy
import anydbm as dbm
import menulog

urlhead = 'http://numenplus.yixin.im/singleNewsWap.do?materialId='
frequency = 3600


class Menu:
    def __init__(self, day= 0):
        self.today = int(time.strftime('%y%m%d',time.localtime(time.time())))  # 151022
        self.returnMaybe = False
        if 100> day >0:
            self.today += 1
        elif day == 0:
            pass
        elif day > 151026:
            self.today = day
        elif day == 100:
            self.returnMaybe = True

        print self.today

        self.startId = 0
        self.result = u'未找到菜单'
        self.lastQuery = 0
        self.now = int(time.time())
        self.cache = {}         # {151019:15163}  # 日期:id
        self.maybe = []         # 爬到的报错的页面
        self.maybeUrl = ''


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
                return self.result