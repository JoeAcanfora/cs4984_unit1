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
from nltk.corpus import stopwords

from nltk.tag.stanford import NERTagger 

dir_path = '/Users/davidkeimig/Desktop/flood/China_Flood'
path = dir_path + "/*.txt"
list_txt = glob.glob(path)
all_toks_class = list()

mit_stopwords = open("../ref/english.stop").read().split('\n')

stopset = set(stopwords.words('english') + mit_stopwords)
for txt in list_txt:
	file_y = open(txt).read()
	tokens = word_tokenize(file_y)
	for value in tokens:
		all_toks_class.append(value)

good_toks = [w.lower() for w in all_toks_class if not w.lower() in stopset and not w.isdigit() and w.isalpha() and len(w) >= 4 and len(w) < 125]

st = NERTagger('./stanford-ner/english.all.3class.distsim.crf.ser.gz','./stanford-ner/stanford-ner.jar')
tagged_words = st.tag(good_toks)
print tagged_words

