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

stopset = []
with open('../ref/english.stop') as f:
    mit = f.read().split('\n')
    stopset = set(nltk.corpus.stopwords.words('english') + mit)

uselesswords = []
with open('../ref/chinafiltwords.txt') as f:
    raw = f.read()
    uselesswords = [line.strip() for line in f.read().split('\n')]

# treat each line as "# filename.txt"
for line in sys.stdin:
    # read file and classify
    num, filename = line.split('\t')
    file = open(filename.strip())
    raw = file.read()
    file.close()
    raw = raw.decode('utf8', 'replace')
    tokens = nltk.word_tokenize(raw)
    tokens = [word.encode('utf8').lower() for word in tokens]

    # filter out unclassifiable words

    tokens = [w for w in tokens if not w in stopset and not w.isdigit() and w.isalpha()
            and not w in uselesswords]
    fdist = nltk.FreqDist(tokens)
    
    features = {}
    for item in fdist.most_common(40):
        word = item[0]
        count = item[1]
        features[word] = count
        
    type = classifier.classify(features)

    # print result and write to appropriate file
    outfile = 'relevant.txt' if type == 'pos' else 'noise.txt'
    type_name = 'positive' if type == 'pos' else 'negative'
    print("{0}\t{1}".format(filename, type_name))
    with open(outfile, 'a') as myfile:
        myfile.write(filename)
