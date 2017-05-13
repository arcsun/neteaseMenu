#coding=utf-8
from flask import Flask, redirect, render_template, request, Response
from codepy import menulog
import anydbm as dbm
import shelve
import os, sys
import urllib
from datetime import datetime
import time
import urllib2
import hashlib


app = Flask(__name__)
visit = 0
visitHome = 0
startTime = time.time()

cache = {}
s = None


@app.route('/', methods=['POST', 'GET'])
def mockMain():
    return "hello mock"



@app.route('/api/v1/verify', methods=['POST', 'GET'])
def mockYidun():
    # 易盾滑块后端验证
    resp = Response('{"msg":"success","result":true,"c":1,"error":0}')
    resp.headers['Content-Type'] = 'application/json;charset=UTF-8'
    return resp



if __name__ == '__main__':
    if sys.platform.startswith('win'):
        # 本地调试
        # import webbrowser
        # webbrowser.open('http://127.0.0.1:8080/')
        app.run(host='127.0.0.1', port= 8080, debug= True, threaded= True)
    else:
        # 线上正式版本
        # app.run(host='0.0.0.0', port= 5050, threaded= True)
        from werkzeug.contrib.fixers import ProxyFix
        app.wsgi_app = ProxyFix(app.wsgi_app)
        app.run(host='0.0.0.0', port= 5050)
