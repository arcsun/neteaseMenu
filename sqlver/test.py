#coding=utf-8
import sqlite3
import urllib


urlhead = 'http://numenplus.yixin.im/singleNewsWap.do?materialId='
page = urllib.urlopen(urlhead+ str(35371))
text = page.read().decode('utf-8')

conn = sqlite3.connect('menu.db')  # 创建一个文件
curs = conn.cursor()
curs.execute('create table if not exists menu(day int, page text) ')
query = 'insert into menu values(?,?)'   #可使用占位符
query2 = 'update menu set page=(?) where day=(?)'   #可使用占位符
vals2 = ['123', 160718]
vals = [160718, text]
curs.execute(query2,vals2)
conn.commit()       # 提交后修改生效
curs.execute('select * from test')
for row in curs.fetchall():
    print row
conn.close()


