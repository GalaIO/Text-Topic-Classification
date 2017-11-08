# -*- encoding: utf-8 -*-
__author__ = 'GalaIO'
import numpy as np
import lda
import lda.datasets


####### 输入数据，是lda自带的路透社的共395个文档，4258个单词
# X矩阵为395*4258，共395个文档，4258个单词，主要用于计算每行文档单词出现的次数（词频），然后输出X[5,5]矩阵；
# vocab为具体的单词，共4258个，它对应X的一行数据，其中输出的前5个单词，X中第0列对应church，其值为词频；
# titles为载入的文章标题，共395篇文章，同时输出0~4篇文章标题如下。

# document-term matrix
X = lda.datasets.load_reuters()
print 'type(x): {}'.format(type(X))
print 'shape: {}\n'.format(X.shape)
print X[:5, :5]

# the vocab
vocab = lda.datasets.load_reuters_vocab()
print("type(vocab): {}".format(type(vocab)))
print("len(vocab): {}\n".format(len(vocab)))
print(vocab[:5])

# titles for each story
titles = lda.datasets.load_reuters_titles()
print("type(titles): {}".format(type(titles)))
print("len(titles): {}\n".format(len(titles)))
print(titles[:5])

####### 训练模型
# 其中设置20个主题，500次迭代
model = lda.LDA(n_topics=20, n_iter=500, random_state=1)
# model.fit_transform(X) is also available
model.fit(X)


####### 显示结果
topic_word = model.topic_word_
print("type(topic_word): {}".format(type(topic_word)))
print("shape: {}".format(topic_word.shape))
print(vocab[:3])
print(topic_word[:, :3])

n = 5
for i, topic_dist in enumerate(topic_word):
    topic_words = np.array(vocab)[np.argsort(topic_dist)][:-(n+1):-1]
    print('*Topic {}\n- {}'.format(i, ' '.join(topic_words)))