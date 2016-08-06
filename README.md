#网易(杭州)菜单 v2.5  
更新说明：  
适配菜单页里新的日期写法  
记录访问次数到本地文件  
连续爬到空白页时, 提前结束此轮查找  
切到sqlite分支, 准备替换存储方式  

示例网址：  
http://43.241.220.139:5000/menu  
http://43.241.220.139:5000/menu/0  

微信公众号：neteasemenu  

运行环境:  
  python 2.7  
  Flask==0.10.1  
  Jinja2==2.8  
  Werkzeug==0.10.4  
  
bgtask.py:  
  爬虫, 每小时抓取一次，需(首先)单独执行: (python bgtask.py &)
  抓取到的url等信息存储在文件datafile中  
  
run.py:  
  web程序入口, python run.py 或使用gunicorn等启动
  gunicorn -b 0.0.0.0:5000 -k gevent run-ol:app
  日志记录在menu.log  
  
codepy:  
  web和日志部分的代码  
  读取bgtask.py生成的文件  
    
  
 
    

    
