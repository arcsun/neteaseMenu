#网易(杭州)菜单 v1.2.1
示例网址：  
http://43.241.220.139:5000/menu/0  
http://43.241.220.139:5000/menu/1  
http://43.241.220.139:5000/menu/151104  

运行环境:  
  python 2.7  
  Flask==0.10.1  
  Jinja2==2.8  
  Werkzeug==0.10.4  
  
bgtask.py:  
  爬虫, 每小时抓取一次，需(首先)单独执行: python bgtask.py &  
  抓取到的url等信息存储在record.pkl中(使用cPickle)  
  
run.py:  
  web程序入口, python run.py 或使用gunicorn等启动  
  日志记录在menu.log  
  
codepy:  
  web和日志部分的代码  
  读取bgtask.py生成的文件  
    
  
 
    

    
