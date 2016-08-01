"""
THIS SCRIPT IS FOR MAKING ML FILE FROM STRATIFIED SAMPLE 
TRUTH DATA FROM RUNNING ON CLUSTER

This was used to make enhanced classifier (same features as original, just more training data)
"""

#program to combine training data (from file like proseVsOther) and features file of book (output of extract_book.py)
from __future__ import print_function #need this to print to file

non=0
yes=0

judgmentByPageId = {} #make a map/dict to store data and key
with open('truthDataFromCluster') as f:
	for line in f:
		line = line.strip() #strip newlines/blanks at beg/end of line
		if not line: 
			continue #skip if blank line in file
		if line.startswith('#'):
			continue #skip comments in file
		arr = line.split(' ')
		pageId = arr[1]
		judgment = arr[0]
		if judgment=='NO' or judgment=='NON?': #change 0's to -1 (what svm_learn wants)
			judgment='-1'
			non+=1
		if judgment=='YES':
			judgment='1'
			yes+=1
	
		#[pageId, judgment] = line.split('\t') **single line of code to do same as above 3 lines
		
		#This line puts data in dict, creates line for pageId
		judgmentByPageId[pageId] = judgment
print(non)
print(yes)
print(judgmentByPageId)
#print(judgmentByPageId) this line prints the map/dict made above
#print(judgmentByPageId['feasibilitystudy02mill_0218']) this line shows how to access value for given key in dict

outf=open('MLfile_cluster_truth','w') #open file for machine learning output

with open('/home/cbuck/some_features') as f:
	for idx, line in enumerate(f):  #add in these lines so can see code is running
		if idx % 20000 == 0:
			print(idx)
		arr=line.strip().split('\t')
		#print(arr) #debugging
		if arr[0] in judgmentByPageId:
			featureStr=judgmentByPageId[arr[0]] #put judgment in featureStr
			for i in range(len(arr[1:])): #len is getting # of features
				featureStr+=' '+str(i+1)+':'+arr[i+1] #add all features to featureStr with proper formatting
			featureStr+=' #'+arr[0]
			print(featureStr,file=outf) #print feature string to output file
outf.close()
