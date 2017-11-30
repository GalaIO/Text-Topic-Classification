# -*- encoding: utf-8 -*-
import re

__author__ = 'GalaIO'

import jieba
import os
from sklearn.feature_extraction.text import TfidfTransformer, TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np

# 载入停用词，放入列表
try:
    sw_file = open('resource/stop_words.txt')
    stop_words = set([word.strip().decode('utf-8') for word in sw_file.readlines()])
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
    filtered_words = set()
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
            if len(word) > 0 and word not in filtered_words and word not in stop_word_list and not pattern_check(word, stop_word_patterns) :
                f(index, word)
            else:
                # 备份被去掉的单词，加快匹配
                filtered_words.add(word)
        index += 1
    return filenames, docs

def docdir_handler_tfidf(dir_path, f, stop_word_list=stop_words, stop_word_pattern_list=stop_word_patterns, scale=0.9):
    '''
    对某一目录下的所有文档，进行遍历分词和对每篇执行f回调函数
    先进行一遍tf-idf去掉 非重要词 默认阈值0.5 即在没文档的tfidf中去掉较小的50%
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
    corpus = []
    filtered_words = set()
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
            if len(word) > 0 and word not in filtered_words and word not in stop_word_list and not pattern_check(word, stop_word_patterns) :
                while (len(corpus) <= index):
                    corpus.append([])
                corpus[index].append(word)
            else:
                # 备份被去掉的单词，加快匹配
                filtered_words.add(word)
        index += 1
    vectorizer = CountVectorizer()
    transformer = TfidfTransformer()
    tfidf = transformer.fit_transform(
        vectorizer.fit_transform([' '.join(doc) for doc in corpus]))
    vocas = vectorizer.get_feature_names()
    weight = tfidf.toarray()
    tfidf_filtered_count = 0
    # 计算总文档的tf-idf
    col_weight = np.sum(weight, 0)
    ti = list(np.asarray(vocas)[np.argsort(col_weight)])
    for index, row in enumerate(weight):
        # 计算该文档的tf-idf
        # ti = list(np.asarray(vocas)[np.argsort(row)])
        for word in corpus[index]:
            try:
                if ti.index(word) >= len(vocas) * scale:
                    f(index, word)
            except ValueError, e:
                f(index, word)
            else:
                tfidf_filtered_count += 1
    print 'tf-idf contribute the filter %d' % tfidf_filtered_count
    return filenames, docs


def docfile_handler(filepath, f, stop_word_list=stop_words):
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
        if len(word) > 0 and word not in stop_word_list and not pattern_check(word, stop_word_patterns):
            f(0, word)

if __name__ == '__main__':

    # 测试文件，每个文档一行
    # file = open('sspider/data-20/17.txt')
    # for line in file.readlines():
    #     seg_list = jieba.cut(line)
    #     # print '/ '.join(seg_list)
    #     filtered = ''
    #     for word in seg_list:
    #         word = word.strip()
    #         if len(word)>0 and word not in stop_words and not pattern_check(word, stop_word_patterns) :
    #             filtered += ' /' + word
    #     print filtered
    #
    # file.close()

    # 存储读取语料 一行预料为一个文档
    import datetime
    corpus = []

    print datetime.datetime.now()
    def f(index, word):
        while(len(corpus) <= index):
            corpus.append('')
        corpus[index] += ' ' + word


    filenames, docs = docdir_handler('sspider/data-160', f)
    print '\r\n'.join(corpus)
    print datetime.datetime.now()

    corpus = []
    filenames, docs = docdir_handler_tfidf('sspider/data-160', f)
    print '\r\n'.join(corpus)
    print datetime.datetime.now()
