# -*- encoding: utf-8 -*-
__author__ = 'GalaIO'

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

import jieba_util
import word_cloud_util
from sklearn.feature_extraction.text import CountVectorizer

if __name__ == '__main__':
    # 存储读取语料 一行预料为一个文档
    corpus = []
    def f(index, word):
        while(len(corpus) <= index):
            corpus.append('')
        corpus[index] += ' ' + word
    jieba_util.docdir_handler('text_data', f)
    # print corpus
    # print len(corpus)

    word_cloud_util.gen_by_text(corpus[0]+corpus[1]+corpus[2], font_path='resource/simkai.ttf', image_path='resource/cloud.jpg', save_path='re.png')

    # 将文本中的词语转换为词频矩阵 矩阵元素a[i][j] 表示j词在i类文本下的词频
    vectorizer = CountVectorizer()
    # print vectorizer

    X = vectorizer.fit_transform(corpus)
    vocab = vectorizer.get_feature_names()
    analyze = vectorizer.build_analyzer()
    weight = X.toarray()
    # print weight
    # print len(weight)

    # LDA算法
    print 'LDA:'
    import numpy as np
    import lda
    import lda.datasets

    model = lda.LDA(n_topics=3, n_iter=50, random_state=1)
    model.fit(np.asarray(weight, dtype=np.int32))  # model.fit_transform(X) is also available

    ####### 显示结果
    topic_word = model.topic_word_
    print("type(topic_word): {}".format(type(topic_word)))
    print("shape: {}".format(topic_word.shape))
    print(vocab[:3])
    print(topic_word[:, :3])

    # 计算每个主题中的前5个单词
    n = 5
    text = ''
    for i, topic_dist in enumerate(topic_word):
        topic_words = np.array(vocab)[np.argsort(topic_dist)][:-(n + 1):-1]
        line_show = ' '.join(topic_words)
        print('*Topic {}\n- {}'.format(i, line_show))
        text += line_show

    print text

    # 计算输入前10篇文章最可能的Topic
    doc_topic = model.doc_topic_
    # print("type(doc_topic): {}".format(type(doc_topic)))
    # print("shape: {}".format(doc_topic.shape))
    for n in range(len(doc_topic)):
        topic_most_pr = doc_topic[n].argmax()
        print("doc: {} topic: {}".format(n, topic_most_pr))


    word_cloud_util.gen_by_text(text, font_path='resource/simkai.ttf', image_path='resource/cloud.jpg')
