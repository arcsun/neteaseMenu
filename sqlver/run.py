#coding=utf-8
from flask import Flask, redirect, render_template, request
import webbrowser
import sqlite3
import anydbm as dbm
import urllib

app = Flask(__name__)

# 后期可能会从dbm更换为sqlite

@app.route('/')
def hello_world():
    conn = sqlite3.connect('test.db')
    curs = conn.cursor()
    curs.execute('select page from test where day=160718')
    text= curs.fetchall()[0]
    return text

@app.route('/menus/<int:day>', methods = ['GET', 'POST'])
def menus(day=0):
    from codepy import menu
    if request.method == 'POST':
        day = int(request.form['day'])
    url = menu.Menu(day).process()
    if url.startswith('http'):
        yxid = url.split('=')[1]
        print yxid

        conn = sqlite3.connect('menu.db')
        curs = conn.cursor()
        curs.execute('create table if not exists menu(day int, yxid int, page text) ')



        page = urllib.urlopen(url)
        text = page.read().decode('utf-8')
        return text
    else:
        return url


@app.route('/save')
def save():
    urlhead = 'http://numenplus.yixin.im/singleNewsWap.do?materialId='
    db = dbm.open('datafile', 'c')
    cache = eval(db['cache'])
    conn = sqlite3.connect('menu.db')
    curs = conn.cursor()
    curs.execute('create table if not exists menu(day int, page text) ')

    cache = {160718: 35371}

    for day in cache.keys():
        print day
        print urlhead+ str(cache.get(day))
        page = urllib.urlopen(urlhead+ str(cache.get(day)))
        text = page.read().decode('utf-8')
        checkQuery = 'select day from menu where day=(?)'
        curs.execute(checkQuery, [day])
        if not curs.fetchall():
            query = 'insert into menu values(?,?)'
        else:
            query = 'update menu set page=(?) where day=(?)'
        vals = [day, text]
        curs.execute(query, vals)
    conn.commit()
    curs.execute('select * from menu')
    for row in curs.fetchall():
        print row
    conn.close()
    db.close()


if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:8080/')
    app.run(port= 8080)