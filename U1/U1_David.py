import nltk
import sys
import glob
import os

dir_path = str(sys.argv[1])
path = dir_path + "/*.txt"
list_txt = glob.glob(path)
print path;

for txt in list_txt:

	file_y = open(txt).read()
	tokens = nltk.word_tokenize(file_y)
	fdist1 = nltk.FreqDist(tokens)
	file_name = os.path.basename(txt)

	fdist1.plot(50, cumulative=True)

	items = fdist1.items();
	file_items_name = file_name + "_items.txt"

	file_x = open(file_items_name, 'w')

	for item in items:
		file_x.write(str(item[0]) + '\t\t' + str(item[1]) + '\n')


