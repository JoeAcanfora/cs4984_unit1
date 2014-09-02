#!/usr/bin/python2

import nltk
import os
import sys

""" 
Unit 1 
------
Usage: python unit1_marc.py textdirectory/
"""


dir = "../data"
if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
    dir = sys.argv[1]

# Raw Frequent Words #
######################
# read each file and put tokens into a list
stopwords = nltk.corpus.stopwords.words('english')
tokens = []
for file in os.listdir(dir):
    raw = open(os.path.join(dir, file)).read()
    raw = raw.decode('utf8')
    t = nltk.word_tokenize(raw)
    # normalized case, alphanumeric words of length > 5
    t = [w.lower() for w in t if w.lower() not in stopwords and w.isalnum() and len(w) > 5]
    tokens += t

# plot the frequency distribution of the tokens
fdist1 = nltk.FreqDist(tokens)
print("Top 20 Words")
for word in fdist1.most_common(20):
    print("{word:<15} {count}".format(word=word[0],count=word[1]))
fdist1.plot(50, cumulative=True)
