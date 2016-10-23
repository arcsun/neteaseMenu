#!/bin/bash
ps -ef | grep gunicorn | awk '{print $2}' | xargs kill -9
ps -ef | grep bgtask.py | awk '{print $2}' | xargs kill -9

sleep 2

(setsid python bgtask.py &)
gunicorn -b 0.0.0.0:80 -k gevent start:app
