#!/bin/bash
ps -ef | grep "gunicorn -b 0.0.0.0:5050 -k gevent mock:app" | awk '{print $2}' | xargs kill -9

sleep 2

gunicorn -b 0.0.0.0:5050 -k gevent mock:app
