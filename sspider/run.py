# -*- encoding: utf-8 -*-
__author__ = 'GalaIO'

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

from handler import *
import re

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
        print title, content
        if len(title) and len(content):
            with open("data/{}.txt".format(Handler.count), "w") as file:
                file.write("%s\r\n%s" % (title, content))
                file.flush()

    def detail_page(self, response):
        print {
            "url": response.url,
            "title": response.doc('title').text(),
        }

if __name__ == '__main__':
    instan = Handler()
    instan.run()