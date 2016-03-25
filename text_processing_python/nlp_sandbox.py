import os
import sys
import operator
import re
import string

# To do's:
	# ignore case
	# most common first word in sentence

class File:
	path = "";
	uniqueWords = {};
	mostCommonWord = "";
	biGrams = [];
	triGrams = [];
	quadGrams = [];
	content = "";
	averageWordLength = 0;
	contentNoPunctuation = "";
	mostCommonFirstWord = 0;
	
	def __init__(self, path):
		self.path = path;
		self.content = self.getContent();
		self.contentNoPunctuation = self.getContentNoPunctuation();
		self.uniqueWords = self.getUniqueWords();
		self.mostCommonWord = self.getMostCommonWord();
		self.biGrams = self.getNGrams(2);
		self.triGrams = self.getNGrams(3);
		self.quadGrams = self.getNGrams(4);
		self.averageSentenceLength = self.getAverageSentenceLength();# 
		self.averageWordLength = self.getAverageWordLength();
		self.contentNoPunctuation = self.getContentNoPunctuation();
		self.mostCommonFirstWord = self.getMostCommonFirstWord();
		self.wordFrequency = self.getWordsWithFrequency(10);
	def printFields(self):
		# print "FILE:"
		# print "\tContent:", self.content;
		print "\nWord Count:", self.uniqueWords;
		print "\nMost Common Word:", self.mostCommonWord;
		# print "\nBi-grams:", self.biGrams;
		# print "\nTri-grams:", self.triGrams;
		# print "\nQuad-grams:", self.quadGrams;
		print "\nAverage Word Length:", self.averageWordLength, " letters";
		print "\nAverage Sentence Length: ", self.averageSentenceLength;
		# print "\nFILE no punctuation", self.contentNoPunctuation;
		print "\nMost Common First Word: ", self.mostCommonFirstWord;
		print "\nWords with frequency 10+: ", self.wordFrequency;

	# return entire file
	def getContent(self):
		content = open(self.path, "r").read();
		return content;
		
	# return average sentence length
	def getAverageSentenceLength(self):
		#i don't think counting words this way will work unless you do it on the no punctuation file
		#since documents like the constitutition have weird punctuation attached to words
		# numWords = len(self.content.split(" ")); 
		numWords = len(self.contentNoPunctuation.split(" "));
		numPeriods = self.content.count(".");
		averageSentenceLength = numWords/numPeriods;
		return averageSentenceLength;

	# return entire file without the punctuation
	def getContentNoPunctuation(self):
		f = open(self.path,"r");
		contentNoPunctuation = "";
		for line in f:
			contentNoPunctuation = contentNoPunctuation + re.sub('\W', ' ', line);
		return contentNoPunctuation;

	# average word length of the file
	def getAverageWordLength(self):
		words = self.content.split(" ");
		totalLength = 0;
		for i in range(0, len(words)):
			totalLength = totalLength + len(words[i]);
		avgWordLength = totalLength/len(words);
		return avgWordLength;

	# create dictionary for words and their number of occurences (need to consider case here...)
	def getUniqueWords(self):
		uniqueWords = {};
		content2 = self.contentNoPunctuation.lower();
		words = content2.split(" ");
		for i in range(0, len(words)):
			if words[i] in uniqueWords and words[i] != '':
				uniqueWords[words[i]] = uniqueWords[words[i]] + 1;
			else:
				uniqueWords[words[i]] = 1;
		return uniqueWords;

	# most common word overall
	def getMostCommonWord(self):
		mostCommonWord = max(self.uniqueWords.iteritems(), key = operator.itemgetter(1))[0];
		return mostCommonWord;

	# n-grams as specified by argument passed
	def getNGrams(self, n):
		j = 0;
		nGrams = [];
		for i in range(j, len(self.content)):
			# print self.content[i : (i + n)];
			nGrams.append(self.content[i : (i + n)]);
			j = j + 1;
		return nGrams;

	def getMostCommonFirstWord(self):
		firstWords = {};
		content2 = re.sub('[\n]', ' ', self.content, flags = re.MULTILINE);
		content2 = re.sub("\s\s+", " ", content2);
		content2 = re.sub('^.\w|,|:|;', ' ', content2);
		content2 = re.sub('[--]', ' ', content2);
		words = content2.split(" ");
		for i in range(0,len(words)):
			str = re.match('\w+.', words[i], re.IGNORECASE);
			if str and i+1 != len(words) and words[i+1] != '':
				if firstWords.has_key(words[i+1]):
					firstWords.update({words[i+1]:firstWords[words[i+1]] + 1});
				else:
					firstWords.update({words[i+1]:1});
		mostCommonFirsWord = max(firstWords.iterkeys(),key=lambda k: firstWords[k]);
		return mostCommonFirsWord;

	def getWordsWithFrequency(self, frequency):
		wordFreq = {};
		for key, value in self.uniqueWords.iteritems():
			if value >= frequency:
				wordFreq.update({key:value});

file = File("AFarewellToArms.txt");
file.printFields();