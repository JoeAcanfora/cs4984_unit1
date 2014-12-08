#!/usr/bin/env python
#* Partial solution to Unit 8 for ClassEvent
#* by Xuan Zhang and Tarek Kanan, Nov. 10, 2014
#* Teams are expected to learn from this, not to just use it.
#* A suitable solution for Unit 8 should be richer and tailored to YourSmall, YourBig.

from nltk.tokenize import sent_tokenize, word_tokenize
from nltk import *
import re, os, operator, nltk
from textutil import *
import sys
import numpy

from people import *
from pygeocoder import Geocoder


# The directory location for ClassEvent documents.
classEventDir = './China_test/'
if len(sys.argv) > 1:
    classEventDir = sys.argv[1]

# The set of stopwords.
stopwords = nltk.corpus.stopwords.words('english')

def main():

	'''
	A pattern that matches "in" OR "at" followed by a single word, two words, or one word + a comma one or two words.
	This is intended to match common location occurrences, like: "in Islip, New York", or "at Islip" 
	'''
	locationPatternString = "((in|at)\s([A-Z][a-zA-Z]{4,}|[A-Z][a-zA-Z]{2,}\s[A-Z][a-zA-Z]{3,}))|\s+[A-Z][a-zA-Z]{3,},\s[A-Z][a-zA-Z]{2,}\s[A-Z][a-zA-Z]{3,}"

	'''
	A pattern that matches phrases relating to the Islip flood's 'girth'. This matches occurrences of
	one word followed by the word "flood", as well as "___ area" or "area of ____", which also may
	describe a flood's girth.
	'''	
	girthPatternString = "(\d+.\d+\skilometers|\d+.\d+\smiles)"

	'''
	A pattern that matches possible causes (or 'source') of the event. Phrases matched are: 
	"affected by ____", "result of ____", "caused by _____", "by ____", or "heavy ____" (which is more specific
	to the Islip event)
	'''
	causePatternString = "(due\sto(\s[A-Za-z]{3,}){1,3}|result\sof(\s[A-Za-z]{3,}){1,3}|caused\sby(\s[A-Za-z]{3,}){1,3}|by\s([A-Za-z]{4,}){1,2})|heavy\s([A-Za-z]{3,})"

	'''
	A pattern that matches context describing possible 'waterways' affect by the event. Phrases matched include:
	"affected ____", "water from _____", and "overflow of _____".
	'''
	waterwaysPatternString = "((the|The)(\s[A-Za-z]{3,}){1,3}\s(River|river))|(affected(\s[A-Za-z]{3,}){1,3})|(water\sfrom(\s[A-Za-z]{3,}){1,3})|(overflow\sof(\s[A-Za-z]{3,}){1,3})"

	'''
	A pattern for 4-digit years
	'''
	yearPatternString = "\s\d{4}"
	
	'''
	A pattern for months
	'''
	monthPatternString = "(?:January|February|March|April|May|June|July|August|September|October|November|December)"

	'''
	A pattern string for total rainfall
	'''
	rainfallPatternString = "((\d+.\d+\smillimeters)|(\d+.\d+\smm))|(\d+.\d+\s(inches|inch))"

	'''
	Monetary Value
	'''
	moneyPatternString = "\d+.\d+\s(million|billion|trillion|thousand)\s(dollars|dollar)|US\s\d+\s(million|billion|trillion|thousand)"

	'''
	Number of people missing, injured, killed, relocated/affected
	'''
	regex_num = "((\d,?)+(\s+[a-z]illions?)?)"
	regex_5words = "(?:\s+([a-zA-Z]+\s+){0,5})"
	missingPatternString = regex_num + regex_5words + "(?:missing)"
	injuredPatternString = regex_num + regex_5words + "(?:injured|harmed)"
	killedPatternString = regex_num + regex_5words + "(killed|dea(d|ths)|bod(y|ies)|casualt(ies|y)|fatalit(ies|y))"
	relocatedPatternString = regex_num + regex_5words + "(?:evacuate|affect(ed|s)?|relocated?)"

	# Compilation of regex patterns to improve repeated query efficiency.
	locationPattern = re.compile(locationPatternString)
	girthPattern = re.compile(girthPatternString)
	causePattern = re.compile(causePatternString)
	waterwaysPattern = re.compile(waterwaysPatternString)
	yearPattern = re.compile(yearPatternString)
	monthPattern = re.compile(monthPatternString)
	rainfallPattern = re.compile(rainfallPatternString)
	moneyString = re.compile(moneyPatternString)
	missingPattern = re.compile(missingPatternString, flags=re.IGNORECASE)
	injuredPattern = re.compile(injuredPatternString, flags=re.IGNORECASE)
	killedPattern = re.compile(killedPatternString, flags=re.IGNORECASE)
	relocatedPattern = re.compile(relocatedPatternString, flags=re.IGNORECASE)



	# A list of all files in the Class Event Directory
	listOfFiles = os.listdir(classEventDir)

	# A Dictionary to store a word and it's associated type as a tuple for the key, and the associated frequency
	# for the value.
	D = dict()

	# Loop through all of the files in the Class Event directory.
	for fileName in listOfFiles:

		# Ignores any non .txt files
		if not fileName.endswith('.txt'):
			continue

		# Stores the file's absolute path
		filePath = os.path.join(classEventDir, fileName)

		# Reads the file contents and tokenizes by sentence.
		fileContents = open(filePath.strip(), 'r').read()
		#Remove non-English words
		words = fileContents.split()
		fileContents = ""
		for w in words:
			if is_ascii(w):
				fileContents = fileContents + " " + w
		fileSentences = sent_tokenize(fileContents)
				
		# Calls the searchMatches function to 
		searchMatches(D, locationPattern, fileSentences, fileName, "location")
		searchMatches(D, girthPattern, fileSentences, fileName, "girth")
		searchMatches(D, causePattern, fileSentences, fileName, "cause")
		searchMatches(D, waterwaysPattern, fileSentences, fileName, "waterways")
		searchMatches(D, yearPattern, fileSentences, fileName, "year")
		searchMatches(D, monthPattern, fileSentences, fileName, "month")
		searchMatches(D, rainfallPattern, fileSentences, fileName, "totalRain")
		searchMatches(D, moneyString, fileSentences, fileName, "money")
		searchMatches(D, killedPattern, fileSentences, fileName, "killed")

		missingResults = []
		killedResults = []
		injuredResults = []
		relocatedResults = []
		for sentence in fileSentences:

			missingResults += [toInt(i) for i in find_missing(sentence)]
			injuredResults += [toInt(i) for i in find_injured(sentence)]
			relocatedResults += [toInt(i) for i in find_relocated(sentence)]
			killedResults += [toInt(i) for i in find_killed(sentence)]


		searchMatches(D, missingPattern, fileSentences, fileName, "missing")
		searchMatches(D, injuredPattern, fileSentences, fileName, "injured")
		searchMatches(D, relocatedPattern, fileSentences, fileName, "relocated")

	print

	'''
	The following code is used to filter words by their Parts of Speech (POS) tag. This is useful because, for example,
	we can ignore any "location" data that is not a noun, as we know that a verb would not be useful in describing a location.
	However, the reason that is not used is because when tagging words individually with POS, we lose context.
	So if we were to tag the phrase "between 5 and 8", which describes the time of, we would tag each word individually, and lose
	the context.

	# Each element in the list is of the form: [Attribute Type, List of Words, POS Tag]
	listOfResults = []

	# Stores the result of listOfResults AFTER filtering unneeded parts of speech.
	refinedListOfResults = []

	waterwaysList = []
	causeList = []
	timeList = []
	locationList = []
	girthList = []

	# From the frequency dictionary, grab the attribute type and word, split the word (which could be several words
	# long, like "between 5 and 8") into words, and append a list containing [Attribute Type, List of Words, POS Tag]
	for typeAndWordTuple, freq in D.iteritems():
		typeOfInfo, word = typeAndWordTuple
		word = word_tokenize(word)
		listOfResults.append([typeOfInfo, word, nltk.pos_tag(word)])
		if (typeOfInfo == "time"):
			timeList.append(word[1:])

	# Sorts list of results by the Attribute Type
	listOfResults = sorted(listOfResults)


	# Creates a dictionary storing the Parts of Speech that are valuable for each specific attribute.
	typeOfInfoPOS = {}
	typeOfInfoPOS["location"] = {"NNP"}
	typeOfInfoPOS["girth"] = {"NN", "JJ"}
	typeOfInfoPOS["cause"] = {"NN", "JJ"}
	typeOfInfoPOS["waterways"] = {"NN"}


	for result in listOfResults:
		typeOfInfo = result[0]
		for resultTuple in result[2]:

			if typeOfInfoPOS.has_key(typeOfInfo) and resultTuple[1] in typeOfInfoPOS[typeOfInfo]:

				refinedListOfResults.append([typeOfInfo, resultTuple])

	print 

	for result in refinedListOfResults:
		typeOfInfo = result[0]
		if typeOfInfo == "location":
			locationList.append(result[1][0])
		elif typeOfInfo == "waterways":
			waterwaysList.append(result[1][0])
		elif typeOfInfo == "cause":
			causeList.append(result[1][0])
		elif typeOfInfo == "girth":
			girthList.append(result[1][0])

	for typeAndWordTuple, freq in D.iteritems():
		typeOfInfo, word = typeAndWordTuple
		if (typeOfInfo == "time"):
			timeList.append(word)
		elif (typeOfInfo == "location"):
			locationList.append(word)
		elif (typeOfInfo == "girth"):
			girthList.append(word)
		elif (typeOfInfo == "cause"):
			causeList.append(word)
		elif (typeOfInfo == "waterways"):
			waterwaysList.append(word)
	'''

	# Creates a frequency dictionary for each attribute type
	locationFreqDict = dict()
	waterwaysFreqDict = dict()
	causeFreqDict = dict()
	girthFreqDict = dict()
	yearFreqDict = dict()
	monthFreqDict = dict()
	rainFreqDict = dict()
	moneyFreqDict = dict()
	killedFreqDict = dict()
	missingFreqDict = dict()
	injuredFreqDict = dict()
	relocatedFreqDict = dict()
	rain_convert = []


	# Loops through the original frequency dictionary, and adds the correspond word and frequency
	# to the dictionary for the appropriate attribute type.
	for typeAndWordTuple, freq in D.iteritems():
		typeOfInfo, result = typeAndWordTuple

		if (typeOfInfo == "location" and result not in stopwords):
			try:
				locationFreqDict[result] += freq
			except:
				locationFreqDict[result] = freq

		if (typeOfInfo == "waterways" and result not in stopwords):
			if re.match('(the|The).*(river|River)', result):
				result = result.lower()
				result = "affected " + result
			try:	
				waterwaysFreqDict[result] += freq
			except:
				waterwaysFreqDict[result] = freq

		if (typeOfInfo == "cause" and result not in stopwords):	
			words = nltk.word_tokenize(result)
			words = nltk.pos_tag(words)
			for w in words:
				if w[1] == "NN": 
					try:
						causeFreqDict[result] += freq
					except:
						causeFreqDict[result] = freq

		if (typeOfInfo == "girth" and result not in stopwords):
			try:
				girthFreqDict[result] += freq
			except:
				girthFreqDict[result] = freq
		if (typeOfInfo == "year" and result not in stopwords):	
			try:
				yearFreqDict[result] += freq
			except:
				yearFreqDict[result] = freq
		if (typeOfInfo == "month" and result not in stopwords):	
			try:
				monthFreqDict[result] += freq
			except:
				monthFreqDict[result] = freq
		if (typeOfInfo == "totalRain" and result not in stopwords):
			try:
				result = string.replace(result, "mm", "millimeters")
				result = string.replace(result, "inch\s", "inches")
				if "inches" in result:
					dec = re.findall('\d+.\d+', result)
					dec = 25.4 * float(dec[0])
					result = re.sub('\d+.\d+', str(dec), result)
				dec = re.findall('\d+.\d+', result)
				try:
					rainFreqDict[result] += freq
					rain_convert.append(float(dec[0]))
				except ValueError:
					continue
			except:
				try:
					rainFreqDict[result] = freq
					dec = re.findall('\d+.\d+', result)
					rain_convert.append(float(dec[0]))
				except ValueError:
					continue

		if (typeOfInfo == "money" and result not in stopwords):
			if "US" in result:
				answer = result.split()
				try:
					if answer[2] == "million":
						result = answer[1] + " million dollars" 
					elif answer[2] == "billion":
						result = answer[1] + " billion dollars"
					elif answer[2] == "thousand":
						result = answer[1] + " thousand dollars"
				except IndexError:
					continue
			try:
				moneyFreqDict[result] += freq
			except:
				moneyFreqDict[result] = freq

		if (typeOfInfo == "killed" and result not in stopwords):
			try:
				killedFreqDict[result] += freq
			except:
				killedFreqDict[result] = freq
		if (typeOfInfo == "missing" and result not in stopwords):
			try:
				missingFreqDict[result] += freq
			except:
				missingFreqDict[result] = freq
		if (typeOfInfo == "injured" and result not in stopwords):
			try:
				injuredFreqDict[result] += freq
			except:
				injuredFreqDict[result] = freq
		if (typeOfInfo == "relocated" and result not in stopwords):
			try:
				relocatedFreqDict[result] += freq
			except:
				relocatedFreqDict[result] = freq
	print 

	# Sorts all of the frequency dictionaries by their frequency values in reverse order, so the greatest
	# frequency is first.
	locationFreqDict = sorted(locationFreqDict.iteritems(), key=operator.itemgetter(1), reverse=True)
	waterwaysFreqDict = sorted(waterwaysFreqDict.iteritems(), key=operator.itemgetter(1), reverse=True)
	causeFreqDict = sorted(causeFreqDict.iteritems(), key=operator.itemgetter(1), reverse=True)
	girthFreqDict = sorted(girthFreqDict.iteritems(), key=operator.itemgetter(1), reverse=True)
	yearFreqDict = sorted(yearFreqDict.iteritems(), key=operator.itemgetter(1), reverse=True)
	monthFreqDict = sorted(monthFreqDict.iteritems(), key=operator.itemgetter(1), reverse=True)
	rainFreqDict = sorted(rainFreqDict.iteritems(), key=operator.itemgetter(1), reverse=True)
	moneyFreqDict = sorted(moneyFreqDict.iteritems(), key=operator.itemgetter(1), reverse=True)
	killedFreqDict = sorted(killedFreqDict.iteritems(), key=operator.itemgetter(1), reverse=True)
	missingFreqDict = sorted(missingFreqDict.iteritems(), key=operator.itemgetter(1), reverse=True)
	injuredFreqDict = sorted(injuredFreqDict.iteritems(), key=operator.itemgetter(1), reverse=True)
	relocatedFreqDict = sorted(relocatedFreqDict.iteritems(), key=operator.itemgetter(1), reverse=True)

	# Prints the top 10 words for each attribute.
	print "Top 10 frequent values for each attribute:"
	print "Location:", locationFreqDict [:50], "\n"
	print "Waterways:", waterwaysFreqDict [:10], "\n"
	print "Cause:", causeFreqDict [:10], "\n"
	print "Girth:", girthFreqDict [:10], "\n"
	print "Year:", yearFreqDict [:10], "\n"
	print "Month:", monthFreqDict [:10], "\n"
	print "Total Rainfall", rainFreqDict [:10], "\n"
	print "Money", moneyFreqDict [:10], "\n"
	print "Killed", killedFreqDict [:10], "\n"
	print "Missing", missingFreqDict [:10], "\n"
	print "Injured", injuredFreqDict [:10], "\n"
	print "Relocated", relocatedFreqDict [:10], "\n"

	# Prints the original template.
	print "Template before filling-out:"
	print "On {Time} a {Girth} caused by {Cause} {Waterways} in {Location}. Total Rainfall is {Total Rainfall}\n"
	# Prints the highest frequency result for each attribute in the formated template.
	print "Template after filling-out:"

	s_locations = locationFreqDict [:50]
	locations = []
	for x in s_locations:
		n = 0
		while n < x[1]:
			locations.append(x[0])
			n = n+1
	cities = []
	provinces = []
	states = []
	for place in locations:
		result_out = None
		try:
			result_out = Geocoder.geocode(place)
		except:
			pass
        # print(str(result[0]))
		rArray = str(result_out).split(',')
		rArray = [x.strip() for x in rArray]
        # print(rArray)
		if rArray.__len__() >= 3 :
			states.append(rArray[rArray.__len__() - 1])
			provinces.append(rArray[rArray.__len__() - 2])
			cities.append(rArray[rArray.__len__() - 3])
		elif rArray.__len__() == 2:
			states.append(rArray[1])
			provinces.append(rArray[0])
		else:
			states.append(rArray[0])

	fdistCities = FreqDist(cities)
	print(fdistCities.most_common(3))
	fdistProvinces = FreqDist(provinces)
	print(fdistProvinces.most_common(5))
	fdistState = FreqDist(states)
	print(fdistState.most_common(1))

	print "In {0} {1} a flood spanning {2} caused by {3} {4} in {5}. The total rainfall was {6} millimeters and the total cost of damages was {7}. Killed {8}, Missing {9}, Injured {10}, Affected {11}".format(monthFreqDict[0][0], yearFreqDict[0][0], girthFreqDict[0][0], causeFreqDict[0][0], waterwaysFreqDict[0][0], locationFreqDict[0][0], numpy.median(numpy.array(rain_convert)), moneyFreqDict[0][0], 
			numpy.percentile(killedResults, 75), numpy.percentile(missingResults, 75), numpy.percentile(injuredResults, 75), numpy.percentile(relocatedResults, 75))
	sys.stdout.write("The cities of")
	for x in fdistCities.most_common(3):
		sys.stdout.write(" ")
		sys.stdout.write(x[0])
	sys.stdout.write(" were affected the greatest")
	sys.stdout.write("while the provinces of")
	for y in fdistProvinces.most_common(3):
		sys.stdout.write(" ")
		sys.stdout.write(y[0])
	sys.stdout.write(" were affected the greatest")
	sys.stdout.write(".Finally nearly all of the floods damage occured in the state of ")
	for z in fdistState.most_common(1):
		sys.stdout.write(z[0])
		print "\n"


