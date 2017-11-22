# -*- encoding: utf-8 -*-
__author__ = 'GalaIO'

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

import jieba_util
import word_cloud_util
from sklearn.feature_extraction.text import TfidfTransformer, TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np


if __name__ == '__main__':
    # 存储读取语料 一行预料为一个文档
    corpus = []


    def f(index, word):
        while (len(corpus) <= index):
            corpus.append('')
        corpus[index] += ' ' + word


    jieba_util.docdir_handler('text_data', f)
    # jieba_util.docdir_handler('text_data', f, stop_wordss=[])
    print '语料数据：'
    print '\r\n'.join(corpus)
    # print len(corpus)

    # 在sklearn中，默认有匹配模式
    ''' r"(?u)\b\w\w+\b"
        默认的正则表达式选择大于2的单词
        或更多的字母数字字符（标点符号被完全忽略
        并始终视为单词分隔符）。 可以直接分割英文，数字6 5 也会被忽略
    '''
    vectorizer = CountVectorizer()  # 该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频
    tf = vectorizer.fit_transform(corpus)
    weight = tf.toarray()
    words = vectorizer.get_feature_names()

    print '词频统计:'
    for cur in weight:
        print ', '.join(['{}: {}'.format(words[k], cur[k]) for k in range(0, len(cur))])


    # print words
    n = 5
    for i, row in enumerate(weight):
        row_sorted = np.asarray(words)[np.argsort(row)][:-(n + 1):-1]
        line_show = ' '.join(row_sorted)
        print('*Topic {}\n- {}'.format(i, line_show))