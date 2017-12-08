# -*- encoding: utf-8 -*-
__author__ = 'GalaIO'

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

import jieba_util
import os
import word_cloud_util
import numpy as np
import json
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer


def tfidf_filter(corpus, scale=0.9):
    result = []
    def result_handler(index, word):
        while(len(result) <= index):
            result.append([])
        result[index].append(word)
    vectorizer = CountVectorizer(dtype=np.int32)
    transformer = TfidfTransformer()
    tfidf = transformer.fit_transform(
        vectorizer.fit_transform(corpus))
    vocas = vectorizer.get_feature_names()
    # weight = tfidf.toarray()
    weight = tfidf
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
                    result_handler(index, word)
            except ValueError, e:
                result_handler(index, word)
            else:
                tfidf_filtered_count += 1
    print 'tf-idf contribute the filter %d' % tfidf_filtered_count
    return result

if __name__ == '__main__':
    save_file = './data_cut_result.txt'
    data_dir = 'sspider/data'
    if os.path.exists(save_file):
        print 'use chched....'
        filenames, corpus = jieba_util.load_save_file(save_file)
        filenames2, docs = jieba_util.load_docs(data_dir)
    else:
        print 'caculate....'
        filenames, docs, corpus = jieba_util.docdir_handler_backup(data_dir, save_filename=save_file)
        corpus = [' '.join(doc) for doc in corpus]

    print 'tfidf filter...'
    result = tfidf_filter(corpus, scale=0.99)
    # 替换为新的语料
    corpus = [' '.join(doc) for doc in result]

    print('start wordcloud....')
    word_cloud_util.gen_by_text(' '.join(corpus), font_path='resource/simkai.ttf', image_path='resource/cloud.jpg', save_path='re.png')


    print ('start vector...')
    # 将文本中的词语转换为词频矩阵 矩阵元素a[i][j] 表示j词在i类文本下的词频
    vectorizer = CountVectorizer(dtype=np.int32)
    # print vectorizer

    X = vectorizer.fit_transform(corpus)
    vocab = vectorizer.get_feature_names()
    # analyze = vectorizer.build_analyzer()
    # weight = X.toarray()
    # print weight
    # print len(weight)

    # LDA算法
    print 'LDA:'
    import numpy as np
    import lda
    import lda.datasets

    topic_num = 10
    topic_words_count = 20
    model = lda.LDA(n_topics=topic_num, n_iter=500, random_state=1)
    model.fit(X)  # model.fit_transform(X) is also available

    ####### 显示结果
    topic_word = model.topic_word_
    print("type(topic_word): {}".format(type(topic_word)))
    print("shape: {}".format(topic_word.shape))
    print(vocab[:topic_num])
    print(topic_word[:, :topic_num])

    # 计算每个主题中的前5个单词
    text = ''
    topic_stat = []
    for i, topic_dist in enumerate(topic_word):
        topic_words = np.array(vocab)[np.argsort(topic_dist)][:-(topic_words_count + 1):-1]
        line_show = ' '.join(topic_words)
        print('*Topic {}\n- {}'.format(i, line_show))
        topic_stat.append({'description': line_show, 'docs': []})
        text += line_show

    # print text

    # 计算输入前10篇文章最可能的Topic
    doc_topic = model.doc_topic_
    # print("type(doc_topic): {}".format(type(doc_topic)))
    # print("shape: {}".format(doc_topic.shape))
    for topic_words_count in range(len(doc_topic)):
        topic_most_pr = doc_topic[topic_words_count].argmax()
        # print("doc: {} topic: {}".format(topic_words_count, topic_most_pr))
        doc = docs[topic_words_count]
        topic_stat[topic_most_pr]['docs'].append(doc[:doc.index('\n')])

    for top in topic_stat:
        print '%s\r\n%s\n\n\n' % (top['description'], '\r\n'.join(top['docs']))

    word_cloud_util.gen_by_text(text, font_path='resource/simkai.ttf', image_path='resource/cloud.jpg')
