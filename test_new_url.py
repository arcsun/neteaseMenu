# coding=utf-8
import urllib
import re
import urllib2
import cookielib
from urllib2 import HTTPError


"""
用来测试新的URL

GET /wap/material/viewImageText?id=31415424 HTTP/1.1
Host: wap.plus.yixin.im
Connection: keep-alive
Cache-Control: max-age=0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
x-wap-profile: http://218.249.47.94/UAProfile/CMCC/MT6797_UAprofile.xml
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Linux; Android 6.0; MZ-PRO 6 Build/MRA58K) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/45.0.2454.94 Mobile Safari/537.36
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,en-US;q=0.8
Cookie: NTESplusSI=6B8336B65EE6B94C690E1E6A42C6691A.yx10.popo.infra.mail-8011; __utma=75741715.572861464.1482587990.1482587990.1482587990.1; __utmb=75741715.2.10.1482587990; __utmc=75741715; __utmz=75741715.1482587990.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)
"""

ua_yixin = 'Mozilla/5.0 (Linux; Android 6.0; PRO 6 Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/44.0.2403.130 Mobile Safari/537.36'
accept = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'

def test(tid, save= False):
    try:
        url = 'http://wap.plus.yixin.im/wap/material/viewImageText?id=%s'% tid
        req = urllib2.Request(url)
        req.add_header('User-Agent', ua_yixin)       # 易信外会有个广告
        req.add_header('Accept', accept)             # 易信会检测这个

        res = urllib2.urlopen(req)
        text = res.read()
        t = text.decode('utf-8')        # 这里print会报错
        if save:
            f = open('page.html', 'w+')
            f.write(text)
            f.close()

        if t.find(u'今日菜单') != -1:
            return '%s find++++++++++++++++++'% tid, True
        else:
            return '%s not find'%tid, False

    except Exception as e:
        return '%s error--------------'% tid, False


# 这个id似乎是固定的, 周五是31613351
pageList = {
    1: 31415423,
    5: 31613351,

    6: 31415424,  # 待定
}

# test(pageList.get(5))

result = []
for i in range(31431985, pageList.get(5)):
    r = test(i)
    if r[1]:
        result.append(i)
    print r[0]

print result