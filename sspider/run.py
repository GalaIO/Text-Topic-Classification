# -*- encoding: utf-8 -*-
__author__ = 'GalaIO'

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

from handler import *
import logging
import re
import datetime
import time

# 配置logging
logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='crawling.log')

class Handler39(BaseHandler):
    '''
    抓取http://oldman.39.net 网站定制
    '''
    count_prefix = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
    count = 0
    def __init__(self):
        BaseHandler.__init__(self)
        # self.url_pattern = ['^http://oldman.39.net/a.*$', '^/a.*$']
        self.url_pattern = [
            '^http://oldman.39.net/lrbj.*$',
            '^http://oldman.39.net/living.*$',
            '^http://oldman.39.net/nutrition.*$',
            '^http://oldman.39.net/lrxl.*$',
            '^http://oldman.39.net/sports.*$',
            '^http://oldman.39.net/ln.*$',
            '^http://oldman.39.net/lryp.*$',
            '^http://oldman.39.net/mrys.*$',
            '^http://oldman.39.net/special.*$',
            '^http://oldman.39.net/lrqw.*$',
            '^http://oldman.39.net/a.*$',
        ]

    def on_start(self):
        self.crawl('http://oldman.39.net/lrbj', callback=self.index_page)
        self.crawl('http://oldman.39.net/living', callback=self.index_page)
        self.crawl('http://oldman.39.net/nutrition', callback=self.index_page)
        self.crawl('http://oldman.39.net/lrxl', callback=self.index_page)
        self.crawl('http://oldman.39.net/ln', callback=self.index_page)
        self.crawl('http://oldman.39.net/sports', callback=self.index_page)
        self.crawl('http://oldman.39.net/lryp', callback=self.index_page)
        self.crawl('http://oldman.39.net/mrys', callback=self.index_page)
        self.crawl('http://oldman.39.net/special', callback=self.index_page)
        self.crawl('http://oldman.39.net/lrqw', callback=self.index_page)
        self.crawl('http://oldman.39.net/a/170606/5435032.html', callback=self.index_page)

    def index_page(self, response):
        for each in response.doc('a[href^="http"]').items():
            self.crawl(each.attr.href, callback=self.index_page)
        # 进一步匹配url 做额外处理
        # if re.match('^http://oldman.39.net/a.*$', response.url) or re.match('^/a.*$', response.url):
        title = response.doc('.art_box h1:first').text()
        content = response.doc('.art_con p').text()
        # logging.info(title, content)
        if len(title) and len(content):
            logging.info('保存...%s %s' % (response.url, title))
            with open("data/{}-{}.txt".format(Handler99.count_prefix, Handler99.count), "w") as file:
                file.write("%s\r\n%s" % (title, content))
                file.flush()
                Handler99.count += 1
        else:
            logging.info('nothing...%s' % (response.url))
        # 休眠5秒
        time.sleep(5)

    def detail_page(self, response):
        logging.info( {
            "url": response.url,
            "title": response.doc('title').text(),
        })

class Handler99(BaseHandler):
    '''
    抓取http://oldman.9939.com/ 网站定制
    '''
    count_prefix = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
    count = 0
    def __init__(self):
        BaseHandler.__init__(self)
        # self.url_pattern = ['^http://oldman.39.net/a.*$', '^/a.*$']
        self.url_pattern = [
            '^http://oldman.9939.com/bj.*$',
            '^http://oldman.9939.com/yinshi.*$',
            '^http://oldman.9939.com/yangsheng.*$',
            '^http://oldman.9939.com/lrxl.*$',
            '^hhttp://oldman.9939.com/lrjs.*$',
            '^http://oldman.9939.com/jb.*$',
            '^http://oldman.9939.com/yy.*$',
        ]

    def on_start(self):
        self.crawl('http://oldman.9939.com/yangsheng/4.shtml', callback=self.index_page)
        self.crawl('http://oldman.9939.com/bj', callback=self.index_page)
        self.crawl('http://oldman.9939.com/yinshi', callback=self.index_page)
        self.crawl('http://oldman.9939.com/yangsheng', callback=self.index_page)
        self.crawl('http://oldman.9939.com/lrxl', callback=self.index_page)
        self.crawl('http://oldman.9939.com/lrjs', callback=self.index_page)
        self.crawl('http://oldman.9939.com/jb', callback=self.index_page)
        self.crawl('http://oldman.9939.com/yy', callback=self.index_page)

    def index_page(self, response):
        logging.info('parse url...')
        for each in response.doc('a[href^="http"]').items():
            self.crawl(each.attr.href, callback=self.index_page)
        # 进一步匹配url 做额外处理
        # if re.match('^http://oldman.39.net/a.*$', response.url) or re.match('^/a.*$', response.url):
        logging.info('handle doc...')
        title = response.doc('.xqTit').text()
        content = response.doc('.inCont p').text()
        # logging.info(title, content)
        if len(title) > 0  and len(content) > 0:
            logging.info('保存...%s %s' % (response.url, title))
            with open("data/{}-{}.txt".format(Handler99.count_prefix, Handler99.count), "w") as file:
                file.write("%s\r\n%s" % (title, content))
                file.flush()
                Handler99.count += 1
        else:
            logging.info('nothing...%s' % (response.url))
        # 休眠5秒
        time.sleep(5)

    def detail_page(self, response):
        logging.info( {
            "url": response.url,
            "title": response.doc('title').text(),
        })

if __name__ == '__main__':
    # instance = Handler39()
    # print 'strrt up..............'
    # instance.run()
    instance = Handler99()
    print 'strrt up..............'
    instance.run()