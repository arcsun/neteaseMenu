#coding=utf-8
import logging
import logging.handlers

LOG_FILE = 'menu.log'
handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes = 1024*1024, backupCount = 5)  # 实例化handler
fmt = '[%(levelname)s]%(asctime)s: %(message)s'

formatter = logging.Formatter(fmt)   # 实例化formatter
handler.setFormatter(formatter)      # 为handler添加formatter

logger = logging.getLogger('menu')    # 获取名为tst的logger
logger.addHandler(handler)           # 为logger添加handler
logger.setLevel(logging.DEBUG)


def info(msg):
    print u'[info]%s'% msg
    logger.info(msg)

def debug(msg):
    print u'[debug]%s'% msg
    logger.debug(msg)