import os
import sys
import operator
import re
import string

#This code was written and tested with version 2.7.* of Python by Brady Sheehan
#and Matthew Sobocinski.

#Class creates objects for each author in the directory structure
class Corpus:
	def __init__(self):
		self.authors = [];
		self.authornames = [];
		self.initializeAuthors();

	def initializeAuthors(self):
		self.authornames = self.getAllFiles("authors/");
		for name in self.authornames:
			a = Author(name);
			a.works = self.getAllFiles("authors/"+name);
			self.authors.append(a);

	#returns files/folders in directory ignoring system files
	def getAllFiles(self, pathName):
		directory = [];
		for item in os.listdir(pathName):
			if not item.startswith('.'):
				directory.append(item);
		return directory;

	def printAuthorsAndWorks(self):
		for author in self.authors:
			print "Author: " + author.name;
			for i in range(0, len(author.works)):
				print "\tWork " + str(i) + ":  " + author.works[i];

	def generateInputPairs(self):
		#take the cartesian product of all of the works by an author with every other
		#work by every other author
		#and create an InputPair for each element of the cartesian product
		#write this output to a file and write the answer to a file as well
		return "";

	def writeInputPairsToFile(self, listOfInputPairs):
		return "";

# note that the author class returns the works as a string and not as a list
class Author:
	def __init__(self, name):
		self.name = name;
		self.works = []; #strings referencing the work

	def getNoStopWords(self, workIndex):
		return "";

	#http://stackoverflow.com/questions/18429143/strip-punctuation-with-regex-python
	def getNoPunctuation(self, workIndex):
		return ' '.join(word.strip(string.punctuation) for word in self.getWork(workIndex).split());

	# get the work as a string with normalized white space
	def getWork(self, workIndex):
		return open(self.getPath(workIndex), "r").read();

	def getPath(self, workIndex):
		return "authors/"+self.name+"/"+self.works[workIndex];


class Features:
	def __init__(self, author, workIndex):
		self.author = author;
		self.workIndex = workIndex;
		self.work = self.author.getWork(workIndex);
		self.workNoPunctuation = self.author.getNoPunctuation(workIndex);
		self.wordCount = self.getWordCount(self.workNoPunctuation);
		self.sentenceCount = self.getSentenceCount(self.work);

	def getWordCount(self, line):
		return len(re.findall(r"\w+(?:-\w+)+|\w+", line));

	def getSentenceCount(self, line):
		return len(re.findall(r'[.!?]', line));

	# get the average word length of this work
	# (the sum of all the word lengths divided by the total number of words)
	def getAvgWordLength(self):
		# counts = [len(x) for x in self.workNoPunctuation.split()];
		# print "lencounts" + str(len(counts));
		# print "wordcounts" + str(self.wordCount);
		# return float(sum(counts))/len(counts);
		# ^^^ 2 line solution I haven't tested
		words = self.workNoPunctuation.split(" ");
		wordLengthsTotal = 0;
		for i in range(0, len(words)):
			wordLengthsTotal = wordLengthsTotal + len(words[i]);
		return float(wordLengthsTotal)/self.wordCount;

	# calculate the average number of words per sentence
	def getAvgSenLength(self):
		return float(self.wordCount)/self.sentenceCount;

	# create a vector of percentage for each word length 'n' in [0-10,11+]
		numSentences = len(re.findall(r'[!.?]', self.work));
		return float(self.wordCount)/numSentences;

	# create a vector of percentages for each word length 'n' in [0-10,11+]
	def getWordLengthPercentages(self):
		frequencies = 11 * [0];
		contentSplit = self.work.split();
		for i in range(0, len(contentSplit)):
			if len(contentSplit[i]) > 10:
				frequencies[10] = frequencies[10] + 1;
			else:
				frequencies[len(contentSplit[i])-1] = frequencies[len(contentSplit[i])-1] + 1;
		for i in range(0, len(frequencies)):
			frequencies[i] = float(frequencies[i]) / float(self.wordCount);
		return frequencies;


	# create a vector of sentence length percentages for each sentence length in 0-30, 30+
	def getSenLengthPercentages(self):
		# self.
		content = self.work.split(r'[!.?]');

		return 0.0;

	# concatenate all of the above features into a numerical vector
	# this will need to be changes because the last two fields will be vectors
	def getFeatureVector(self):
		vector = [];
		vector.append(self.getAvgWordLength());
		vector.append(self.getAvgSenLength());
		vector.append(self.getWordLengthPercentages());
		vector.append(self.getSenLengthPercentages());
		return vector;

	def printFeatures(self):
		print "Author: " + self.author.name + ", Work: " + self.author.works[self.workIndex];
		print "word count: " + str(self.wordCount);
		print "sentence count: " + str(self.sentenceCount);
		print "Average word length: " + str(self.getAvgWordLength());
		print "Average sent length: " + str(self.getAvgSenLength());
		print "word length percentages: " + str(self.getWordLengthPercentages()) + "\n";

# Each input pair is two sets of vectors (possibly a vector of vectors)
# that define one input that will be given to the neural network
class InputPair:
	def __init__(self, author1, workIndex1, author2, workIndex2):
		self.author1 = author1;
		self.author2 = author2;
		self.workIndex1 = workIndex1;
		self.workIndex2 = workIndex2;
		self.feature1 = "";
		self.feature2 = "";
		self.initializeFeatureVectors();

	def initializeFeatureVectors(self):
		self.feature1 = Features(self.author1, self.workIndex1);
		self.feature2 = Features(self.author2, self.workIndex2);

	def printFeatureVectors(self):
		print "Author1: " + self.author1.name;
		print "\tFeatures: " + self.feature1;
		print "\nAuthor2: " + self.author2.name;
		print "\tFeatures: " + self.feature1;

	def printPairs(self):
		self.feature1.printFeatures();
		self.feature2.printFeatures();

if __name__ == '__main__':
	a = Corpus();
	inputPair = InputPair(a.authors[1], 1, a.authors[2], 1);
	inputPair.printPairs();
