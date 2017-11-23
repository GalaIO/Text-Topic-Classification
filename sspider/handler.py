# -*- encoding: utf-8 -*-
import re

__author__ = 'GalaIO'

import Queue
import requests
from pyquery import PyQuery as pq


class BaseHandler:


    def __init__(self):
        self.url_pattern = []
        self.crawl_config = {
            'queue_size': 1000
        }
        self.queue = Queue.Queue(self.crawl_config['queue_size'])

    def crawl(self, url, callback):
        # 匹配url模式
        if self.check_url_pattern(url):
            self.queue.put((url, callback))

    def run(self):
        if not self.__dict__.has_key('on_start') or not self.__dict__['on_start'].__dict__.has_key('func_name'):
            print 'you should name a on_start func!'

        # 运行初始代码
        self.on_start()
        # 开始从队列取出 执行
        while(self.queue.qsize() > 0):
            url, callback = self.queue.get()
            print 'crawl %s, callback %s' % (url, callback.func_name)
            response = requests.get(url)
            content = response.content
            response.doc = pq(content.decode(response.apparent_encoding))
            callback(response)

        print 'over!!'

    def on_start(self):
        pass


    def check_url_pattern(self, url):
        if len(self.url_pattern) <= 0:
            return True
        for pattern in self.url_pattern:
            if re.match(pattern, url, re.I |re.S):
                return True
        return False

