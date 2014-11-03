#!/usr/bin/env python

"""
Topicizer
"""


import gensim
from nltk.corpus import stopwords

import nltk

import sys
import glob

#Call the NLTK stop words list
stoplist = stopwords.words('english')
extra_stop = [ 
#                "../ref/chinafiltwords.txt",
                "../ref/english.stop"
             ]

for file in extra_stop:
    with open(file) as f:
        raw = f.read().strip()
        tokens = [word for word in nltk.word_tokenize(raw)]
        stoplist += tokens

documents = []

for filename in glob.glob(sys.argv[1] + "/*.txt"):
    # tokenize each file
    with open(filename) as f:
        raw = f.read().strip().decode('utf-8')
        tokens = [word.lower() for word in nltk.word_tokenize(raw) if word.lower() not in
            stoplist and word.lower().isalpha()]
        documents.append(tokens)

#Remove the stop words
texts = documents

#Build the dictionary and the corpus
dictionary = corpora.Dictionary(texts)
corpus = [dictionary.doc2bow(text) for text in texts]

#Define the LDA model and the number of topics.
notopics = 50
lda = models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=notopics)
print(lda[dictionary.doc2bow(texts[0])])

#Printing the topic with their probabilities
print "\n\n", notopics, "Topics with their corresponding probabilities\n"
for i in range(0, lda.num_topics):
    #print "Topic", i+1, ":", lda.print_topic(i)
    print "Topic", i+1, ":", " + ".join(word[1] for word in lda.show_topic(i))
