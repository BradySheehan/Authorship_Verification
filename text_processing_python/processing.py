import os
import sys
import operator
import re
import string

class Author:
	def __init__(self, name):
		self.name = name;
		self.works = [];
		
	def getNoStopWords(self, work):
		return "";
		
	def getNoPunctuation(self, work):
		return "";
		
class Features:
	def __init__(self, work, authorIndex):
		self.work = work;
		self.authorIndex = authorIndex;
		self.avgWordLength = self.getAvgWordLength();
		self.avgSenLength = self.getAvgSenLength();
		self.wordLengthPercentages = self.getWordLengthPercentages();
		self.senLengthPercentages = self.getSenLengthPercentages();
		self.featureVector = self.createFeatureVector();
		
	# get the average word length of this work
	def getAvgWordLength(self):
		return 0.0;
		
	# calculate the average sentence length of this wrk
	def getAvgSenLength(self):
		return 0.0;
		
	# create a vector of percentage for each word length 'n' in [0-10,11+]
	def getWordLengthPercentages(self):
		return 0.0;
		
	# create a vector of sentence length percentages for each sentence length in [?]
	def getSenLengthPercentages(self):
		return 0.0;
	
	# concatenate all of the above features into a numerical vector
	# this will need to be changes because the last two fields will be vectors
	def createFeatureVector(self):
		vector = [];
		vector.append(self.avgWordLength);
		vector.append(self.avgSenLength);
		vector.append(self.wordLengthPercentages);
		vector.append(self.senLengthPercentages);
		return vector;

authors = [];
# names = ['Bronte','Collins','Dickens','Ibsen','James','Jewett','Meredith','Phillips','Shaw','Thackeray','Trollope','Wharton'];
names = ['A','B']; # temp for now

# create an Author object for each author
for name in range(0, len(names)):
	authors.append(Author(names[name]));
	
# populate the Author's work list, then calculate a feature vector for each work
for author in range(0, len(authors)):
	authors[author].works = os.listdir("../authors/" + names[author]);
	print authors[author].works;
	thisAuthorsWorks = authors[author].works;
	for work in range(0, len(thisAuthorsWorks)): # for each work by this Author, calculate the features
		features = Features(thisAuthorsWorks[work], author);
		vector = features.createFeatureVector();
		for feature in range(0, len(vector)):
			print vector[feature],
		print;
		
		
		
		
		
		
		
		
		
		
		
		
		
		