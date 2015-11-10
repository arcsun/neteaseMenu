#coding=utf-8
from flask import Flask, redirect
import cPickle as pickle
from codepy import menulog

app = Flask(__name__)

# 线上版本的启动入口

@app.route('/')
def hello_world():
    return 'Netease Menu!'


@app.route('/menu/<int:day>')
def menu(day=0):
    from codepy import menu
    url = menu.Menu(day).process()
    if url.startswith('http'):
        return redirect(url)
    else:
        return url


@app.route('/start/<int:startid>')
def start(startid= 15900):
    # 重置起始查找点为指定值
    try:
        f = file('record.pkl', 'rb')
        startId = pickle.load(f)
        startId = startid
        lastQuery = pickle.load(f)
        cache = pickle.load(f)
        maybe = pickle.load(f)
        f.close()

        f = file('record.pkl', 'wb')
        pickle.dump(startId, f, 0)
        pickle.dump(lastQuery, f, 0)
        pickle.dump(cache, f, 0)
        pickle.dump(maybe, f, 0)
        f.close()
        msg = u'设置查找起点ID为:%d'% startid
        menulog.info(msg)
        return msg
    except (IOError, EOFError):
        msg = u'缓存读取错误'
        menulog.info(msg)
        return msg


if __name__ == '__main__':
    # 这两行用于gunicorn
    from werkzeug.contrib.fixers import ProxyFix
    app.wsgi_app = ProxyFix(app.wsgi_app)

    app.run(host='0.0.0.0', port= 5000)
