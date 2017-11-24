# -*- encoding: utf-8 -*-
import re

__author__ = 'GalaIO'

import jieba
import os

# 载入停用词，放入列表
try:
    sw_file = open('resource/stop_words.txt')
    stop_words = [word.strip().decode('utf-8') for word in sw_file.readlines()]
    swp_file = open('resource/stop_word_pattern.txt')
    stop_word_patterns = [word.strip().decode('utf-8') for word in swp_file.readlines()]
    # stop_words = []
    # print stop_words
finally:
    sw_file.close()


# 匹配停用词规则
def pattern_check(str, pattern_list):
    for pattern in pattern_list:
        if re.match(pattern, str):
            return True
    return False

def docdir_handler(dir_path, f, stop_word_list=stop_words, stop_word_pattern_list=stop_word_patterns):
    '''
    对某一目录下的所有文档，进行遍历分词和对每篇执行f回调函数
    :param dir_path:
    :param f: f(index, word)，表示第几篇的什么单词，利用全局变量或闭包，引用等完成值传递或者操作
    :return: 所有文件名 和 原始文档

    这是f的一个例子，把每个文档的词连为一个字符串，同时存在列表里
    corpus = []
    def f(index, word):
        while(len(corpus) <= index):
            corpus.append('')
        corpus[index] += ' ' + word

    '''
    index = 0
    filenames = []
    docs = []
    print('start cut....')
    print('start filter stopword...')
    for filename in os.listdir(dir_path):
        filenames.append(filename)
        try:
            td_file = open(os.path.join(dir_path, filename))
            td_content = td_file.read()
        finally:
            td_file.close()
        docs.append(td_content)
        seg_list = jieba.cut(td_content)
        for word in seg_list:
            word = word.strip()
            # 检查是否是停用词
            if len(word) > 0 and word not in stop_word_list and not pattern_check(word, stop_word_patterns) :
                f(index, word)
        index += 1
    return filenames, docs


def docfile_handler(filepath, f, stop_wordss=stop_words):
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
        if len(word) > 0 and word not in stop_wordss:
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
    # dir_path = 'text_data'
    dir_path = 'sspider/data'
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
