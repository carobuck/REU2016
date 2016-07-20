#script to extract just pages with recipes on them; store all words from those pages in file (file for each page)


from __future__ import print_function #need this to print to file
import xml.etree.ElementTree as ET #need for parsing XML file of book
import string #need for testing if punctuation in word
import os
from os import listdir #need for reading all files from folder
import math
from math import floor

def getRecipePgs(xml_bk,recPgs):
	tree=ET.parse(xml_bk) #parse xml
	pages=tree.findall(".//OBJECT") #store all the bk pages in list called 'pages' 
	for p in pages:
		bkPg = p.attrib['usemap'][:-5]  #get page name_# so can reference later
		#print(bkPg) #debugging
		if bkPg in recPgs:
			outf=open('/home/cbuck/recipePages/'+bkPg,'w')
			words=p.findall(".//WORD")
			for tag in words:
				#print(tag.text) #debugging
				print(str(tag.text),file=outf)
			outf.close()

#get set with recipe pages (w/ specific %/confidence recipe)
with open('/home/cbuck/percentClfAsRecipe_2clf') as f:
	recipes=set([]) #set to store books that have recipe pgs
	eightyFive=set([])	#set to store recipes w/ >= 85% confidence
						#USE SET HERE B/C HASHABLE AND FASTER (?????)
	
	for idx, line in enumerate(f):
		if idx%20000==0:
			print(idx)
		line=line.strip()
		if not line:
			continue #skip if blank line in file
		data=line.split('\t') #make an array out of each line in file
		per=floor(100*float(data[2]))
		if(per>=85):
			eightyFive.add(data[0])
				

#getRecipePgs('/home/cbuck/detected-poems/365dessertsdesse00nels.xml',eightyFive)
# ^^trial run with just one book (it works!! :)

files=os.listdir('/home/cbuck/detected-poems')

for file in files:
	print(file)
	getRecipePgs('/home/cbuck/detected-poems/'+file,eightyFive)



