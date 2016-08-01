
"""
program to combine truth data and extracted features file of book 
use for making ML file for training models

**also, for judgments, converts all to 1 or 0 ("NON?" pages, non food recipes, are treated as 0)
"""
from __future__ import print_function #need this to print to file

non=0
yes=0

judgmentByPageId = {} #make a map/dict to store data and key
with open('stratSample2CLF') as f:
	for line in f:
		line = line.strip() #strip newlines/blanks at beg/end of line
		if not line: 
			continue #skip if blank line in file
		if line.startswith('#'):
			continue #skip comments in file
		arr = line.split(' ')
		pageId = arr[1]		#**may need to change array indices here, depending on order of pgID and judgment on line
		judgment = arr[0]
		if judgment=='0': #change 0's to -1 (what svm_learn wants)
			judgment='-1'
			non+=1
		if judgment=='NO': 
			judgment='-1'
			non+=1	
		if judgment=='A': 
			judgment='-1'
			non+=1	
		if judgment=='NON?': 
			judgment='-1'
			non+=1	
		if judgment=='1':
			yes+=1
		if judgment=='YES':
			judgment='1'
			yes+=1	
	
		#[pageId, judgment] = line.split('\t') **single line of code to do same as above 3 lines
		
		#This line puts data in dict, creates line for pageId
		judgmentByPageId[pageId] = judgment
print(non)
print(yes)
#print(judgmentByPageId) this line prints the map/dict made above
#print(judgmentByPageId['feasibilitystudy02mill_0218']) this line shows how to access value for given key in dict

outf=open('otherClusterTest_ML','w') #open file for machine learning output

with open('/home/cbuck/some_features') as f:
	for line in f:
		arr=line.strip().split('\t')
		#print(arr)
		if arr[0] in judgmentByPageId:
			featureStr=judgmentByPageId[arr[0]] #put judgment in featureStr
			for i in range(len(arr[1:])): #len is getting # of features
				featureStr+=' '+str(i+1)+':'+arr[i+1] #add all features to featureStr with proper formatting
			featureStr+=' #'+arr[0]
			print(featureStr,file=outf) #print feature string to output file
outf.close()

		