#SCRIPT TO PLAY WITH ADDING NEW FEATURES FOR DETECTING RECIPES
#EVENTUALLY ADD THESE TO extract_book2.py

#import necessary libraries
from __future__ import print_function #need this to print to file
import xml.etree.ElementTree as ET #need for parsing XML file of book
import string #need for testing if punctuation in word
#import nltk
from nltk.stem.snowball import SnowballStemmer

stemmer=SnowballStemmer("english")
print(stemmer.stem("running"))

def numCookWords(page):
	with open('cookingWords.txt') as f:
		for line in f:
			line=line.strip() #strip newlines/blanks at beg/end of line
			if not line:
				continue #skip blank lines in file
			if line.startswith('#'):
				continue #skip comments in file
			cookWords=[line.rstrip('\n') for line in f]
		cWord=0 #counter for cooking words
		pg=page.findall(".//WORD")
		for tag in pg:
			word=tag.text
			if word.isalpha(): #test if word at least one char and all char alphabetic
				word=word.casefold() #change to all lowercase for easier comparison; casefold() is more stringent than lower() and accounts for letters in other lang
				origWord=word
				word=stemmer.stem(word)
				if word in cookWords:
					cWord+=1
					print(word,origWord) #test to see if working
		if len(pg)==0:
			return 0 #blank page, return 0
		else:
			return float(cWord)/len(pg)

tree=ET.parse('foodNewsletter.xml') #parse xml
pages=tree.findall(".//OBJECT") #store all the bk pages in list called 'pages'
for p in pages:
	numCookWords(p)

def numMeasureWords(page):
	with open('measurements.txt') as f:
		for line in f:
			line=line.strip()
			if not line:
				continue #skip blanks in file
			if line.startswith('#'):
				continue #skip comments in file
			measures=[line.rstrip('\n') for line in f]
		measureWord=0 #counter
		pg=page.findall(".//WORD")
		for tag in pg:
			word=tag.text
			if not word.isdigit():
				word=word.casefold()
				if word in measures:
					measureWord+=1
					#print(word) #testing
		if len(pg)==0:
			return 0 #blank page, return 0
		else:
			return float(measureWord)/len(pg)

def upperToTotalLetters(page):
	upperCase=0 #uppercase counter
	letter=0
	pg=page.findall(".//WORD")
	if len(pg)==0:
		return 0 #blank page, return 0
	else:
		for tag in pg:
			word=tag.text
			for c in word:
				if c.isalpha():
					letter+=1 #count all the letters on page
				if c.isupper():
					upperCase+=1 #count all uppercase char
		return float(upperCase)/float(letter)


def pgLocation(loc,book):
	return float(loc)/len(book)


tree=ET.parse('foodNewsletter.xml') #parse xml
pages=tree.findall(".//OBJECT") #store all the bk pages in list called 'pages'
count=0 
for p in pages:
	count+=1
	x = p.attrib['usemap'][:-5]
	pgLocation(count,pages)



#print(cookWords)

def parsePrint(xmlBk,f):
	tree=ET.parse(xmlBk) #parse xml
	pages=tree.findall(".//OBJECT") #store all the bk pages in list called 'pages' 
	for p in pages:
		x = p.attrib['usemap'][:-5]
		print(x+'\t'+str(numDigits(p))+'\t'+str(punct(p))+'\t'+str(scaledWords(p,pages)),file=f)

def numDigits(page):
	digPunc=0
	pg=page.findall(".//WORD")
	for tag in pg:
		word=tag.text
		
	if len(pg)==0: #DONT FORGET TO DEAL WITH BLANK PAGES!!
		return 0 #return 0 if have blank page