#!/usr/bin/python2

from __future__ import division

import nltk
import os
import sys

""" 
Unit 1 
------
Usage: python wordlength_dist.py textdirectory/
"""


if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
    dir = sys.argv[1]
else:
    print("Please specify a directory of .txt files")
    

# read each file and put tokens into a list
stopwords = nltk.corpus.stopwords.words('english')
tokens = []
for file in os.listdir(dir):
    raw = open(os.path.join(dir, file)).read()
    raw = raw.decode('utf8')
    t = nltk.word_tokenize(raw)
    t = [w.lower() for w in t]
    tokens += t

## 7.2
# find percentage of words not in stop list
tokens_nostop = [w for w in tokens if w not in stopwords]
percent_nostop = len(tokens_nostop) / len(tokens) * 100
print("Percent of tokens not in stopwords: {0:.4f}%".format(percent_nostop))

## 7.3
# wordlength distribution
wl = [len(w) for w in tokens if len(w) in range(1,16)]
wl_nostop = [len(w) for w in tokens_nostop if len(w) in range(1,16)]
fdist_wl = nltk.FreqDist(wl)
fdist_wl_ns = nltk.FreqDist(wl_nostop)
print("FreqDist of wordlengths (w/ stopwords)")
sorted_fdist = sorted(fdist_wl.items(), key=lambda freq: freq[1])[::-1]
for wordlength in sorted_fdist:
    print(wordlength)

print("FreqDist of wordlengths (w/o stopwords)")
sorted_fdist = sorted(fdist_wl_ns.items(), key=lambda freq: freq[1])[::-1]
for wordlength in sorted_fdist:
    print(wordlength)

## 7.4
# percentage of each word in yourwords
print("Percentage of YourWords out of " + str(len(tokens_nostop))) 
yourwords = open("../ref/yourwords.txt").read().split('\n')
yourwords = [w.lower().strip() for w in yourwords]
percentages = []
for word in yourwords:
    count = tokens_nostop.count(word)
    percent = count // len(tokens_nostop)
    percentages.append((word, count))

# sort and print
percentages = sorted(percentages, key=lambda word: word[1])[::-1]
print "{0:>12} {1:^22} {2}".format("WORD", "%", "COUNT")
for item in percentages:
    word = item[0]
    count = item[1]
    percent = count // len(tokens_nostop)
    print "{0:>12} {1:.20f} {2}".format(word, percent, count)


