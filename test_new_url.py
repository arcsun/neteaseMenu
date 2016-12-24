# coding=utf-8
import urllib
import re
import urllib2
import cookielib

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

UA_yixin = 'Mozilla/5.0 (Linux; Android 6.0; PRO 6 Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/44.0.2403.130 Mobile Safari/537.36 YiXin/4.8.3'
UA_uc = 'Mozilla/5.0 (Linux; Android 6.0; MZ-PRO 6 Build/MRA58K) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/45.0.2454.94 Mobile Safari/537.36'
cookie_uc = 'NTESplusSI=6B8336B65EE6B94C690E1E6A42C6691A.yx10.popo.infra.mail-8011; __utma=75741715.572861464.1482587990.1482587990.1482587990.1; __utmb=75741715.2.10.1482587990; __utmc=75741715; __utmz=75741715.1482587990.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)'


def test():
    try:
        urlhead = 'http://wap.plus.yixin.im/wap/material/viewImageText?id='
        startId = 31613351
        nowId = startId

        req = urllib2.Request(urlhead+ str(nowId))
        req.add_header('User-Agent', UA_uc)

        # req.add_header('Accept-Encoding', 'gzip, deflate')
        # req.add_header('Accept-Language', 'zh-CN,en-US;q=0.8')
        # req.add_header('Upgrade-Insecure-Requests', '1')
        # req.add_header('x-wap-profile', 'http://218.249.47.94/UAProfile/CMCC/MT6797_UAprofile.xml')
        # req.add_header('Cookie', cookie_uc)

        res = urllib2.urlopen(req)
        text = res.read().decode('utf-8')

        print text
        if text.find(u'今日菜单') != -1:
            print 'find'
        else:
            print 'not find'

    except Exception as e:
        print e


test()

# page = urllib.urlopen('http://wap.plus.yixin.im/wap/material/viewImageText?id=31613351')
# text = page.read().decode('utf-8')
# print text
