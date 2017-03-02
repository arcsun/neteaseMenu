# coding=utf-8
import urllib
import re
import urllib2

"""
用来测试新的正则
"""


def test():
    pattern_title = r"<title>(.+)</title>"
    pattern_weekday = ur"（星期(.)）"
    pattern_year = ur'20(\d\d)-'
    pattern_month_update = r'-(\d+)-'
    pattern_month = r'>(\d+)</span>'
    pattern_day = ur'月(\d+)日'
    pattern_day2 = ur'>(\d+)日'
    urlhead = 'http://numenplus.yixin.im/singleNewsWap.do?materialId='
    datafile = 'datafile'


    page = urllib.urlopen(urlhead+ str(36673))
    text = page.read().decode('utf-8')
    if text.find(u'今日菜单') != -1:
        print 'find'

        year = re.findall(pattern_year, text)[0]

        print 'year: %s'% year

        monthday = re.findall(pattern_month, text)

        print 'monthday: %s'% monthday


        if monthday[0] == '0' and len(monthday)> 2:
            month = monthday[0]+monthday[1]
            dayIndex = 2
        else:
            month = monthday[0]
            dayIndex = 1

        print 'month: %s'% month

        if len(monthday) > dayIndex:
            day = monthday[dayIndex]
            if len(day) == 1:
                # 针对 1</span>...>5日&nbsp
                day += re.findall(pattern_day2, text)[0]
        else:
            day = re.findall(pattern_day, text)[0]

        print 'day: %s'% day

        update_month = re.findall(pattern_month_update, text)[0]  # 发布菜单的月份，用于跨年
        if int(update_month) == 12 and int(month) == 1:
            year = str(int(year)+1)
        thisday = int(year+month+day)

        print 'thisday: %s'% thisday

        print 'update_month: %s'% update_month

    else:
        print 'not find'


def test2(mid):
    req = urllib2.Request('http://numenplus.yixin.im/singleNewsWap.do?materialId=%s&companyId=1'% mid)
    req.add_header('User-Agent', 'Mozilla/5.0 (Linux; Android 6.0; PRO 6 Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/44.0.2403.130 Mobile Safari/537.36 YiXin/4.8.3')
    try:
        res = urllib2.urlopen(req, timeout= 5)
        html = res.read().decode('utf-8')
        return html, html.find(u'今日菜单') != -1, html.find(u'请求素材不存在') != -1
    except Exception as e:
        print mid, e
        return 'timeout', False, True


def testBus(mid):
    url = "http://numenplus.yixin.im/multiNewsWap.do?multiNewsId=%s"%mid
    req = urllib2.Request(url+ '&companyId=1')
    req.add_header('User-Agent', 'Mozilla/5.0 (Linux; Android 6.0; PRO 6 Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/44.0.2403.130 Mobile Safari/537.36 YiXin/4.8.3')
    res = urllib2.urlopen(req)
    html = res.read().decode('utf-8')
    return html



for i in range(51770, 52100):
    result = test2(i)
    if result[1] is True:
        key = 'menu'
    elif result[2] is False:
        key = 'exist'
    else:
        key = 'p'
    print i, result[1], result[2], key

#
# for i in range(10490, 11000):
#     r = testBus(i)
#     if r.find(u'杭州网易班车线路') != -1:
#         print i, True, '+++++++++++'
#     elif r.find(u'请求多图文素材不存在') != -1:
#         break
#     else:
#         print i


