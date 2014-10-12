from __future__ import division
import nltk
from nltk import *
import sys
import glob
import os
from nltk.corpus import stopwords
import matplotlib.pyplot as plt

dir_path = '/Users/davidkeimig/Desktop/flood/China_Flood'
path = dir_path + "/*.txt"
list_txt = glob.glob(path)
all_toks_china = list()

for txt in list_txt:
	file_y = open(txt).read()
	tokens = word_tokenize(file_y)
	all_toks_china = all_toks_china + tokens

mit_stopwords = open("../ref/english.stop").read().split('\n')

stopset = set(stopwords.words('english') + mit_stopwords)

good_toks = [w.lower() for w in all_toks_china if not w.lower() in stopset and not w.isdigit() and w.isalpha() and len(w) >= 4]

bigram_measures = collocations.BigramAssocMeasures()
finder = BigramCollocationFinder.from_words(good_toks)
finder.apply_freq_filter(3)
scores = finder.score_ngrams(bigram_measures.raw_freq)
count = finder.ngram_fd.items()

print count[:50]