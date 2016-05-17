#coding=utf-8
from flask import Flask, redirect, render_template, request
from codepy import menulog
import anydbm as dbm
import webbrowser
import os
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Netease Menu!'


@app.route('/menu/<int:day>', methods = ['GET', 'POST'])
def menu(day=0):
    # 0今天, 1明天, 151202指定日期
    from codepy import menu
    if request.method == 'POST':
        day = int(request.form['day'])
    url = menu.Menu(day).process()
    if url.startswith('http'):
        return redirect(url)
    else:
        return url

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
    # 暂无权限
    return render_template('manage.html')


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
    webbrowser.open('http://127.0.0.1:8080/menu')
    app.run(port= 8080)
