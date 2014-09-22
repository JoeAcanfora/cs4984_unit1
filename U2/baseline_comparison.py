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

from nltk.book import *
import dateutil
import pyparsing
import numpy
import six
from nltk.corpus import PlaintextCorpusReader
corpus_root = '/Users/davidkeimig/Desktop/Islip13Rain_edit'
wordlists = PlaintextCorpusReader(corpus_root, '.*')
wordlists.fileids()
ClassEvent = Text(wordlists.words())


dir_path = '/Users/davidkeimig/Desktop/flood/China_Flood'
path = dir_path + "/*.txt"
list_txt = glob.glob(path)
all_toks_china = list()

for txt in list_txt:
	file_y = open(txt).read()
	tokens = word_tokenize(file_y)
	all_toks_china = all_toks_china + tokens

brown_cats = brown.categories()
all_toks_brown = list()

reuters_cats = reuters.categories()
all_toks_reuters = list()

state_union_cats = state_union.fileids()
all_toks_state_union = list()

complete_toks = list()

linux_words = open("../ref/words").read().split('\n')
linux_set = set(linux_words)

for cat in brown_cats:
	words = brown.words(categories=cat)
	tokens = [w.lower() for w in words]
	all_toks_brown = all_toks_brown + tokens
	complete_toks = complete_toks + tokens

for cat in reuters_cats:
	words = reuters.words(categories=cat)
	tokens = [w.lower() for w in words]
	all_toks_reuters = all_toks_reuters + tokens
	complete_toks = complete_toks + tokens

for cat in state_union_cats:
	words = state_union.words(cat)
	tokens = [w.lower() for w in words]
	all_toks_state_union = all_toks_state_union + tokens
	complete_toks = complete_toks + tokens

for word in linux_words:
	complete_toks.append(word)


#list_brown = list()
#for word in all_toks_brown:
#	word_length = len(word)
#	list_brown = list_brown + word_length

cnt_brown = Counter()
cnt_reuters = Counter()
cnt_state_union = Counter()
cnt_linux = Counter()

for word in all_toks_brown:
	cnt_brown[len(word)] += 1

for word in all_toks_reuters:
	cnt_reuters[len(word)] += 1

for word in all_toks_state_union:
	cnt_state_union[len(word)] += 1

for word in linux_set:
	cnt_linux[len(word)] += 1

print "\nBrown Corpus Word Length\n"
for freq in cnt_brown.items():
    print('Number of Characters {}:   Count {}'.format(freq[0], freq[1]))

print "\nReuters Corpus Word Length\n"
for freq in cnt_reuters.items():
    print('Number of Characters {}:   Count {}'.format(freq[0], freq[1]))

print "\nState of the Union Corpus Word Length\n"
for freq in cnt_state_union.items():
    print('Number of Characters {}:   Count {}'.format(freq[0], freq[1]))

print "\nEnglish Corpus Word Length\n"
for freq in cnt_linux.items():
    print('Number of Characters {}:   Count {}'.format(freq[0], freq[1]))

complete_txt = Text(complete_toks)
flood_words = open("../ref/yourwords.txt").read().split('\n')
flood_set = set(flood_words)

syn_flood_set = list()

for item in flood_set:
	for synset in wn.synsets(str(item)):
		for name in synset.lemma_names:
			syn_flood_set.append(name)

found = [w for w in complete_txt if w.lower() in syn_flood_set]
fdist1 = FreqDist(found)

found_ClassEvent = [w.lower() for w in wordlists.words() if w.lower() in syn_flood_set]
fdist2 = FreqDist(found_ClassEvent)

found_china = [w.lower() for w in all_toks_china if w.lower() in syn_flood_set]
fdist3 = FreqDist(found_china)

print('\n{label1:<15}  {label2}'.format(label1='YourWords', label2='Baseline Percent'))
total_list = list()
for item in fdist1.items():
	percent_list = list()
	percent = (item[1] / len(complete_txt)) * 100
	percent_list.append(item[0])
	percent_list.append(percent)
	total_list = total_list + percent_list
	print('{word:<15} | {count}'.format(word=item[0], count=percent))

print('\n{label1:<15}  {label2}'.format(label1='YourWords', label2='ClassEvent Percent'))

new_total = list()
for item in fdist2.items():
	percent_list = list()
	percent = (item[1] / len(complete_txt)) * 100
	percent_list.append(item[0])
	percent_list.append(percent)
	new_total = new_total + percent_list
	print('{word:<15} | {count}'.format(word=item[0], count=percent))

print('\n{label1:<15}  {label2}'.format(label1='YourWords', label2='YourSmall Percent'))

new_total_2 = list()
for item in fdist3.items():
	percent_list = list()
	percent = (item[1] / len(complete_txt)) * 100
	percent_list.append(item[0])
	percent_list.append(percent)
	new_total_2 = new_total_2 + percent_list
	print('{word:<15} | {count}'.format(word=item[0], count=percent))
