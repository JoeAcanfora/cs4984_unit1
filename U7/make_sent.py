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

dir_path = '/Users/davidkeimig/Desktop/PAK_FLOOD/Pakistan_Flood'
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
	sent = "";
	for r in good_toks:
		sent = sent + r
		sent = sent + " "
	with open("./PakSentFiles/"+ str(count) + ".txt", "a") as file:
		file.write(sent)
