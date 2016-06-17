#script to make dict (hashmap) for language modeling; common words in recipes
from __future__ import print_function #need this to print to file
import xml.etree.ElementTree as ET #need for parsing XML file of book
import string #need for testing if punctuation in word
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
			if word in langModel:
				langModel[word]+=1
				#totalWords+=1 #INCREMENT HERE?!?! WON'T GET UNIQUE WORDS
			else:
				langModel[word]=1
				totalWords+=1
	for key in langModel:
		if langModel[key]==1: #ERROR HERE; MAYBE JUST IGNORE/DON'T PRINT THOSE WITH VALUE 1 RATHER THAN DELETING
			del langModel[key] #delete keys that only occur once	
	print(langModel)
	print(len(langModel))
	#READ IN WORD; SOME SORT OF FILE PROCESSING HERE (word is string)
	
languageModel('foodNewsletter.xml') #size: 8291 unique words; w/ repeats read in 34948 words
languageModel3('foodNewsletter.xml') #with stemming: size= 6037


#SHOULD i DO SOME STEMMING BEFORE TESTING IF WORD IN DICT? THAT WAY DON'T HAVE 
# REPEATS LIKE ingredient and ingredientS....???? ok since do stemming in learning alg/features too???
# ********try with and without stemming**********