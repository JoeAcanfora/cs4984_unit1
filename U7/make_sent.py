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
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters
from nltk.cluster import KMeansClusterer, euclidean_distance
from nltk.corpus import wordnet as wn

from nltk import cluster
from nltk.cluster import euclidean_distance
from numpy import array


mit_stopwords = open("../ref/english.stop").read().split('\n')
stopset = set(stopwords.words('english') + mit_stopwords)

all_train = []

file_list = open('../ref/trainset_small.txt').readlines()
your_words = open('../ref/yourwords.txt').readlines()
yourwords_list = set(your_words)

def letters(input):
    valids = []
    for character in input:
        if character.isalpha():
            valids.append(character)
    return ''.join(valids)

def find_lemma(word):
	lemma_list = list()
	synsets = nltk.corpus.wordnet.synsets(word)
	if len(synsets) == 0 or len(synsets[0].lemma_names()) == 0:
		return word
	for l in synsets:
		lemma_list = lemma_list + l.lemma_names()
	return lemma_list

synsets = list()
final_set = list()
for x in yourwords_list:
	print "first"
	sent = letters(x)
	value = find_lemma(sent)
	final_set = final_set + value

your_words = list()
for x in final_set:
	your_words.append(x.encode("ascii"))

dir_path = '/Users/davidkeimig/Documents/cs4984_unit1/cs4984_unit1/U1/china_flood'
path = dir_path + "/*.txt"
list_txt = glob.glob(path)
all_toks_china = list()


def vectorize_sent(sent, words):
	l = list(words)
	vector = [0] * len(l)

	tokes = word_tokenize(sent)
	for word in tokes:
		lemma = find_lemma(word)
		try:
			vector[l.index(lemma)] += 1
		except ValueError:
			pass

	return array(vector)

def find_lemma(word):
	lemma_list = list()
	synsets = nltk.corpus.wordnet.synsets(word)
	if len(synsets) == 0 or len(synsets[0].lemma_names()) == 0:
		return word

	return synsets[0].lemma_names()[0]


for txt in list_txt:
	file_y = open(txt).read()
	tokens = sent_tokenize(file_y)
	all_toks_china = all_toks_china + tokens

good_toks = list()
dictionary = set()
count = 0;
for x in all_toks_china:
	count = count + 1
	x = re.sub('\s+', ' ', x)
	words = word_tokenize(x)
	good_toks = [w.lower() for w in words if not w.lower() in stopset and not w.isdigit() and w.isalpha() and len(w) >= 2]
	once = 0
	for q in your_words:
		if q in good_toks:
			if once == 0:
				sent = ""
				for r in good_toks:
					sent = sent + r
					sent = sent + " "
				with open("./ChinaSentFiles/"+ str(count) + ".txt", "a") as file:
					file.write(sent)
				once = 1
