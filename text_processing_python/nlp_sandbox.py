import os
import sys
import operator

# To do's:
	# strip punctuation (i'll work on this with regexp)
	# ignore case
	# most common first word in sentence

# probably want a File object for each file being tested and categorized
class File:
	path = "";
	uniqueWords = {};
	mostCommonWord = "";
	biGrams = [];
	triGrams = [];
	quadGrams = [];
	content = "";
	averageWordLength = 0;

	def __init__(self, path):
		self.path = path;
		self.content = self.getContent();
		self.uniqueWords = self.getUniqueWords();
		self.mostCommonWord = self.getMostCommonWord();
		self.biGrams = self.getNGrams(2);
		self.triGrams = self.getNGrams(3);
		self.quadGrams = self.getNGrams(4);
		self.averageWordLength = self.getAverageWordLength();

	def printFields(self):
		print "FILE:"
		# print "\tContent:", self.content;
		print "\tWord Count:", self.uniqueWords;
		print "\tMost Common Word:", self.mostCommonWord;
		print "\tBi-grams:", self.biGrams;
		print "\tTri-grams:", self.triGrams;
		print "\tQuad-grams:", self.quadGrams;
		print "\tAvg Word Length:", self.averageWordLength, " letters";

	# return entire file
	def getContent(self):
		content = open(self.path, "r").read();
		return content;
		
	# average word length of the file
	def getAverageWordLength(self):
		words = self.content.split(" ");
		totalLength = 0;
		for i in range(0, len(words)):
			totalLength = totalLength + len(words[i])
		avg = totalLength/len(words)
		return avg

	# create dictionary for words and their number of occurences (need to consider case here...)
	def getUniqueWords(self):
		uniqueWords = {};
		words = self.content.split(" ");
		for i in range(0, len(words)):
			if words[i] in uniqueWords:
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

file = File("testFile.txt");
file.printFields();