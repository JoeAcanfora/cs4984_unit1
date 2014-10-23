#!/usr/bin/env python

""" 
Reducer

Uses a key in the form "num\tfilename" to 
and reads each file.
"""

import sys
import zipimport

try:
    importer = zipimport.zipimporter('nltk.mod')
    nltk = importer.load_module("nltk")
    nltk.data.path += ["./nltkData/"]
except zipimport.ZipImportError:
    import nltk

from cPickle import load

stopset = []
with open('../ref/english.stop') as f:
    mit = f.read().split('\n')
    stopset = set(nltk.corpus.stopwords.words('english') + mit)

# load tagger
tagger = nltk.tag.stanford.NERTagger(
        'stanford-ner/english.all.3class.distsim.crf.ser.gz',
        'stanford-ner/stanford-ner.jar'
        )

to_tag = []
# treat each line as "# filename.txt"
for line in sys.stdin:
    # read file 
    num, filename = line.split('\t')
    file = open(filename.strip())
    raw = file.read()
    file.close()
    raw = raw.decode('ascii', 'replace')

    # tokenize and eliminate useless words
    toks = nltk.word_tokenize(raw)
    toks = [w for w in toks if not w.lower() in stopset and not w.isdigit() and
            w.isalpha() and len(w) >= 4 and len(w) < 125]

    # take the most common words per file
    fdist = nltk.FreqDist(toks)
    most = [w[0] for w in fdist.most_common(10)]

    # for speed, we just add it to a list and tag all of them at once
    to_tag += most

# tag the most common words
ne_tagged = tagger.tag(to_tag)                            # NER tag
#pos_tagged = [nltk.tag.pos_tag(word) for word in most]  # POS tag

# print each word along with tag
for word, tag in ne_tagged:
    if tag != 'O':
        print(word + "\t" + tag)
