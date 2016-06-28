#SCRIPT TO PLAY WITH ADDING NEW FEATURES FOR DETECTING RECIPES
#EVENTUALLY ADD THESE TO extract_book2.py

#import necessary libraries
from __future__ import print_function #need this to print to file
import xml.etree.ElementTree as ET #need for parsing XML file of book
import string #need for testing if punctuation in word
#import nltk
from nltk.stem.snowball import SnowballStemmer
import csv
import itertools #need for merging list of lists into a single list

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
				#	print(word,origWord) #test to see if working
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

def parsePrint(xmlBk,f):
	tree=ET.parse(xmlBk) #parse xml
	pages=tree.findall(".//OBJECT") #store all the bk pages in list called 'pages' 
	for p in pages:
		x = p.attrib['usemap'][:-5]
		#print(x+'\t'+str(numDigits(p))+'\t'+str(punct(p))+'\t'+str(scaledWords(p,pages)),file=f)

def numDigits(page):
	digPunc=0
	pg=page.findall(".//WORD")
	for tag in pg:
		word=tag.text
		
	if len(pg)==0: #DONT FORGET TO DEAL WITH BLANK PAGES!!
		return 0 #return 0 if have blank page

def ingPhraserBAD(page,foods,measures):
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
	return ingPhrase #return proportion of ingPhrases/#lines on pg...
	#^^^not perf; may bias towards recipes with fewer or more ingredients???


#MODIFY THIS SO CHECKS IF GET MEASURE+[OF]+FOOD WORD
def ingPhraser(page,foods,measures):
	ingPhrase=0
	lines=page.findall(".//LINE")
	if len(lines)==0: #deal with blank page
		return 0
	for l in lines:
		#foodWord=False #DON'T NEED ANYMORE??
		unitWord=False
		of=False
		phrase=''  #use for debugging
		words=l.findall(".//WORD")
		for tag in words:
			phrase+=tag.text+' '  #use for debugging
			x=tag.text
			x.casefold() 
			if unitWord and of:
				x=stemmer.stem(x)
				if x in foods: 
					ingPhrase+=1 # have MEASURE + OF + FOOD phrase
					print(phrase) #debugging
					break  #does this break out of the line??
				else:
					break #if next word isn't a food, want to break to next line
			if unitWord:
				x=stemmer.stem(x)
				if x=='of':
					of=True 
					continue
				elif x in foods:  
					ingPhrase+=1 #have MEASURE + FOOD phrase
					print(phrase) #debugging
					break
				else:
					break #if next word isn't 'of' or food, want to break to next line (this may be a bit harsh/restrictive??)
			if x in measures:
				unitWord=True
				continue
	#return(ingPhrase)
	#return float(ingPhrase)/len(lines)		
# ^^^^CHECK TO MAKE SURE LOGIC WORKS AS I EXPECT IT TO...run to test;
	

with open('measurements.txt') as f2:
	for line in f2:
		line=line.strip()
		if not line:
			continue #skip blanks in file
		if line.startswith('#'):
			continue #skip comments in file
		measures=set([line.rstrip('\n') for line in f2])
#*****MODIFY THIS SO SPLIT ON SPACES AND TAKE OUT #/MEASURE WORDS AND COOK WORDS
with open('nyt-ingredients-snapshot-2015.csv') as csvfile:
	reader=csv.DictReader(csvfile)
	tempFoods=set([]) #use set so don't get repeats (yes)
	for row in reader:
		tempFoods.add(row['name'])
	tempFoods=[element.lower() for element in tempFoods] #lowercase everything
	#print(foods)
	tempFoods=[element.split(' ') for element in tempFoods] #split everything into single words
	foods=list(itertools.chain.from_iterable(tempFoods))
	#^^check over what I get from this before moving on...
	print('\n'+'\n'+'poooop'+'\n')
	print(len(foods))
	for f in foods:
		if f in measures: 
			foods.remove(f)
		if f.isdigit():
			foods.remove(f)
		f=stemmer.stem(f) #stem all the foods (for differences like berry vs berries)	
	foods.remove('of')	
	foods.remove('the')	#of, the, be prove problematic...but doesn't entirely work to remove?? 
	foods.remove('be')  #something else must be going on...????
			
	print('\n'+'\n'+'poooop'+'\n')

	print(len(foods))		

print(stemmer.stem('berry')) #berries and berry both stem to berri! yay :)
print(stemmer.stem('of'))

print('\n'+'\n'+'poooop'+'\n')

tree=ET.parse('foodNewsletter.xml') #parse xml
pages=tree.findall(".//OBJECT") #store all the bk pages in list called 'pages'
sumA=0
sumBAD=0
for p in pages:
	sumA+=ingPhraser(p,foods,measures)
	sumBAD+=ingPhraserBAD(p,foods,measures)
print(str(sumA)+"\n"+"\n"+str(sumBAD))	