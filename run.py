#coding=utf-8
from flask import Flask, redirect, render_template, request
from codepy import menulog
import anydbm as dbm
import webbrowser
import os

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
        return render_template('menu.html', vals= vals, days= future)
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


@app.route('/menu/log')
def readLog():
    f = None
    try:
        files = os.listdir('./')
        logs = []
        for fname in files:
            if fname.startswith('menu.log'):
                logs.append(fname)
        f = open(logs[-1])
        content = f.read().decode('utf-8')
        return content
    except IOError:
        return '读取日志出错'
    finally:
        if f:
            f.close()



if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1/menu')
    app.run(port= 80)
