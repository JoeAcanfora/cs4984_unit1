#!/usr/bin/python2

import nltk
import os
import sys

""" Unit 1 """

dir = "../data"
if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
    dir = sys.argv[1]

# Raw Frequent Words #
######################
# read each file and put tokens into a list
tokens = []
for file in os.listdir(dir):
    raw = open(os.path.join(dir, file)).read()
    raw = raw.decode('utf8')
    t = nltk.word_tokenize(raw)
    t = [w.lower() for w in t]    # make words lowercase
    tokens += t

# plot the frequency distribution of the tokens
fdist1 = nltk.FreqDist(tokens)
print("Top 20 Words")
for word in fdist1.most_common(20):
    print(word)
fdist1.plot(50, cumulative=True)


