#coding=utf-8
from flask import Flask, redirect, render_template, request
from codepy import menulog
import anydbm as dbm
import os, sys
import urllib
from datetime import datetime
import time

app = Flask(__name__)
visit = 0
visitHome = 0
startTime = time.time()


@app.route('/')
def hello_world():
    return redirect('/menu')


@app.route('/menu/<int:day>', methods = ['GET', 'POST'])
def menu(day=0):
    # 0今天, 1明天, 151202指定日期
    from codepy import menu
    if request.method == 'POST':
        day = int(request.form['day'])
    globals()['visit'] += 1
    menulog.info(u'访问菜单@%s'% visit)
    url = menu.Menu(day).process()
    if url.startswith('http'):
        return redirect(url)
    else:
        return url


@app.route('/menus/<int:day>', methods = ['GET', 'POST'])
def menus(day=0):
    # 为解决微信内跳转卡住的问题, 增加这个方法
    # 服务器从易信读取网页信息后再返回给用户
    from codepy import menu
    if request.method == 'POST':
        day = int(request.form['day'])
    globals()['visit'] += 1
    menulog.info(u'访问菜单@%s'% visit)
    url = menu.Menu(day).process()
    if url.startswith('http'):
        page = urllib.urlopen(url)
        text = page.read().decode('utf-8')
        return text
    else:
        return url


@app.route('/menus/bus')
def bus():
    # 班车路线页, 中转一下
    globals()['visit'] += 1
    menulog.info(u'访问菜单@%s'% visit)
    url = "http://numenplus.yixin.im/multiNewsWap.do?multiNewsId=7386"
    try:
        page = urllib.urlopen(url)
        text = page.read().decode('utf-8')
        return text
    except:
        return u'网页访问出错'


def getWeekDayFromDay(daytime):
    """根据日期(如20160517)计算是星期几"""
    try:
        daytime = '20'+ str(daytime)    # '20160517'
        year = int(daytime[:4])         # 2016
        month = int(daytime[4:6])       # 5
        day = int(daytime[6:8])         # 17
        weekday = datetime(year, month, day, 0, 0, 0, 0).weekday()
        weekdaynames= {
            0: u'星期一',
            1: u'星期二',
            2: u'星期三',
            3: u'星期四',
            4: u'星期五',
            5: u'星期六',
            6: u'星期日',
        }
        return weekdaynames.get(weekday, u'')
    except:
        menulog.debug(u'获取星期几错误')
        return u''

@app.route('/menu')
def menuList():
    globals()['visitHome'] += 1
    menulog.info(u'访问主页@%s'% visitHome)
    try:
        db = dbm.open('datafile', 'c')
        cache = eval(db['cache'])
        future = eval(db['future'])
        vals = {}
        for day in future:
            vals[day] = cache[day]
        db.close()
        weekdays = {}
        for day in vals.keys():
            weekdays[day] = getWeekDayFromDay(day)
        return render_template('menu.html', vals= vals, days= future, weekdays= weekdays)
    except (IOError, KeyError):
        msg = u'缓存读取错误'
        menulog.info(msg)
        return msg


@app.route('/menu/manage/hzmenu')
def manage():
    seconds = int(time.time()- startTime)
    days = seconds/(24*60*60)
    if days >= 1:
        seconds -= 24*60*60*days
    hours = seconds/(60*60)
    if hours >= 1:
        seconds -= 60*60*hours
    miniutes = seconds/60
    if miniutes >= 1:
        seconds -= 60*miniutes
    timestr = u'本次已运行：%s天%s小时%s分钟%s秒'% (days, hours, miniutes, seconds)
    return render_template('manage.html', visit= visit, visitHome= visitHome, timestr= timestr)


@app.route('/menu/info')
def info():
    try:
        db = dbm.open('datafile', 'r')
        msg = str(db)
        db.close()
        return msg
    except (IOError, KeyError):
        return u'缓存读取错误'


@app.route('/menu/delete/<int:day>', methods = ['GET', 'POST'])
def delete(day= 150101):
    try:
        db = dbm.open('datafile', 'w')
        if request.method == 'POST':
            day = int(request.form['day'])
        cache = eval(db['cache'])
        if cache.has_key(day):
            del cache[day]
            msg = u'删除%s'% day
        else:
            msg = u'del key not found'
        menulog.info(msg)
        db['cache'] = str(cache)
        db.close()
        return msg
    except (IOError, KeyError):
        return u'缓存读取错误'


