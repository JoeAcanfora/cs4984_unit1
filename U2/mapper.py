#!/usr/bin/env python2

"""
Mapper - 7.3: Wordlength Distribution


"""

import sys
import nltk

stopwords = nltk.corpus.stopwords.words('english')
#lines = open(sys.argv[1]).read().splitlines()
#stopwords = set([l.strip().lower() for l in lines])

for line in sys.stdin:
    line = line.decode('utf8')
    words = nltk.word_tokenize(line)
    wordlengths = [len(w) for w in words if w not in stopwords]

    for length in wordlengths:
        print("{0}\t{1}".format(length, 1));
