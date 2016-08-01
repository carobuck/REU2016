"""
This is supplementary script just counts the number of 1/0's in truth data
This can also be found in other scripts
"""
from __future__ import print_function #need this to print to file

non=0
yes=0

judgmentByPageId = {} #make a map/dict to store data and key
with open('recipeVsWith1848') as f:
	for line in f:
		line = line.strip() #strip newlines/blanks at beg/end of line
		if not line: 
			continue #skip if blank line in file
		if line.startswith('#'):
			continue #skip comments in file
		arr = line.split('\t')
		pageId = arr[0]
		judgment = arr[1]
		if judgment=='0': #change 0's to -1 (what svm_learn wants)
			judgment='-1'
			non+=1
		if judgment=='1':
			yes+=1
	
		#[pageId, judgment] = line.split('\t') **single line of code to do same as above 3 lines
		
		#This line puts data in dict, creates line for pageId
		judgmentByPageId[pageId] = judgment
print(non,' NON')
print(yes,' recipes')