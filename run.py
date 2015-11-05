#coding=utf-8
from flask import Flask, redirect
import webbrowser
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Netease Menu!'


@app.route('/menu/<int:day>')
def menu(day=0):
    # 今天0, 明天1...
    from codepy import menu
    url = menu.Menu(day).process()
    if url.startswith('http'):
        return redirect(url)
    else:
        return url


if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1/menu/0')
    app.run(port= 80)
