__author__ = 'joeacanfora'

import nltk
import os
import sys
import collections
import mmap
from nltk.corpus import stopwords

dir = "/Users/joeacanfora/Desktop/Virginia Tech/Capstone/china_flood"

bigramDir = "/Users/joeacanfora/Desktop/Virginia Tech/Capstone/U4/Bigrams10k.txt"

bigram = open(bigramDir)


stopwords = nltk.corpus.stopwords.words('english')
tokens = []
i = 0
for file in os.listdir(dir):
    raw = open(os.path.join(dir, file)).read()
    raw = raw.decode('utf8')
    t = nltk.word_tokenize(raw)
    tokens += t

collocations = nltk.bigrams(tokens)

s = mmap.mmap(bigram.fileno(), 0, access=mmap.ACCESS_READ)

cnt = collections.Counter()
for gram in collocations :
    gram = gram.__str__().replace("u", "")
    if s.find(gram) != -1:
        cnt[gram] += 1

print cnt.most_common(50)









