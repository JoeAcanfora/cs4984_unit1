from __future__ import division

import nltk
from nltk import *
from nltk.corpus import brown
from nltk.corpus import reuters
from nltk.corpus import state_union
import sys
import glob
import os

from nltk.corpus import wordnet as wn

import sys

from nltk.corpus import PlaintextCorpusReader
from nltk.corpus import stopwords

from nltk.tag.stanford import NERTagger 

from nltk import chunk
from nltk import tag
import numpy

dir_path = sys.argv[1]
path = dir_path + "/*.txt"
list_txt = glob.glob(path)
all_toks_class = list()
all_sent = list()

mit_stopwords = open("../ref/english.stop").read().split('\n')

stopset = set(stopwords.words('english') + mit_stopwords)
for txt in list_txt:
	file_y = open(txt).read().decode('utf8')
	tokens = word_tokenize(file_y)
	for value in tokens:
		all_toks_class.append(value)

good_sent = [w.encode('ascii', 'replace') for w in all_sent if len(w) >= 10 and len(w) < 100]
good_toks = [w for w in all_toks_class if not w.lower() in stopset and not w.isdigit() and w.isalpha() and len(w) >= 4 and len(w) < 125]

fdist1 = FreqDist(good_toks)
most = fdist1.most_common(100)
list_values = list()
for word in most:
	list_values.append(word[0])

st = NERTagger('./stanford-ner/english.all.3class.distsim.crf.ser.gz','./stanford-ner/stanford-ner.jar')
tagged_words = st.tag(list_values)

tag_words = list()
for word in list_values:
	tag_words = tag_words + tag.pos_tag(word)

print "CHUNK WORDS:"
tree = chunk.ne_chunk(tagged_words)
print tree.draw

print "STANDFORD WORDS:"
for word in tagged_words:
	if (word[1] != 'O'):
		print word


