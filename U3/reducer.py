#!/usr/bin/env python2

""" 
Reducer
"""

import sys
import zipimport


try:
    importer = zipimport.zipimporter('nltk.mod')
    nltk = importer.load_module("nltk")
    nltk.data.path += ["./nltkData/"]
except zipimport.ZipImportError:
    import nltk

sys.path.append("..")
import TextUtils as tu
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters
from nltk.tokenize import sent_tokenize

from cPickle import load

# punkt sentence tokenizer setup
punkt_param = PunktParameters()
punkt_param.abbrev_types = set(['dr', 'vs', 'mr', 'mrs', 'prof', 'inc'])
sentence_splitter = PunktSentenceTokenizer(punkt_param)

# load trained POS tagger from disk
input = open("t2.pkl", "rb")
tagger = load(input)
input.close()

current_word = None
current_count = 0
length = None

words = dict()

# treat each line as a filename
for line in sys.stdin:
    # read file and split into sentences
    num, filename = line.split('\t')
    file = open(filename.strip())
    raw = file.read()
    file.close()
    raw = raw.decode('utf8').lower()
    sents = sent_tokenize(raw)

    # pos-tag each word in the sentence
    for sent in sents:
        text = nltk.word_tokenize(sent)
        text = tu.filter_non_alpha_words(text)
        tagged_sent = tagger.tag(text)

        # then add it to our table of words and counts
        for tag in tagged_sent:
            key = "{0}\{1}".format(tag[0].encode('utf8'),tag[1])

            #words[key] = words.setdefault(key, default=0) + 1
            if key in words:
                words[key] += 1
            else:
                words[key]  = 1

from operator import itemgetter
sorted_words = sorted(words.items(), key=itemgetter(1), reverse=True)
for w in sorted_words:
    print("{0}\t{1}".format(*w))
