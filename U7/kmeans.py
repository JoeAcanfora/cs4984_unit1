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

dir_path = '/Users/davidkeimig/Desktop/Islip13Rain_edit'
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
for x in all_toks_china:
	x = re.sub('\s+', ' ', x)
	words = word_tokenize(x)
	good_toks = [w.lower() for w in words if not w.lower() in stopset and not w.isdigit() and w.isalpha() and len(w) >= 2]
	YourWordsSynsets = list()
	
	for word in good_toks:
		dictionary.add(find_lemma(word))

vector_total = dict()
for x in all_toks_china:
	vector = vectorize_sent(x, dictionary)
	vector_total[x] = vector
vectors = vector_total.values()
clusterer = cluster.KMeansClusterer(2, euclidean_distance) 
result = clusterer.cluster(vectors, True)

print('Clustered:', vectors)
print('As:', result)
print('Means:', clusterer.means())
print('Cluster Names:', clusterer.cluster_names())

# how do we:
#	find the centroid
#	find vectors closest to centroids
# 	map vector to sentence natively

print(clusterer.classify_vectorspace(vectorize_sent('islip long island flooding rain heavy pour down on New York hard', dictionary)))

print(clusterer._centroid(result, clusterer.means()))