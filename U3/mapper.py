#!/usr/bin/env python2

"""
Mapper

Split the line into sentences (for now).
Use tagger to tag POS.
count occurrences of that word with POS.
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

# tokenize into sentences and tag
for line in sys.stdin:
    line = line.decode('utf8').lower()
    sents = sent_tokenize(line)

    for sent in sents:
        text = nltk.word_tokenize(sent)
        text = tu.filter_non_alpha_words(text)
        tagged_sent = tagger.tag(text)
        for tag in tagged_sent:
            print("{0}\t{1}\t1".format(tag[0].encode('utf8'),tag[1]))

