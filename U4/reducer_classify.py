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

from cPickle import load

# load classifier from disk
classifier_file = sys.argv[1]
input = open(classifier_file, "rb")
classifier = load(input)
input.close()

# treat each line as "# filename.txt"
for line in sys.stdin:
    # read file and classify
    num, filename = line.split('\t')
    file = open(filename.strip())
    raw = file.read()
    file.close()
    raw = raw.decode('utf8').lower()

    tokens = nltk.word_tokenize(raw)
    tokens = [word.encode('utf8') for word in tokens]

    pos = 0
    neg = 0
    for word in tokens:
        word = word.lower()
        type = classifier.classify({'word': word})
        if type == 'pos':
            pos += 1
        elif type == 'neg':
            neg += 1

    # print result and write to appropriate file
    type = 'positive' if pos > neg else 'negative'
    outfile = 'relevant.txt' if pos > neg else 'noise.txt'
    print("{0}\t{1}".format(filename, type))
    with open(outfile, 'a') as myfile:
        myfile.write(filename)
