#网易(杭州)菜单 v2.7
示例网址：
www.crystalpot.cn/menu

微信公众号：neteasemenu  

运行环境:  
  python 2.7  
  Flask==0.10.1  
  Jinja2==2.8  
  Werkzeug==0.10.4
  
bgtask.py:  
  自动定时抓取信息，需首先执行: (python bgtask.py &)
  抓取到的url等信息存储在文件datafile中
  
run.py:  
  web程序入口, python run.py 或使用gunicorn等启动  
  gunicorn -b 0.0.0.0:5000 -k gevent run-ol:app  
  日志记录在menu.log  
  
codepy:  
  web和日志部分的代码  
  读取bgtask.py生成的文件  
  
    
  
 
    

    
