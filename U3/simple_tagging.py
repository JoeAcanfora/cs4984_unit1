from __future__ import division

import nltk
from nltk.corpus import brown
from nltk.corpus import reuters
from nltk.corpus import state_union
import sys
import glob
import os

from nltk.corpus import wordnet as wn

from collections import Counter
from tabulate import tabulate

import time
import numpy as np
import matplotlib.pyplot as plt

import dateutil
import pyparsing
import numpy
import six
from nltk.corpus import PlaintextCorpusReader

from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters
from nltk.tokenize import sent_tokenize

corpus_root = '/Users/davidkeimig/Desktop/Islip13Rain_edit'
wordlists = PlaintextCorpusReader(corpus_root, '.*')
wordlists.fileids()
ClassEvent = nltk.Text(wordlists.words())

found_ClassEvent = [w.lower() for w in wordlists.words()]

punkt_param = PunktParameters()
punkt_param.abbrev_types = set(['dr', 'vs', 'mr', 'mrs', 'prof', 'inc'])
sentence_splitter = PunktSentenceTokenizer(punkt_param)

dir_path = str(sys.argv[1])
path = dir_path + "/*.txt"
list_txt = glob.glob(path)

all_sent = list()

for txt in list_txt:
	file_y = open(txt).read()
	tokens = sent_tokenize(file_y)
	all_sent = all_sent + tokens

for sent in all_sent:
	text = nltk.word_tokenize(sent)
	value = [word.lower() for word in text]
	results = nltk.pos_tag(value)
	print "SENT: "
	print results
	print "\n"
	