@app.route('/menu/delfuture/<int:day>', methods = ['GET', 'POST'])
def delfuture(day= 161300):
    try:
        db = dbm.open('datafile', 'w')
        if request.method == 'POST':
            day = int(request.form['day'])
        future = eval(db['future'])
        if day in future:
            future.remove(day)
            msg = u'删除%s'% day
        else:
            msg = u'del key not found'
        menulog.info(msg)
        db['future'] = str(future)
        db.close()
        delete(day)
        return msg
    except (IOError, KeyError) as e:
        print e
        return u'缓存读取错误'


@app.route('/menu/refreshlist')
def refreshlist():
    try:
        db = dbm.open('datafile', 'w')
        cache = eval(db['cache'])
        future = []
        today = int(time.strftime('%y%m%d',time.localtime(time.time())))
        for day in cache.keys():
            if day >= today:
                future.append(day)
        future.sort()
        db['future'] = str(future)
        msg = u'更新%s后已找到的菜单列表 from homepage'% today
        menulog.info(msg)
        db.close()
        return msg
    except (IOError, KeyError):
        return u'缓存读取错误'


@app.route('/menu/clear')
def clearMaybe():
    # 清空可能的菜单(maybe=[])
    try:
        db = dbm.open('datafile', 'w')
        db['maybe'] = '[]'
        db.close()
        msg = u'清空maybe'
        menulog.info(msg)
        return msg
    except (IOError, KeyError):
        msg = u'缓存读取错误'
        menulog.info(msg)
        return msg


@app.route('/menu/start/<int:startid>', methods = ['GET', 'POST'])
def start(startid= 17000):
    # 设置起始查找点为指定值
    try:
        if request.method == 'POST':
            startid = int(request.form['startid'])
        db = dbm.open('datafile', 'w')
        db['startId'] = str(startid)
        db.close()
        msg = u'设置查找起点ID为:%d'% startid
        menulog.info(msg)
        return msg
    except (IOError, KeyError):
        msg = u'缓存/POST参数读取错误'
        menulog.info(msg)
        return msg


@app.route('/menu/add/<int:day>/<int:mid>', methods = ['GET', 'POST'])
def add(day= 151203, mid= 17063):
    # 手动添加一个菜单（偶尔发布者会填错日期）
    try:
        db = dbm.open('datafile', 'w')
        cache = eval(db['cache'])
        if request.method == 'POST':
            day = int(request.form['day'])
            mid = int(request.form['mid'])
        cache[day] = mid
        db['cache'] = str(cache)
        msg = u'更新%s的菜单id为%s'% (day, mid)
        menulog.info(msg)
        db.close()
        return msg
    except (IOError, KeyError):
        msg = u'缓存/POST参数读取错误'
        menulog.info(msg)
        return msg


@app.route('/menu/log/<int:lines>')
def readLog(lines= 0):
    # 读取多少行log, 0为全部
    f = None
    try:
        files = os.listdir('./')
        logs = []
        for fname in files:
            if fname.startswith('menu.log'):
                logs.append(fname)
        if logs:
            f = open(logs[-1])
            contents = f.readlines()
            content = ''
            if lines == 0:
                lines = len(contents)
            line = 0
            for msg in reversed(contents):
                line += 1
                if line < lines:
                    content += msg+ '<br>'
                else:
                    break
            return content.decode('utf-8')
        else:
            return u'暂无日志'
    except IOError:
        return '读取日志出错'
    finally:
        if f:
            f.close()


if __name__ == '__main__':
    if sys.platform.startswith('win'):
        # 本地调试
        # import webbrowser
        # webbrowser.open('http://127.0.0.1:80/menu')
        app.run(host='127.0.0.1', port= 80, debug= True)
    elif len(sys.argv)> 1:
        # 线上调试, 随便传个参数
        app.run(host='0.0.0.1', port= 80, debug= True)
    else:
        # 线上正式版本, 用gunicorn启动
        from werkzeug.contrib.fixers import ProxyFix
        app.wsgi_app = ProxyFix(app.wsgi_app)
        app.run(host='0.0.0.0', port= 80)
