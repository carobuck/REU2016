#import necessary libraries
from __future__ import print_function #need this to print to file
import xml.etree.ElementTree as ET #need for parsing XML file of book
import string #need for testing if punctuation in word


#function to parse a book and print its features to a file
#parameters: takes a XML book file; like in this form: 'foodNewsletter.xml'
#and takes file name; if file DNE, will make file of that name
#Will make new output file for each xml book (if give new output file name for each book)
def parsePrint(xmlBk,f):
	tree=ET.parse(xmlBk) #parse xml
	pages=tree.findall(".//OBJECT") #store all the bk pages in list called 'pages' 
	for p in pages:
		x = p.attrib['usemap'][:-5]
		print(x+'\t'+str(numDigits(p))+'\t'+str(punct(p))+'\t'+str(numWords(p)),file=f)

#counts # of digits and digits with punctuation
def numDigits(page):
	digPunc=0
	pg=page.findall(".//WORD")
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
	return digPunc

#returns proportion of punctuation to words on a page
def punct(page):
	punc=0
	pg=page.findall(".//WORD")
	for i in range(len(pg)):
		for c in pg[i].text:
			if c in string.punctuation:
				punc+=1
	if len(pg)==0:
		return 0 #MAYBE CHANGE LATER FOR HOW TO DEAL WITH BLANK PAGES??
	else:
		return float(punc)/len(pg)

#returns # of words on a page
def numWords(page):
	pg=page.findall(".//WORD")
	return len(pg)



#for each line in book, want to print:
# (bkname_page#	numDigits	punctuation	numWords )

#OPEN ONE OUTPUT FILE FOR HOWEVER MANY BOOKS TO RUN THRU
f=open('extract_book_output','w')
#FOR EACH BOOK, SEND XML AND f (FILE STREAM)
parsePrint('foodNewsletter.xml',f)
parsePrint('specialnewsrelea00unit_djvu.xml',f)
parsePrint('annualreportswa72deptgoog_djvu.xml',f)
parsePrint('manualvertebrat02jordgoog_djvu.xml',f)
parsePrint('feasibilitystudy02mill_djvu.xml',f)
parsePrint('studiesofweathertypesandstorms.xml',f)
#CLOSE OUTPUT FILE AFTER RUN ALL THE BOOKS
f.close()

# 1=PROSE
# 0=OTHER