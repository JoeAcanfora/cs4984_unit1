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

import pickle
import re

#f = open('maxEnt.pickle', 'wb')

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

file_list = open('../ref/trainset.txt').readlines()
for line in file_list:
	tokens = word_tokenize(line)
	file_name = tokens[0]
	classify = tokens[1]
	dir_path = '/Users/davidkeimig/Desktop/flood/China_Flood/'
	path = dir_path + file_name
	file_y = open(path).read()
	words = word_tokenize(file_y)
	if (classify == 'positive'):
		all_train = all_train + [(name, 'pos') for name in words]
	else:
		all_train = all_train + [(name, 'neg') for name in words]

	print "Completed tagging " + file_name

featuresets = [(gender_features(n), gender) for (n, gender) in all_train]

print "starting training..."

#maxEnt = MaxentClassifier.train(featuresets)

f = open('maxEnt.pickle')
maxEnt = pickle.load(f)

dir_path = '/Users/davidkeimig/Desktop/flood/China_Flood'
path = dir_path + "/*.txt"
list_txt = glob.glob(path)
all_toks_china = list()

output_list = list()

for txt in list_txt:
	file_y = open(txt).read()
	tokens = word_tokenize(file_y)

	pos = 0
	neg = 0
	for test_word in tokens:
		out = maxEnt.classify({'word': test_word})
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

maxEnt.show_most_informative_features(40)

#pickle.dump(maxEnt, f)
f.close()




