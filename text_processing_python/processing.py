from __future__ import print_function
from random import randint
import os
import sys
import operator
import re
import string
import time

#This code was written and tested with version 2.7.* of Python by Brady Sheehan
#and Matthew Sobocinski.

#Class creates objects for each author in the directory structure
class Corpus:
	#note we can still treat this as an empty constructor by calling it and passing None
	#then checking if name is None or not and processing accordingly
	def __init__(self, directory=None):
		self.authors = [];
		self.authornames = [];
		self.initializeAuthors(directory);
		self.features = self.generateFeatures(); #dictionary

		# self.differentPairs = self.generateRandomInputPairs(name);
		# self.differentPairs = self.generateDifferentInputPairs();
		# self.samePairs = self.generateSameInputPairs();
	def initializeAuthors(self, directoryName):
		# if directoryName!=None:
			self.authornames = self.getAllFiles(str(directoryName)+"/");
			for name in self.authornames:
				a = Author(name, directoryName);
				a.works = self.getAllFiles(str(directoryName)+"/"+name);
				self.authors.append(a);
		# else:
		# 	self.authornames = self.getAllFiles("authors/");
		# 	for name in self.authornames:
		# 		a = Author(name, directoryName);
		# 		a.works = self.getAllFiles("authors/"+name);
		# 		self.authors.append(a);

	def generateFeatures(self):
		features = {};
		authorworks = [];
		for i in range(0, len(self.authors)):
			for j in range(0, len(self.authors[i].works)):
				authorworks.append(Features(self.authors[i], j));
			features.update({self.authors[i].name:authorworks});
		return features;

	#returns files/folders in directory ignoring system files
	def getAllFiles(self, pathName):
		directory = [];
		for item in os.listdir(pathName):
			if not item.startswith('.'):
				directory.append(item);
		return directory;

	# for testing purposes only
	def printAuthorsAndWorks(self):
		for author in self.authors:
			print("Author: " + author.name);
			for i in range(0, len(author.works)):
				print("\tWork " + str(i) + ":  " + author.works[i]);


	# This expects the name of an author and not the author object
	# Generates random pairs of works by different authors
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

	def generateRandomDifferentPairs2(self, numberToGenerate, filename): 
		f = open(filename, 'w+');
		print("Starting random pair generation");
		rand = [];
		generated = 0;
		while generated < numberToGenerate:
			randomAuthor1 = self.authors[randint(0, len(self.authors)-1)]; #pick a random author
			randomAuthor2 = self.authors[randint(0, len(self.authors) - 1)];
			if randomAuthor1.name != randomAuthor2.name:
				pair = InputPair(randomAuthor1, randint(0, len(randomAuthor1.works)-1), randomAuthor2, randint(0, len(randomAuthor2.works) - 1));
				rand.append(pair);
				print(pair.printPair(), file = f);
				generated+= 1;
		return rand;

	def generateRandomSamePairs(self, numberToGenerate, filename):
		f = open(filename, 'w+');
		print("Starting random same pair generation");
		rand = [];
		generated = 0;
		while generated < numberToGenerate:
			randomAuthor1 = self.authors[randint(0, len(self.authors)-1)]; #pick a random author
			work1 = randint(0, len(randomAuthor1.works)-1);
			work2 = randint(0, len(randomAuthor1.works)-1);
			if randomAuthor1.works[work1] != randomAuthor1.works[work2]:
				pair = InputPair(randomAuthor1, work1, randomAuthor1, work2);
				rand.append(pair);
				print(pair.printPair(), file = f);
				generated+= 1;
		return rand;

	# Generate all combinations of different authors and all combinations of the same author
	def generateDifferentInputPairs(self): 
		diff = [];
		for i in range(0, len(self.authors)): 
			for ii in range(0, len(self.authors[i].works)):
				for j in range(0, len(self.authors)):
				 	if self.authors[i].name != self.authors[j].name: 
						for jj in range(0, len(self.authors[j].works)):
							# print "1 - " + str(self.authors[i].printAuthorAndWork(ii)) + "\t 2 - " + str(self.authors[j].printAuthorAndWork(jj));
							diff.append(InputPair(self.authors[i], ii, self.authors[j], jj));
		return diff;

	# Generate pairs of works by the same author
	def generateSameInputPairs(self):
		f = open("same_pair_names.txt", 'w+');
		same = [];
		for i in range(0, len(self.authors)):
			for j in range(0, len(self.authors[i].works)):
				for jj in range(0, len(self.authors[i].works)):
					if self.authors[i].works[j] != self.authors[i].works[jj]:
						pair = InputPair(self.authors[i], j, self.authors[i], jj);
						same.append(pair);
						print(pair.printPair(), file = f);
		return same;

	# Writes a given vector of InputPairs to a file for processing with matlab neural network
	def writeInputPairsToFile(self, pairs, filename):
		f = open(filename, 'w+');
		for i in range(0, len(pairs)):
			pair = pairs[i];
			featureList = self.features[pair.author1.name];
			featureList2 = self.features[pair.author2.name];
			print(featureList[pair.workIndex1].getFeatureVector() + "," + featureList2[pair.workIndex2].getFeatureVector(), file = f);
		return "";

	# Specify the number of ones or zeros to write and if its ones or zeros
	def writeOutputTargets(self, numpairs, filename, ones):
		f = open(filename, 'w+');
		if ones == "1":
			for i in range(0, numpairs):
				print("1", file=f);
		else:
			for i in range(0, numpairs):
				print("0", file=f);

	def printAllFeatures(self):
		for i in range(0, len(self.authors)):
			featureList = self.features[self.authors[i].name];
			for j in range(0, len(featureList)):
				featureList[j].printFeatures();

	def printPairs(self, listOfPairs):
		print("Printing Pairs");
		for i in range(0, len(listOfPairs)):
			print(str(i+1)+"a:");
			featureList1 = a.features[listOfPairs[i].author1.name];
			featureList1[listOfPairs[i].workIndex1].printFeatures();
			print(str(i+1)+"b:");
			featureList2 = a.features[listOfPairs[i].author2.name];
			featureList2[listOfPairs[i].workIndex2].printFeatures();

	def generateAllDiffPairs(self):
		print("generating all different pairs from corpus");
		inputPairList = [];
		f = open("diff_pair_names.txt", 'w+');
		for i in range(0, len(self.authors)):
			for ii in range(0, len(self.authors)):
				if i!=ii:
					featureList1 = self.features[self.authors[i].name];
					featureList2 = self.features[self.authors[ii].name];
					for j in range(0, len(self.authors[i].works)):
						for jj in range(0, len(self.authors[ii].works)):
							pair = InputPair(self.authors[i], j, self.authors[ii], jj);
							inputPairList.append(pair);
							print(pair.printPair(), file=f);
		return inputPairList;

