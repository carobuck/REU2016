"""
script to just find out how many books are in my upper % recipe/confidence bins
(finds how many books are flagged as having recipes in them)
"""
import math
from math import floor

outf=open('pagesForSearchingTRIAL','w')
outf2=open('booksTRIAL','w')
with open('/home/cbuck/percentClfAsRecipe_2clf') as f:
	recipes=set([]) #set to store books that have recipe pgs
	eightyFive=[]	#list to store recipes w/ >= 85% confidence (high precision at/above this confidence level)
	
	for idx, line in enumerate(f):
		if idx%20000==0:
			print(idx)
		line=line.strip()
		if not line:
			continue #skip if blank line in file
		data=line.split('\t') #make an array out of each line in file
		per=floor(100*float(data[2]))
		if(per>=85): 
			eightyFive.append(data[0])
		#	continue #go to next line in file
			recipes.add(data[0][:-5]) #only adds book ID if not already in the set
			print(data[0]+'\t'+str(data[2]),file=outf)
				
	#print(recipes)


for x in recipes:
	print(x,file=outf2)
print(len(recipes))
print(len(eightyFive))