# Prints any matches in the files with their corresponding filename and location in the file.
# Also creates a frequency dictionary for words and their attributes.
def searchMatches(D, pattern, fileSentences, fileName, typeOfInfo):
	
	# Loop over all sentences in the file.
	for sentence in fileSentences:

		# Loop over all matches from the regex object.
		for match in pattern.finditer(sentence):

			# Splits the match into words
			result = match.group().split()

			# Filters any words of length 2 or less.
			result = [w for w in result if len(w) > 2 or w == "mm" or w == "US" or w.isdigit()]
			
			# Joins filtered set words with spaces
			result = " ".join(w for w in result)

			# Display the filename and location in the file at which a match was found. 
			#print "{4}: {0}: {1}-{2}: {3}".format(fileName, match.start(), match.end(), result, typeOfInfo)
			
			# Increment the frequency for this attribute and word pair
			try:
				D[typeOfInfo, result] += 1
			except:
				D[typeOfInfo, result] = 1

def toInt(words):
	try:
		return int(words)
	except:
		num, word = words.split()
		if "million" in words:
			return int(num) * 1000000

def getCoords(coords):

    xy = str(coords).split(",", 2)
    x = xy[0][1:]
    y = xy[1][:-1]
    result = [float(x), float(y)]
    return result

if __name__ == "__main__": main()
