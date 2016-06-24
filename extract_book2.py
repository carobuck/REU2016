#import necessary libraries
from __future__ import print_function #need this to print to file
import xml.etree.ElementTree as ET #need for parsing XML file of book
import string #need for testing if punctuation in word
from nltk.stem.snowball import SnowballStemmer #need to stem words for cookWords and measureWords features
stemmer=SnowballStemmer("english") #set up stemmer
import os
from os import listdir #need for reading all files from folder
import csv 

#function to parse a book and print its features to a file
#parameters: takes a XML book file; like in this form: 'foodNewsletter.xml'
#and takes file name; if file DNE, will make file of that name
#Will make new output file for each xml book (if give new output file name for each book)
def parsePrint(xmlBk,f,cookWords,measures,foods):
	with open(xmlBk, 'rb') as xml_bk:
		tree=ET.parse(xml_bk) #parse xml
		pages=tree.findall(".//OBJECT") #store all the bk pages in list called 'pages' 
		count=0 #count number of iterations of for loop
		avgP=avgPunc(pages)
		avgW=avgWord(pages)
		for p in pages:
			count+=1
			x = p.attrib['usemap'][:-5]  #get page name_# so can reference later
			features = [numDigits(p), 
				scaledPunc(p,avgP),
				scaledWords(p,avgW),
				numCookWords(p,cookWords),
				numMeasureWords(p,measures),
				upperToTotalLetters(p),
				moreThan10(p),
				pgLocation(count,pages),
				ingPhraser(p,foods,measures)
				]; 
			print(x+'\t'+'\t'.join([str(f) for f in features]),file=f)

			#print(x+'\t'+str(numDigits(p))+'\t'+str(scaledPunc(p,avgP))+'\t'+str(scaledWords(p,avgW))+'\t'+str(numCookWords(p,cookWords))+'\t'+str(numMeasureWords(p,measures))+'\t'+str(upperToTotalLetters(p))+'\t'+str(moreThan10(p))+'\t'+str(pgLocation(count,pages))+'\t'+str(ingPhraser(p,foods,measures)),file=f)
			#print(x+'\t'+str(numDigits(p))+'\t'+str(punct(p))+'\t'+str(numCookWords(p))+'\t'+str(numMeasureWords(p))+'\t'+str(pgLocation(count,pages))+'\t'+str(upperToTotalLetters(p)),file=f)
			#print(x+'\t'+str(punct(p))+'\t'+str(scaledWords(p,pages))+'\t'+str(numCookWords(p))+'\t'+str(numMeasureWords(p))+'\t'+str(pgLocation(count,pages))+'\t'+str(upperToTotalLetters(p)),file=f)

#counts # of digits and digits with punctuation
def numDigits(page):
	digPunc=0
	pg=page.findall(".//WORD")
	if len(pg)==0:
		return 0 #return 0 if have blank page
	else:
		for tag in pg:
			word=tag.text
			num=False
			punc=False
			if word.isdigit():
				#print word
				digPunc+=1
			else:
				for c in word:
					if c in string.punctuation:
						punc=True
					if c.isdigit():
						num=True
				if punc and num:
					digPunc+=1
					#print word
		return float(digPunc)/len(pg) #return proportion of # digits to # words on pg

#returns proportion of punctuation to words on a single page
def punct(page):
	punc=0
	pg=page.findall(".//WORD")
	if len(pg)==0:
		return 0 
	else:
		for i in range(len(pg)):
			for c in pg[i].text:
				if c in string.punctuation:
					punc+=1
		return float(punc)/len(pg)

#returns average proportion of punctuation to words on page for whole book
def avgPunc(book):
	sumPunc=0
	for p in book:
		sumPunc+=punct(p)
	return float(sumPunc)/len(book)

#returns scaled proportion of punct to words (scaled to average punctuation for whole book)
def scaledPunc(page,avg):
	thisPg=punct(page)
	return(thisPg-avg)/avg

#returns # of words on a page
#used in scaledWords (actual feature function)
def numWords(page):
	pg=page.findall(".//WORD")
	return len(pg)

#returns average # of words per page
#used in scaledWords (actual feature function)
def avgWord(book):
	Sum=0
	for p in book:
		Sum+=numWords(p)
	return float(Sum)/len(book)

#returns scaled # of words on page (-1 indicate blank page; closer to 0 indicate closer to average # of words on page)
def scaledWords(page,avg):
	thisPg=numWords(page)
	return (thisPg-avg)/avg

#function to count proportion of cooking words on a page
def numCookWords(page,cookWords):
	pg=page.findall(".//WORD")
	if len(pg)==0:
			return 0 #blank page, return 0
	else:
		cWord=0 #counter for cooking words
		for tag in pg:
			word=tag.text
			if word.isalpha(): #test if word at least one char and all char alphabetic
				word=word.casefold() #change to all lowercase for easier comparison; casefold() is more stringent than lower() and accounts for letters in other lang
				word=stemmer.stem(word)
				if word in cookWords:
					cWord+=1
					#print(word) #test to see if working
		return float(cWord)/len(pg)

