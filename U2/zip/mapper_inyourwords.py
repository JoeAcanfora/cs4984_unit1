#!/usr/bin/env python

"""
Mapper
"""

import sys
import zipimport

importer = zipimport.zipimporter('nltk.mod')
nltk = importer.load_module("nltk")

nltk.data.path += ["./nltkData/"]
from nltk.corpus import stopwords

stopwords = stopwords.words('english')
#lines = open(sys.argv[1]).read().splitlines()
#stopwords = set([l.strip().lower() for l in lines])

yourwords = [ "flood",
	  "rain",
	  "overflow",
	  "dam",
	  "storm",
	  "severe",
	  "water",
	  "damage",
	  "submerge",
	  "washed",
	  "collapsed",
	  "river",
	  "discharge ",
	  "downpour",
	  "downstream",
	  "flash",
	  "levee",
	  "swept",
	  "torrential",
	  "runoff"]

for line in sys.stdin:
    line = line.decode('utf8')
    words = nltk.word_tokenize(line)
    words = [w.lower() for w in words if w not in stopwords]

    for word in words:
	value = 1 if word in yourwords else 0
        print("{0}\t{1}".format(word.encode('utf-8'), value));
