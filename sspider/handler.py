# -*- encoding: utf-8 -*-
import re

__author__ = 'GalaIO'

import Queue
import requests
from pyquery import PyQuery as pq
import logging

class BaseHandler:


    def __init__(self):
        self.url_pattern = []
        self.crawl_config = {
            'queue_size': 1000
        }
        # 从文件读取已爬过的url
        try:
            with open('url_saved_file.txt', 'r') as url_saved_file:
                self.url_cached = [url.strip() for url in url_saved_file.readlines()]
        except Exception, e:
            logging.error(e.message)
        self.url_cached = []
        self.queue = Queue.Queue(self.crawl_config['queue_size'])

    def crawl(self, url, callback):
        # 匹配url模式
        if self.check_url_pattern(url):
            self.queue.put((url, callback))

    def run(self):
        if not self.__dict__.has_key('on_start') or not self.__dict__['on_start'].__dict__.has_key('func_name'):
            logging.error('you should name a on_start func!')

        # 运行初始代码
        self.on_start()
        # 开始从队列取出 执行
        while(self.queue.qsize() > 0):
            url, callback = self.queue.get()
            logging.info('crawl %s, callback %s' % (url, callback.func_name))
            try:
                response = requests.get(url)
                content = response.content
                response.doc = pq(content.decode(response.apparent_encoding))
            except Exception, e:
                logging.warning('%s has a err %s..coding is %s' % (url, e.message, response.encoding if isinstance(response, requests.Response) else 'None'))
                continue
            logging.info('crawl done, callbbacking...')
            callback(response)
            logging.info('callback done, pulling...')

        logging.info('over!!')
        # 保存爬取的url路径，为了随后去重
        url_saved_file = open('url_saved_file.txt', 'w')
        url_saved_file.write('\r\n'.join(self.url_cached))
        url_saved_file.flush()
        url_saved_file.close()

    def on_start(self):
        pass


    def check_url_pattern(self, url):
        # 首先去重
        if url in self.url_cached:
            return False
        self.url_cached.append(url)
        if len(self.url_pattern) <= 0:
            return True
        for pattern in self.url_pattern:
            if re.match(pattern, url, re.I |re.S):
                return True
        return False

