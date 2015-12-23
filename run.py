#coding=utf-8
from flask import Flask, redirect, render_template, request
from codepy import menulog
import anydbm as dbm
import webbrowser

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


@app.route('/menu/info')
def info():
    db = dbm.open('datafile', 'r')
    msg = str(db)
    db.close()
    return msg


@app.route('/menu/clear')
def clearMaybe():
    # 清空可能的菜单(maybe=[])
    try:
        db = dbm.open('datafile', 'c')
        db['maybe'] = '[]'
        db.close()
        msg = u'清空maybe'
        menulog.info(msg)
        return msg
    except (IOError, KeyError):
        msg = u'缓存读取错误'
        menulog.info(msg)
        return msg


@app.route('/menu/start/<int:startid>')
def start(startid= 17000):
    # 设置起始查找点为指定值
    try:
        db = dbm.open('datafile', 'c')
        db['startId'] = str(startid)
        db.close()
        msg = u'设置查找起点ID为:%d'% startid
        menulog.info(msg)
        return msg
    except (IOError, KeyError):
        msg = u'缓存读取错误'
        menulog.info(msg)
        return msg


@app.route('/menu/add/<int:day>/<int:mid>')
def add(day= 151203, mid= 17063):
    # 手动添加一个菜单（偶尔发布者会填错日期）
    db = dbm.open('datafile', 'c')
    cache = eval(db['cache'])
    cache[day] = mid
    db['cache'] = str(cache)
    msg = u'更新%s的菜单id为%s'% (day, mid)
    menulog.info(msg)
    db.close()
    return msg



if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1/menu')
    app.run(port= 80)
