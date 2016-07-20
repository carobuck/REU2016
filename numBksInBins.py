#script to find out how many books are in my upper % bins

import math
from math import floor
import pickle #might as well save ID's and %recipe for later when doing own binning/sampling 
import numpy as np #for making histogram
import matplotlib.pyplot as plt

outf=open('pagesForSearchingTRIAL','w')
outf2=open('booksTRIAL','w')
with open('/home/cbuck/percentClfAsRecipe_2clf') as f:
	recipes=set([]) #set to store books that have recipe pgs
	eightyFive=[]	#list to store recipes w/ >= 85% confidence
	
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
			#print(data[0][:-5]) #get just book ID, w/out pg #
			recipes.add(data[0][:-5]) #only adds book ID if not already in the set
			print(data[0]+'\t'+str(data[2]),file=outf)
		#print(recipes)
				

		#break
	#print(recipes)


#print(recipes) #take out b/c comp take longer to print than to actually process
#print(len(recipes))
for x in recipes:
	print(x,file=outf2)
print(len(recipes))
print(len(eightyFive))




