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
print path;

all_toks = list()
value = list()

for txt in list_txt:
	file_y = open(txt).read()
	tokens = word_tokenize(file_y)
	value = tokens;
	all_toks = all_toks + tokens

stopset = set(stopwords.words('english'))

good_toks = [w for w in all_toks if not w in stopset]
good_toks = [w for w in good_toks if not w.isdigit() and w.isalpha() and len(w) >= 3]
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

number_names = number_names[:15]
names = names[:15]
counter = counter[:15]

plt.bar(number_names, counter, align='center')
plt.xticks(number_names, names)
plt.show()

fdist1 = FreqDist(text)
fdist1.plot(50, cumulative=True)