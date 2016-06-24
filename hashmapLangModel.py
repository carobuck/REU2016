#script to make dict (hashmap) for language modeling; common words in recipes
from __future__ import print_function #need this to print to file
import xml.etree.ElementTree as ET #need for parsing XML file of book
import string #need for testing if punctuation in word
from math import log10 #need for dealing with small probabilities
from nltk.stem.snowball import SnowballStemmer #need to stem words for cookWords and measureWords features
stemmer=SnowballStemmer("english") #set up stemmer

def languageModel(xmlBk):
	langModel={} # {} makes new dict; is equivalent to: dict()
	#langModel['bread']=1
	#print(len(langModel))
	#print(langModel['bread']) #need ' ' around string;
	# here string bread is key, and 1 will be counter; increment each time find in document
	# add any new words to dict
	totalWords=0 #counter to store total number of unique words read in/stored in dict

	tree=ET.parse(xmlBk) #parse xml
	pages=tree.findall(".//OBJECT") #store all the bk pages in list called 'pages' 
	for p in pages:
		pg=p.findall(".//WORD")
		for tag in pg:
			word=tag.text
			if word in langModel:
				langModel[word]+=1
				#totalWords+=1 #INCREMENT HERE?!?! WON'T GET UNIQUE WORDS
			else:
				langModel[word]=1
				totalWords+=1
	print(langModel)
	print(len(langModel))
	print(totalWords)
	#READ IN WORD; SOME SORT OF FILE PROCESSING HERE (word is string)

def languageModel2(xmlBk):
	langModel={} # {} makes new dict; is equivalent to: dict()
	totalWords=0 #counter to store total number of unique words read in/stored in dict

	tree=ET.parse(xmlBk) #parse xml
	pages=tree.findall(".//OBJECT") #store all the bk pages in list called 'pages' 
	for p in pages:
		pg=p.findall(".//WORD")
		for tag in pg:
			word=tag.text
			word=stemmer.stem(word)
			if word in langModel:
				langModel[word]+=1
				#totalWords+=1 #INCREMENT HERE?!?! WON'T GET UNIQUE WORDS
			else:
				langModel[word]=1
				totalWords+=1
	print(langModel)
	print(len(langModel))
	#READ IN WORD; SOME SORT OF FILE PROCESSING HERE (word is string)

def languageModel3(xmlBk):
	langModel={} # {} makes new dict; is equivalent to: dict()
	totalWords=0 #counter to store total number of unique words read in/stored in dict

	tree=ET.parse(xmlBk) #parse xml
	pages=tree.findall(".//OBJECT") #store all the bk pages in list called 'pages' 
	for p in pages:
		pg=p.findall(".//WORD")
		for tag in pg:
			word=tag.text
			if word.isalpha():
				#word=stemmer.stem(word) #stem word
				word=word.casefold()   #all lowercase 
				if word in langModel:
					langModel[word]+=1
					totalWords+=1 #INCREMENT HERE?!?! WON'T GET UNIQUE WORDS
				else:
					langModel[word]=1
					totalWords+=1
	totalWords=float(totalWords)
	for key in langModel:
		langModel[key]=log10(langModel[key]/totalWords)
		#if langModel[key]==1: #ERROR HERE; MAYBE JUST IGNORE/DON'T PRINT THOSE WITH VALUE 1 RATHER THAN DELETING
		#	del langModel[key] #delete keys that only occur once	
	langModel['$MISSING'] = log10(0.5/totalWords)
	print(langModel)
	print(len(langModel))
	#READ IN WORD; SOME SORT OF FILE PROCESSING HERE (word is string)
	
#languageModel('foodNewsletter.xml') #size: 8291 unique words; w/ repeats read in 34948 words
languageModel3('foodNewsletter.xml') #with stemming: size= 6037

def scoreWord(langModel, word):
	if word in langModel:
		return langModel[word] # log P(w|langModel)
	else:
		return langModel['$MISSING'] # "cheat" of sorts; want to give low score to words that don't appear in model


def scoreWords(langModel, words): #would words be a whole line??? then lang model would need to include foods and measure words
	score = 0 
	for w in words:
		score += scoreWord(langModel, w)
	return score / len(words)

#SHOULD i DO SOME STEMMING BEFORE TESTING IF WORD IN DICT? THAT WAY DON'T HAVE 
# REPEATS LIKE ingredient and ingredientS....???? ok since do stemming in learning alg/features too???
# ********try with and without stemming**********


#*****************************
#train/make lang model based on NYTimes csv data, break up food names into single words (split on spaces!!) and build prob model based on that
#maybe include other foods/ingredient lists also?? scrape off internet
#maybe make several lang models, for foods and measureWords??--> or need to combine into one for whole line probability of having food and measure words

# ^^ will this even make it better? won't pull up things with #'s and/or food and measureWords??