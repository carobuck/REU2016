from __future__ import print_function #need this to print to file

import xml.etree.ElementTree as ET
import string #need for testing if punctuation in word

#this one commented out b/c is really big book; takes long time to run
#tree=ET.parse('betterfruit09wash_djvu.xml') #this line parses the xml file and makes it into a big tree
tree=ET.parse('foodNewsletter.xml') #line to parse file
#print type(tree)

#do I need this line?
root=tree.getroot() #gets root of tree and names it 'root'

pages=tree.findall(".//OBJECT") #this makes a list with all of the pages in the book (128 pages,0-127)
#print type(pages)
#print len(pages)



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
			print('1')
		else:
			print('0')	

for p in pages:
	moreThan10(p)