#function to count proportion of measurement words on a page 
def numMeasureWords(page,measures):
	pg=page.findall(".//WORD")
	if len(pg)==0:
		return 0 #blank page, return 0
	else:
		measureWord=0 #counter
		for tag in pg:
			word=tag.text
			if not word.isdigit():
				word=word.casefold()
				word=stemmer.stem(word)
				if word in measures:
					measureWord+=1
					#print(word) #testing
		return float(measureWord)/len(pg)

#calculates where page is in relation to whole book; ranges (0,1] (in theory, if closer to 0 or 1, is less likely to be recipe)
def pgLocation(loc,book):
	return float(loc)/len(book)

#function to count proportion of uppercase letters to total number of letters on the page
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
				#if c.isalpha(): #COMMENT OUT TO COUNT ALL CHAR
				letter+=1 #count all the letters on page MAYBE CHANGE LATER TO COUNT ALL CHAR (incl digits/punc??)
				if c.isupper():
					upperCase+=1 #count all uppercase char
		if letter==0: #if no letters on page
			return 0
		else:
			return float(upperCase)/float(letter)

#this function returns true (1) if there are at least 10 alphabetical words on a page, false (0) otherwise
def moreThan10(page):
	pg=page.findall(".//WORD")
	if len(pg)==0: 
		return 0 #blank page, return 0
	else:
		alphaWord=0
		for tag in pg:
			word=tag.text
			if word.isalpha():
				alphaWord+=1
		if alphaWord>10:
			return 1
		else:
			return 0	

#returns # of 'ingredient phrases' on a page (# of lines that have both a food word and a measure word)
#IS NOT PERFECT; TRY TO IMPROVE?? pulls up some directions, and misses some b/c ingredients not in set that I compare to
def ingPhraser(page,foods,measures):
	ingPhrase=0
	lines=page.findall(".//LINE")
	if len(lines)==0: #deal with blank page
		return 0
	for l in lines:
		foodWord=False
		unitWord=False
		#phrase=''
		words=l.findall(".//WORD")
		size = len(words)
		if size>=11:
			continue
		for tag in words:
			#phrase+=tag.text+' '
			x=tag.text
			x.casefold()
			if not foodWord and x in foods:
				if x.isalpha():
					if x not in measures:
						foodWord=True
			if not unitWord and x in measures:
				unitWord=True
		if foodWord and unitWord: #(10 or fewer words on a line)
			ingPhrase+=1
	return float(ingPhrase)/len(lines) #return proportion of ingPhrases/#lines on pg...
	#^^^not perf; may bias towards recipes with fewer or more ingredients???


#for each line in book, want to print:
# (bkname_page#	numDigits	punctuation	numWords )

#OPEN ONE OUTPUT FILE FOR HOWEVER MANY BOOKS TO RUN THRU
f=open('extract_train_data4','w')
#FOR EACH BOOK, SEND XML AND f (FILE STREAM) and 3 other files

#open 3 other files once and then send to each of the books (faster/more efficient)
with open('cookingWords.txt') as f1:
	for line in f1:
		line=line.strip() #strip newlines/blanks at beg/end of line
		if not line:
			continue #skip blank lines in file
		if line.startswith('#'):
			continue #skip comments in file
		cookWords=set([line.rstrip('\n') for line in f1])
with open('measurements.txt') as f2:
	for line in f2:
		line=line.strip()
		if not line:
			continue #skip blanks in file
		if line.startswith('#'):
			continue #skip comments in file
		measures=set([line.rstrip('\n') for line in f2])
with open('nyt-ingredients-snapshot-2015.csv') as csvfile:
	reader=csv.DictReader(csvfile)
	foods=set([])
	for row in reader:
		foods.add(row['name'])
	foods=[element.lower() for element in foods] #lowercase everything

files=os.listdir('/home/cbuck/xmlRecipesBooks')
#print(files)
for file in files:
	print(file)
	parsePrint('/home/cbuck/xmlRecipesBooks/'+file,f,cookWords,measures,foods)
#parsePrint('foodNewsletter.xml',f)
#parsePrint('schoolfoodservic00mass_djvu.xml',f)
#parsePrint('CAT31304297_djvu.xml',f)
#parsePrint('CAT31293900_djvu.xml',f)
#parsePrint('schfoodservic7277mont_djvu.xml',f)
#parsePrint('CAT31303133_djvu.xml',f)
#parsePrint('CAT81760442_djvu.xml',f)
#parsePrint('skilfulhousewife00unse_djvu.xml',f)
#CLOSE OUTPUT FILE AFTER RUN ALL THE BOOKS
f.close()



