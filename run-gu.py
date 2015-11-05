#coding=utf-8
from flask import Flask, redirect
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


if __name__ == '__main__':
    # 这两行用于gunicorn
    from werkzeug.contrib.fixers import ProxyFix
    app.wsgi_app = ProxyFix(app.wsgi_app)

    app.run(host='0.0.0.0', port= 5000)
