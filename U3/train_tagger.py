#!/usr/bin/env python

"""
A script that combines nltk annotated text corpora for parts of speech and
combines them into a custom training set. Then it trains a bigram tagger
based on the training set and saves it to disk as t2.pkl.

uses these corpora:
    brown
    conll 2000 chunking data
    treebank

unused:
    semcor
    penn treebank
    senseval 2 corpus
"""

corpora_names = [
        'brown',
        'conll2000',
        'treebank',
#        'ptb',
#        'semcor',
#        'senseval'
        ]

import nltk

# build the training sets
corpora = []
nc = __import__("nltk.corpus", fromlist=corpora_names)
for c in corpora_names:
    corpora.append(getattr(nc, c))

tagged_words = []
tagged_sents = []
for corpus in corpora:
    print("adding " + corpus.__name__)
    #tagged_words += corpus.tagged_words()
    tagged_sents += corpus.tagged_sents()

#print('Length of word training set:' +  str(len(tagged_words)))
print('Length of sentence training set:' +  str(len(tagged_sents)))

# train the taggers based off sentences
print("Training tagger...")
unigram_tagger = nltk.UnigramTagger(tagged_sents)
bigram_tagger = nltk.BigramTagger(tagged_sents)

t0 = nltk.DefaultTagger("NN")
t1 = nltk.UnigramTagger(tagged_sents, backoff=t0)
t2 = nltk.BigramTagger(tagged_sents, backoff=t1)

# save the tagger to disk
print("Saving tagger as t2.pkl")
from cPickle import dump
output = open("t2.pkl", "wb")
dump(t2, output, -1)
output.close()
