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
for line in sys.stdin:

# punkt sentence tokenizer setup
punkt_param = PunktParameters()
punkt_param.abbrev_types = set(['dr', 'vs', 'mr', 'mrs', 'prof', 'inc'])
sentence_splitter = PunktSentenceTokenizer(punkt_param)

# load trained POS tagger from disk
input = open("t2.pkl", "rb")
tagger = load(input)
input.close()

current_length = None
current_count = 0
length = None

# filen
for line in sys.stdin:
    line = line.decode('utf8').lower()
    sents = sent_tokenize(line)

    for sent in sents:
        text = nltk.word_tokenize(sent)
        text = tu.filter_non_alpha_words(text)
        tagged_sent = tagger.tag(text)
        for tag in tagged_sent:
            print("{0}\t{1}\t1".format(tag[0].encode('utf8'),tag[1]))

    line = line.strip()
    word, pos, count = line.split('\t')

    try:
        count = int(count)
    except ValueError:
        continue

    if current_word == word and current_pos == pos:
        current_count += count
    else:
        if current_word:
            print("{0}\t{1}\t{2}".format(word, pos, current_count))
        current_count = count
        current_word = word

if current_word == word and current_pos == pos:
    print("{0}\t{1}\t{2}".format(word, pos, current_count))
