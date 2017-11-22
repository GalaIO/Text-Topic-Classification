# -*- encoding: utf-8 -*-
__author__ = 'GalaIO'

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

import jieba_util
from llda import LLDA
import numpy

# 存储读取语料 一行预料为一个文档
corpus = []

def f(index, word):
    while (len(corpus) <= index):
        corpus.append([])
    corpus[index].append(word)

filenames = jieba_util.docdir_handler('text_data', f)
labels = [name.decode('GB2312').rstrip('.txt').split(' ') for name in filenames]
# print corpus
# print len(corpus)
print ', '.join([''.join(i) for i in labels])

labelset = list(set(reduce(list.__add__, labels)))

llda = LLDA(K=50, alpha=0.001, beta=0.001)
llda.set_corpus(labelset, corpus, labels)

vocab = llda.vocas

print "M=%d, V=%d, L=%d, K=%d, W=%d" % (len(corpus), len(llda.vocas), len(labelset), 50, len(vocab))

for i in range(50):
    sys.stderr.write("-- %d : %.4f\n" % (i, llda.perplexity()))
    llda.inference()
print "perplexity : %.4f" % llda.perplexity()

topic_word = llda.phi()

# 计算每个主题中的前5个单词
n = 5
for k, label in enumerate(labelset):
    # 打印前20个每个label的单词重要度
    # print "\n-- label %d : %s" % (k, label)
    # for w in numpy.argsort(-phi[k])[:20]:
    #     print "%s: %.4f" % (llda.vocas[w], phi[k,w])
    ow = numpy.asarray(vocab)[numpy.argsort(topic_word[k])][:-(n+1):-1]
    print "%d-%s:\r\n%s" % (k, label, ', '.join(ow))

# 计算输入前10篇文章最可能的Topic
doc_topic = llda.dhi()
for n in range(len(doc_topic)):
    topic_most_pr = doc_topic[n].argmax()
    print("doc: {}\r\n {}\r\n topic: {}".format(n, ' '.join(corpus[n]), topic_most_pr))