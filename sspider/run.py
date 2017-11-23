# -*- encoding: utf-8 -*-
__author__ = 'GalaIO'

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

from handler import *
import logging

# 配置logging
logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='crawling.log')

class Handler(BaseHandler):
    '''
    抓取http://oldman.39.net 网站定制
    '''
    count = 0
    def __init__(self):
        BaseHandler.__init__(self)
        self.url_pattern = ['^http://oldman.39.net/a.*$', '^/a.*$']

    def on_start(self):
        self.crawl('http://oldman.39.net/a/170606/5435032.html', callback=self.index_page)

    def index_page(self, response):
        for each in response.doc('a[href^="http"]').items():
            self.crawl(each.attr.href, callback=self.index_page)
        title = response.doc('.art_box h1:first').text()
        content = response.doc('.art_con p').text()
        # logging.info(title, content)
        if len(title) and len(content):
            logging.info('保存...%s' % title)
            with open("data/{}.txt".format(Handler.count), "w") as file:
                file.write("%s\r\n%s" % (title, content))
                file.flush()
                Handler.count += 1

    def detail_page(self, response):
        logging.info( {
            "url": response.url,
            "title": response.doc('title').text(),
        })

if __name__ == '__main__':
    instance = Handler()
    print 'strrt up..............'
    instance.run()