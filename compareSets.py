"""
script to compare sets of things; to see if there is overlap in train/test data
"""

from __future__ import print_function #need this to print  
import string

count=0
pgs1=set([])
pgs2=set([])
pgs3=set([])

with open('stratSample2CLF') as f1:
	for line in f1:
		line=line.strip() #strip newlines/blanks at beg/end of line
		if not line:
			continue #skip blank lines in file
		if line.startswith('#'):
			continue #skip comments in file
		data=line.split(' ')
		pgs1.add(data[1])
		count+=1 #debugging

print(count)
print(len(pgs1))
#print((pgs1)) #debugging

with open('MLfileRecipe_train_Wcluster') as f2:
	for line in f2:
		line=line.strip()
		if not line:
			continue #skip blank lines in file
		data=line.split(' ')
		pgs2.add(data[10].strip('#'))
print(len(pgs2))

overlap=set(pgs1.intersection(pgs2))
print(len(overlap))
print(overlap)	

with open('testML_cluster') as f3: #testML_cluster
	for line in f3:
		line=line.strip()
		if not line:
			continue #skip blanks
		data=line.split(' ')
		pgs3.add(data[10].strip('#'))
print(len(pgs3))

over=set(pgs3.intersection(pgs2))
print(len(over))
print(over)


