from __future__ import print_function
import os
import sys
import operator
import re
import string
import time
from random import randint

#This code was written and tested with version 2.7.* of Python by Brady Sheehan
#and Matthew Sobocinski.

#Class creates objects for each author in the directory structure
class Corpus:
	def __init__(self, name):
		self.authors = [];
		self.authornames = [];
	 	self.initializeAuthors();
		# self.initializeOneAuthor(name);
		self.features = self.generateFeatures(); #dictionary
		self.differentPairs = self.generateRandomInputPairs(name);
		# self.differentPairs = self.generateDifferentInputPairs();
		self.samePairs = self.generateSameInputPairs();
		
	# def initializeOneAuthor(self, name):
		# a = Author(name);
		# a.works = self.getAllFiles("authors/" + name);
		# self.authors.append(a);

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
			print("Author: " + author.name);
			for i in range(0, len(author.works)):
				print("\tWork " + str(i) + ":  " + author.works[i]);
				
	
	def generateRandomInputPairs(self, authorOfInterest):
		rand = [];
		generated = 0;
		index = 0;
		for i in range(0, len(self.authors)):
			if(self.authors[i].name == authorOfInterest):
				index = i;
			
		numberToGenerate = len(self.authors[index].works);
		for i in range(0, numberToGenerate): # generate n random files
			while generated < numberToGenerate:
				randomAuthor = randint(0, len(self.authors)-1);
				if self.authors[randomAuthor].name != authorOfInterest:
					randomWork = randint(0, len(self.authors[randomAuthor].works));
					rand.append(InputPair(self.authors[index], i, self.authors[randomAuthor], randomWork));
					generated = generated + 1;
		return rand;					
						
					

	def generateDifferentInputPairs(self): #generate all combinations of different authors and all combinations of the same author
		diff = [];
		for i in range(0, len(self.authors)): # for each author
			for ii in range(0, len(self.authors[i].works)): # for each work by this author
				for j in range(0, len(self.authors)): # for each author
				 	if self.authors[i].name != self.authors[j].name: # if not the i'th author
						for jj in range(0, len(self.authors[j].works)): # generate features for each of their works
							# print "1 - " + str(self.authors[i].printAuthorAndWork(ii)) + "\t 2 - " + str(self.authors[j].printAuthorAndWork(jj));
							diff.append(InputPair(self.authors[i], ii, self.authors[j], jj));
		return diff;

	def generateSameInputPairs(self):
		same = [];
		for i in range(0, len(self.authors)):
			for j in range(0, len(self.authors[i].works)):
				for jj in range(0, len(self.authors[i].works)):
					if self.authors[i].works[j] != self.authors[i].works[jj]:
						# print "1 - " + str(self.authors[i].printAuthorAndWork(j)) + "\t 2 - " + str(self.authors[i].printAuthorAndWork(jj));
						same.append(InputPair(self.authors[i], j, self.authors[i], jj));
		return same;

	def generateFeatures(self):
		features = {};
		for i in range(0, len(self.authors)):
			authorworks = [];
			for j in range(0, len(self.authors[i].works)):
				authorworks.append(Features(self.authors[i], j));
			features.update({self.authors[i].name:authorworks});
		return features;

	#Writes a given vector of InputPairs to a file for processing with matlab neural network
	def writeInputPairsToFile(self, pairs, filename):
		f = open(filename, 'w+');
		for i in range(0, len(pairs)):
			pair = pairs[i];
			featureList = self.features[pair.author1.name];
			featureList2 = self.features[pair.author2.name];
			print(featureList[pair.workIndex1].getFeatureVector() + "," + featureList2[pair.workIndex2].getFeatureVector(), file = f);
		return "";

	#Specify the number of ones or zeros to write and if its ones or zeros
	def writeOutputTargets(self, numpairs, filename, ones):
		f = open(filename, 'w+');
		if ones == 1:
			for i in range(0, numpairs):
				print("1", file=f);
		else:
			for i in range(0, numpairs):
				print("0", file=f);		
		
	def printAllFeatures(self):
		for author, works in self.features.iteritems():
			for i in range(0, len(works)):
				works[i].printFeatures();

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

	def printAuthorAndWork(self, workIndex):
		return "Author: " + self.name + ", Work: " + self.works[workIndex];


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

	# create a vector of percentages for each word length 'n' in [1-10,11+]
	def getWordLengthPercentages(self):
		frequencies = 11 * [0];
		contentSplit = self.workNoPunctuation.split();
		for i in range(0, len(contentSplit)):
			if len(contentSplit[i]) > 10:
				frequencies[10] += 1;
			else:
				frequencies[len(contentSplit[i])-1] += 1;
		for i in range(0, len(frequencies)):
			frequencies[i] = float(frequencies[i]) / float(self.wordCount);
		return frequencies;

	# create a vector of sentence length percentages for each sentence length in 1-30, 30+
	def getSenLengthPercentages(self):
		contentSplit = filter(None, re.split(r'[!.?]', self.work));
		frequencies = 30 * [0];
		for i in range(0, len(contentSplit)):
			wordCount = len(re.findall(r"\w+(?:-\w+)+|\w+", contentSplit[i]));
			if wordCount > 30:
				frequencies[29] += 1;
			else:
				frequencies[wordCount-1] += 1;
		for i in range(0, len(frequencies)):
			frequencies[i] = float(frequencies[i]) / float(len(re.findall(r'[.!?]', self.work)));
		return frequencies;

			# create a vector of sentence length percentages for each sentence length in 1-30, 30+
	def getSenLengthPercentages2(self):
		contentSplit = filter(None, re.split(r'[!.?]', self.work));
		frequencies = 10 * [0];
		for i in range(0, len(contentSplit)):
			wordCount = len(re.findall(r"\w+(?:-\w+)+|\w+", contentSplit[i]));
			if wordCount > 30:
				frequencies[9] += 1;
			else:
				frequencies[(wordCount/3)+(wordCount%3)-1] += 1;
		for i in range(0, len(frequencies)):
			frequencies[i] = float(frequencies[i]) / float(len(re.findall(r'[.!?]', self.work)));
		return frequencies;

	# concatenate all of the above features into a numerical vector (as a string)
	def getFeatureVector(self):
		features = "";
		features = features + str(self.getWordLengthPercentages()).rstrip(r"]").lstrip(r"[") + "," ;
		features = features + str(self.getSenLengthPercentages()).rstrip(r"]").lstrip(r"[");
		return features;

	def printFeatures(self):
		print("Author: " + self.author.name + ", Work: " + self.author.works[self.workIndex]);
		print("word count: " + str(self.wordCount));
		print("sentence count: " + str(self.sentenceCount));
		print("Average word length: " + str(self.getAvgWordLength()));
		print("Average sent length: " + str(self.getAvgSenLength()));
		print("word length percentages: " + str(self.getWordLengthPercentages()));
		print("sen length percentages: " + str(self.getSenLengthPercentages()) + "\n");

# Pair together 2 sets of author objects and indices of their works
class InputPair:
	def __init__(self, author1, workIndex1, author2, workIndex2):
		self.author1 = author1;
		self.author2 = author2;
		self.workIndex1 = workIndex1;
		self.workIndex2 = workIndex2;

if __name__ == '__main__':

	a = Corpus("james");
	# inputpair = InputPair(a.authors[1], 1, a.authors[2], 1);

	# featureList1 = a.features[a.authors[1].name];
	# featureList2 = a.features[a.authors[2].name];

	# featureList1[1].printFeatures();
	# featureList2[1].printFeatures();
	# 
	a.writeInputPairsToFile(a.samePairs, "in.txt");
	a.writeInputPairsToFile(a.differentPairs, "in2.txt");
	a.writeOutputTargets(len(a.samePairs), "out.txt", 1);
	a.writeOutputTargets(len(a.differentPairs), "out2.txt", 0);

	# diff = a.generateInputPairs();
	# for i in range(0, len(diff)):
	# 	diff[i].printPair();

	# t0 = time.time();
	# t1 = time.time();
	# duration = t1-t0;
	# print(duration);







