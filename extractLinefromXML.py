from __future__ import print_function #need this to print to file
import xml.etree.ElementTree as ET #need for parsing XML file of book
import string #need for testing if punctuation in word
from nltk.stem.snowball import SnowballStemmer #need to stem words for cookWords and measureWords features
stemmer=SnowballStemmer("english") #set up stemmer
import os
from os import listdir #need for reading all files from folder


#try this with foodNewsletter.xml

tree=ET.parse('foodNewsletter.xml') #parse xml
pages=tree.findall(".//OBJECT") #store all the bk pages in list called 'pages' 
count=0 #count number of iterations of for loop
for p in pages:
	lines=p.findall(".//LINE")
	for l in lines:
		words=l.findall(".//WORD")
		x=''
		for tag in words:
			x+=tag.text+' '
		print(x)
		print('BLAH')
		


