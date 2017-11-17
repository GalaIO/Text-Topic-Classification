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
    # 先计算td-idf
    # 存储读取语料 一行预料为一个文档
    corpus = []


    def f(index, word):
        while (len(corpus) <= index):
            corpus.append('')
        corpus[index] += ' ' + word


    jieba_util.docdir_handler('text_data', f)
    # print corpus
    # print len(corpus)

    vectorizer = CountVectorizer()  # 该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频
    transformer = TfidfTransformer()  # 该类会统计每个词语的tf-idf权值
    tfidf = transformer.fit_transform(
        vectorizer.fit_transform(corpus))  # 第一个fit_transform是计算tf-idf，第二个fit_transform是将文本转为词频矩阵
    word = vectorizer.get_feature_names()  # 获取词袋模型中的所有词语
    weight = tfidf.toarray()
    # 统计前n个关键词
    n = 5
    tfidf_keyword_re = []
    for samp in weight:
        samp_keyword = np.asarray(word)[np.argsort(samp)][:-(n+1):-1]
        tfidf_keyword_re.append(' '.join(samp_keyword))
    print ', '.join(tfidf_keyword_re)

    # 直接对向量矩阵计算k-means
    print 'Start Kmeans:'
    # 簇的个数
    clu_n = 2
    from sklearn.cluster import KMeans
    clf = KMeans(n_clusters=clu_n)
    s = clf.fit(weight)
    print s

    # 打印中心点
    print clf.cluster_centers_
    # 打印样本簇
    print clf.labels_
    # 用来评估簇的个数是否合适，距离越小说明簇分的越好，选取临界点的簇个数
    print(clf.inertia_)

    # 输出格式化结果
    for j in range(0, clu_n):
        print 'label %d' % j
        # 寻找对应的label索引，然后打印对应的关键字序列
        for index, label_index in enumerate(clf.labels_):
            if label_index == j:
                print tfidf_keyword_re[index]