# note that the author class returns the works as a string and not as a list
class Author:
	def __init__(self, name, path):
		self.name = name;
		self.works = []; #strings referencing the work
		self.path = path;
	def getNoStopWords(self, workIndex):
		return "";

	#http://stackoverflow.com/questions/18429143/strip-punctuation-with-regex-python
	def getNoPunctuation(self, workIndex):
		return ' '.join(word.strip(string.punctuation) for word in self.getWork(workIndex).split());

	# get the work as a string with normalized white space
	def getWork(self, workIndex):
		return open(self.getPath(workIndex), "r").read();

	def getPath(self, workIndex):
		return self.path + "/" +self.name+"/"+self.works[workIndex];

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
		self.senLengthPercentages = self.getSenLengthPercentages();
		self.wordLengthPercentages = self.getWordLengthPercentages();

	def getWordCount(self, line):
		return len(re.findall(r"\w+(?:-\w+)+|\w+", line));

	def getSentenceCount(self, line):
		return len(re.findall(r'[.!?]', line));

	# get the average word length of this work
	# (the sum of all the word lengths divided by the total number of words)
	def getAvgWordLength(self):
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
		frequencies = 50* [0];
		sentenceCount = float(len(re.findall(r'[.!?]', self.work)));
		for i in range(0, len(contentSplit)):
			wordCount = len(re.findall(r"\w+(?:-\w+)+|\w+", contentSplit[i]));
			if wordCount !=0:
				if wordCount > 50:
					frequencies[49] += 1;
				else:
					frequencies[wordCount-1] += 1;
			else:
				sentenceCount-= 1;
		for i in range(0, len(frequencies)):
			frequencies[i] = float(frequencies[i]) / sentenceCount;
		return frequencies;

	# concatenate all of the above features into a numerical vector (as a string)
	def getFeatureVector(self):
		features = "";
		features = features + str(self.wordLengthPercentages).rstrip(r"]").lstrip(r"[") + "," ;
		features = features + str(self.senLengthPercentages).rstrip(r"]").lstrip(r"[");
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

	def printPair(self):
		return "1 - " + str(self.author1.printAuthorAndWork(self.workIndex1)) + ", 2 - " + str(self.author2.printAuthorAndWork(self.workIndex2));
if __name__ == '__main__':


	# print("Starting");
	# a = Corpus();
	# print("Finished building corpus.");
	# listOfPairs1 = a.generateRandomDifferentPairs2(2);
	# listOfPairs2 = a.generateRandomSamePairs(2);
	# a.printPairs(listOfPairs1);
	# a.printPairs(listOfPairs2);


	# print("starting");
	# a = Corpus(None, "authors2");
	# print("Finished Building Corpus.");
	# a.printAuthorsAndWorks();
	# size = len(a.features);
	# print("number of lists of features:"+str(size));
	# size2 = len(a.authornames);
	# print("number of authornames: " + str(size2));
	# a.printAllFeatures();

	# inputpair = InputPair(a.authors[1], 1, a.authors[2], 1);

	# featureList1 = a.features[a.authors[1].name];
	# featureList2 = a.features[a.authors[2].name];

	# featureList1[1].printFeatures();
	# featureList2[1].printFeatures();
	#

	# a.writeInputPairsToFile(a.samePairs, "in.txt");
	# a.writeInputPairsToFile(a.differentPairs, "in2.txt");
	# a.writeOutputTargets(len(a.samePairs), "out.txt", 1);
	# a.writeOutputTargets(len(a.differentPairs), "out2.txt", 0);

	# diff = a.generateInputPairs();
	# for i in range(0, len(diff)):
	# 	diff[i].printPair();

	# t0 = time.time();
	# t1 = time.time();
	# duration = t1-t0;
	# print(duration);
	# 

	print("starting");
	a = Corpus('../data/corpus/ingroup');
	print("Finished Building Corpus.");

	listOfPairs = a.generateAllDiffPairs();
	a.writeInputPairsToFile(listOfPairs, "all_diff_pairs.txt");
	a.writeOutputTargets(len(listOfPairs), "out1.txt", "0");

	print("processing2");
	listOfPairs2 = a.generateSameInputPairs();
	a.writeInputPairsToFile(listOfPairs2, "all_same_pairs.txt");
	a.writeOutputTargets(len(listOfPairs2), "out2.txt", "1");