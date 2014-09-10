from __future__ import division
import nltk
from nltk import *
import sys
import glob
import os
from nltk.corpus import stopwords
import matplotlib.pyplot as plt

# Usage: python U1_David.py directory_path (Ex: /Users/davidkeimig/Desktop/flood/China_Flood)

dir_path = str(sys.argv[1])
path = dir_path + "/*.txt"
list_txt = glob.glob(path)

def content_fraction(text):
	mit_stopwords = open("../ref/english.stop").read().split('\n')
	stopset = set(stopwords.words('english') + mit_stopwords)
	content = [w for w in text if w.lower() not in stopset]
	return len(content) / len(text)

def calculate_range15(fdist):
	total = 0;
	small = 0;
	freq_list = fdist.items()
	for item in freq_list:
		total = total + int(item[1])
		if int(item[0]) <= 15 and int(item[0]) >= 1:
			small = small + int(item[1])
	return small / total

def search_top20Flood(text):
	flood_words = open("../ref/yourwords").read().split('\n')
	flood_set = set(flood_words)
	found = [w for w in text if w.lower() in flood_set]
	fdist1 = FreqDist(found)
	print "\nTOP 20 FLOOD WORDS FREQ"
	for item in fdist1.items():
		print("{word:<15} {count}".format(word=item[0],count=item[1]))
	return

def calc_average_words(tokens):
	return float(sum(map(len, tokens))) / len(tokens)

def calc_average_words_lines(toks):
	sent_tokenizer = nltk.data.load('nltk:tokenizers/punkt/english.pickle')
	text = corpus.gutenberg.raw(path)
	sents = sent.sent_tokenizer.tokenize(text)
	print sents

print path;

mit_stopwords = open("../ref/english.stop").read().split('\n')

all_toks = list()

for txt in list_txt:
	file_y = open(txt).read()
	tokens = word_tokenize(file_y)
	all_toks = all_toks + tokens

stopset = set(stopwords.words('english') + mit_stopwords)

new_toks = list()
rxstem = stem.RegexpStemmer('er$|a$|as$|az$')

#for tok in all_toks:
	#new_toks.append(rxstem.stem(tok))
all_text = Text(all_toks)
content = content_fraction(all_text)
print "\nCONTENT FRACTION\n"
print content
good_toks = [w.lower() for w in all_toks if not w.lower() in stopset and not w.isdigit() and w.isalpha() and len(w) >= 4]
text = Text(good_toks)
print "\nCOLLOCATIONS\n"
text.collocations()
bigram_measures = collocations.BigramAssocMeasures()
finder = BigramCollocationFinder.from_words(good_toks)
finder.apply_freq_filter(3)
scores = finder.score_ngrams(bigram_measures.raw_freq)
count = finder.ngram_fd.items()

print "\nCOUNT VALUES\n"
print count[:10]
print "\nRANK VALUES\n"
print scores[:10]
print "\n"

trigram_measures = collocations.TrigramAssocMeasures()
finder_tri = TrigramCollocationFinder.from_words(good_toks)
finder_tri.apply_freq_filter(3)
count_tri = finder_tri.ngram_fd.items()

print_values = count_tri[:10]

print "\nTRI VALUES\n"
print count_tri[:10]
print "\n"

for tri in print_values:
	data = tri[0]
	data_count = tri[1]
	combo = ' '.join(data)
	print "{0:<30} {1}".format(combo, data_count)


names = []
counter = []
value = 0
number_names = []
for elem in count:
	number_names.append(int(value))
	value = value + 1
	name = elem[0]
	count = elem[1]
	string = '\n'.join(name)
	names.append(str(string))
	counter.append(int(count))

number_names = number_names[:10]
names = names[:10]
counter = counter[:10]

plt.bar(number_names, counter, align='center')
plt.xticks(number_names, names)
plt.show()

fdist1 = FreqDist(text)

lengths = FreqDist([len(w) for w in text])

num_1_15 = calculate_range15(lengths)
print "\nPERCENT OF WORDS 1-15\n"
print num_1_15
print "\n"
array = fdist1.items()

search_top20Flood(text)

print("\nTop 20 Words")
for word in array[:20]:
    print("{word:<15} {count}".format(word=word[0],count=word[1]))

print("\nAVERAGE NUMBER OF LETTERS IN WORDS\n")
num = calc_average_words(good_toks)
print num

print("\nAVERAGE NUMBER OF WORDS PER LINE\n")
calc_average_words_lines(good_toks)

fdist1.plot(50, cumulative=True)

