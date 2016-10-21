import operator

from nltk import word_tokenize
from nltk.corpus import stopwords

# This returns the word bag passed in as a list of (key, value) tuples
# Ex) [(key1, val1), (key2, val2),...]
def sortbyvalue(dict):
	return sorted(dict.items(), key=operator.itemgetter(1))

def wordTokenizer(text):
	return word_tokenize(text)

def normalizeWords(wordList):
	return [word.lower() for word in wordList]

def removeStopWords(wordList, language):
	return [word for word in wordList if word not in stopwords.words(language)]
	
def removePunctuation(wordList):
	punctuation = [
		',',
		',',
		'!',
		'.',
		')',
		':',
		';',
		'-',
		'--'
	]
	return [word for word in wordList if word not in punctuation]
	
def createOrUpdateWordBag(wordList, wordbag = {}):
	for word in wordList:
		if word in wordbag:
			wordbag[word] += 1
		wordbag.setdefault(word, 1)
	return wordbag
	
# Prints the top n words from the bag
def print_top_n(bag, n):
	sorted_bag_list = sortbyvalue(bag)
	numwords = len(sorted_bag_list)
	for i in range(n):
		print sorted_bag_list[numwords - i - 1]