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
voc = set()

def f(index, word):
    while (len(corpus) <= index):
        corpus.append([])
    corpus[index].append(word)
    voc.add(word)

filenames, docs = jieba_util.docdir_handler_tfidf('sspider/data', f)
# filenames, docs = jieba_util.docdir_handler('sspider/data-160', f)
labels = [['健康', '长寿', '锻炼', '生活', '心理', '饮食']] * len(docs)
# labels = [[name.decode('GB2312').rstrip('.txt') for name in filenames]] * len(docs)
# labels = [name.decode('GB2312').rstrip('.txt').split(' ') for name in filenames]
# print corpus
# print len(corpus)
# print ', '.join([''.join(i) for i in labels])

labelset = list(set(reduce(list.__add__, labels)))

llda = LLDA(K=50, alpha=1.0/len(labels), beta=1.0/len(voc))
llda.set_corpus(labelset, corpus, labels)

vocab = llda.vocas
iter_count = 50

print "M=%d, V=%d, L=%d, K=%d, W=%d" % (len(corpus), len(llda.vocas), len(labelset), iter_count, len(vocab))

for i in range(iter_count):
    sys.stderr.write("-- %d : %.4f\n" % (i, llda.perplexity()))
    llda.inference()
print "perplexity : %.4f" % llda.perplexity()

topic_word = llda.phi()

# 计算每个主题中的前5个单词
n = 15
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