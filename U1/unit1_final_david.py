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

for txt in list_txt:
	file_y = open(txt).read()
	tokens = word_tokenize(file_y)
	all_toks = all_toks + tokens

stopset = set(stopwords.words('english'))

new_toks = list()
rxstem = stem.RegexpStemmer('er$|a$|as$|az$')

#for tok in all_toks:
	#new_toks.append(rxstem.stem(tok))

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
array = fdist1.items()

print("Top 20 Words")
for word in array[:20]:
    print("{word:<15} {count}".format(word=word[0],count=word[1]))

fdist1.plot(50, cumulative=True)
