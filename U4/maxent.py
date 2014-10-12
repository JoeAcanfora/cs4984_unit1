from __future__ import division

import nltk
from nltk import *
import scipy
from scipy import *

import sys
import glob
import os

from nltk.corpus import wordnet as wn

from collections import Counter
from tabulate import tabulate

import dateutil
import pyparsing
import numpy
import six
from nltk.corpus import PlaintextCorpusReader

from nltk.classify import MaxentClassifier
from nltk.corpus import stopwords

import pickle
import re

import nltk.classify
from sklearn.svm import LinearSVC

f = open('NaiveBayesClassifier.pickle', 'wb')

all_train = list()

def gender_features(word):
	return {'word': word}

def tryint(s):
    try:
        return int(s)
    except:
        return s

def alphanum_key(s):
    return [ tryint(c) for c in re.split('([0-9]+)', s) ]

def sort_nicely(l):
    l.sort(key=alphanum_key)

print "Starting....\n"


mit_stopwords = open("../ref/english.stop").read().split('\n')
stopset = set(stopwords.words('english') + mit_stopwords)

all_train = []

file_list = open('../ref/trainset_small.txt').readlines()

dir_path = '/Users/davidkeimig/Desktop/flood/China_Flood'
path = dir_path + "/*.txt"
list_txt = glob.glob(path)
all_toks_china = list()

for txt in list_txt:
	file_y = open(txt).read()
	tokens = word_tokenize(file_y)
	all_toks_china = all_toks_china + tokens

good_toks = [w.lower() for w in all_toks_china if not w.lower() in stopset and not w.isdigit() and w.isalpha() and len(w) >= 2]

fdist2 = FreqDist(good_toks)
filt_set = [name[0] for name in fdist2.most_common(50)]
flood_words = open("../ref/yourwords.txt").read().split('\n')
flood_set = set(flood_words)
filt_set = [word for word in filt_set if not word.lower() in flood_set]

for line in file_list:
	file_name, classify = line.split('\t')

	dir_path = '/Users/davidkeimig/Desktop/flood/China_Flood/'
	path = dir_path + file_name
	file_y = open(path).read()
	words = word_tokenize(file_y)

	found = [w.lower() for w in words if not w.lower() in stopset and not w.isdigit() and w.isalpha() and not w.lower() in filt_set]
	fdist1 = FreqDist(found)

	#print fdist1.most_common(40)

	if (classify == 'positive\n'):
		all_train = all_train + [(name[0], 'pos') for name in fdist1.most_common(40)]
	else:
		all_train = all_train + [(name[0], 'neg') for name in fdist1.most_common(40)]

	print "Completed tagging " + file_name

featuresets = [(gender_features(n), gender) for (n, gender) in all_train]

print len(featuresets)

print "starting training..."

#maxEnt = DecisionTreeClassifier.train(featuresets[:5577])
maxEnt = NaiveBayesClassifier.train(featuresets[:5577])
#maxEnt = MaxentClassifier.train(featuresets[:5577])
#maxEnt = nltk.classify.SklearnClassifier(LinearSVC())
#maxEnt.train(featuresets[:5577])


#f = open('DecisionTreeClassifier.pickle')
#maxEnt = pickle.load(f)

dir_path = '/Users/davidkeimig/Desktop/flood/China_Flood'
path = dir_path + "/*.txt"
list_txt = glob.glob(path)
all_toks_china = list()

output_list = list()

test = [w[0].lower() for w in all_train]

for txt in list_txt:
	file_y = open(txt).read()
	tokens = word_tokenize(file_y)

	pos = 0
	neg = 0
	found = [w for w in tokens if w.lower() in test]
	for test_word in found:
		out = maxEnt.classify({'word': test_word.lower()})
		if (out == 'pos'):
			pos = pos + 1
		else:
 			neg = neg + 1

	get_file = txt.split('/')
	if (pos > neg):
		output_list.append(get_file[6] + "\tpositive")
	else:
		output_list.append(get_file[6] + "\tnegative")

print "finished training"
sort_nicely(output_list)
for value in output_list:
	print value


print 'Accuracy: %4.2f' % nltk.classify.accuracy(maxEnt, featuresets[5577:])

#maxEnt.show_most_informative_features(20)

pickle.dump(maxEnt, f)
f.close()




