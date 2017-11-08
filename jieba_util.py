# -*- encoding: utf-8 -*-
__author__ = 'GalaIO'

import jieba
import os

# 载入停用词，放入列表
try:
    sw_file = open('resource/stop_words.txt')
    stop_words = [word.strip().decode('utf-8') for word in sw_file.readlines()]
    # print stop_words
finally:
    sw_file.close()

def docdir_handler(dir_path, f):
    '''
    对某一目录下的所有文档，进行遍历分词和对每篇执行f回调函数
    :param dir_path:
    :param f: f(index, word)，表示第几篇的什么单词，利用全局变量或闭包，引用等完成值传递或者操作
    :return: void

    这是f的一个例子，把每个文档的词连为一个字符串，同时存在列表里
    corpus = []
    def f(index, word):
        while(len(corpus) <= index):
            corpus.append('')
        corpus[index] += ' ' + word

    '''
    index = 0
    for filename in os.listdir(dir_path):
        try:
            td_file = open(os.path.join(dir_path, filename))
            td_content = td_file.read()
        finally:
            td_file.close()
        seg_list = jieba.cut(td_content)
        for word in seg_list:
            word = word.strip()
            if len(word) > 0 and word not in stop_words:
                f(index, word)
        index += 1


def docfile_handler(filepath, f):
    '''
    对某文档，进行遍历分词和对每篇执行f回调函数
    :param dir_path:
    :param f: f(index, word)，表示第几篇的什么单词，利用全局变量或闭包，引用等完成值传递或者操作
    :return: void
    '''
    try:
        td_file = open(filepath)
        td_content = td_file.read()
    finally:
        td_file.close()
    seg_list = jieba.cut(td_content)
    for word in seg_list:
        word = word.strip()
        if len(word) > 0 and word not in stop_words:
            f(0, word)

if __name__ == '__main__':

    # 测试文件，每个文档一行
    # file = open('text_data.txt')
    # for line in file.readlines():
    #     seg_list = jieba.cut(line)
    #     # print '/ '.join(seg_list)
    #     filtered = ''
    #     for word in seg_list:
    #         word = word.strip()
    #         if len(word)>0 and word not in stop_words:
    #             filtered += ' /' + word
    #     print filtered
    #
    # file.close()

    # 测试文件，读取一个目录下所有文件
    dir_path = 'text_data'
    #存储读取语料 一行预料为一个文档
    corpus = []
    for filename in os.listdir(dir_path):
        td_file = open(os.path.join(dir_path, filename))
        td_content = td_file.read()
        td_file.close()
        seg_list = jieba.cut(td_content)
        filtered = ''
        for word in seg_list:
            word = word.strip()
            if len(word)>0 and word not in stop_words:
                filtered += ' /' + word
        print filtered
