from __future__ import print_function #need this to print to file
import xml.etree.ElementTree as ET #need for parsing XML file of book
import string #need for testing if punctuation in word
from nltk.stem.snowball import SnowballStemmer #need to stem words for cookWords and measureWords features
stemmer=SnowballStemmer("english") #set up stemmer
import os
from os import listdir #need for reading all files from folder
import csv

#try this with foodNewsletter.xml




def ingPhraser(page):
	with open('measurements.txt') as f:
		for line in f:
			line=line.strip()
			if not line:
				continue #skip blanks in file
			if line.startswith('#'):
				continue #skip comments in file
			measures=[line.rstrip('\n') for line in f]
			with open('nyt-ingredients-snapshot-2015.csv') as csvfile:
				reader=csv.DictReader(csvfile)
				name=set([])
				for n in name:
					n.lower()
				for row in reader:
					name.add(row['name'])
				ingPhrase=0
				lines=p.findall(".//LINE")
				for l in lines:
					foodWord=False
					unitWord=False
					phrase=''
					size=0 #num of words in line
					words=l.findall(".//WORD")
					for tag in words:
						phrase+=tag.text+' '
						size+=1
						x=tag.text
						x.casefold()
						if x in name:
							if x.isalpha():
								if x not in measures:
									foodWord=True
						if x in measures:
							unitWord=True
					if foodWord and unitWord and (size<11):
						ingPhrase+=1
				return(ingPhrase) #prints # phrases per page

tree=ET.parse('foodNewsletter.xml') #parse xml
pages=tree.findall(".//OBJECT") #store all the bk pages in list called 'pages' 
with open('measurements.txt') as f:
	for line in f:
		line=line.strip()
		if not line:
			continue #skip blanks in file
		if line.startswith('#'):
			continue #skip comments in file
		measures=[line.rstrip('\n') for line in f]
with open('nyt-ingredients-snapshot-2015.csv') as csvfile:
	reader=csv.DictReader(csvfile)
	foods=set([])
	for row in reader:
		foods.add(row['name'])
	foods=[element.lower() for element in foods]
print(foods)
print(measures)
#for p in pages:
#	print(ingPhraser(p))
# want # of lines that have # then food name? 
# or proportion of 'ingredient phrases'/# lines on pg?? maybe try both?

#try something first: count # of lines with qty (use dict and measureWords.txt?) AND food word?