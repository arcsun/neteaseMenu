# coding=utf-8
import time
import urllib
import re

"""
用来测试新的正则
"""

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