"""
script to just make histogram of % recipe 
If want to sample from various bins, and make histogram, use histSamplePercentRec.py
"""
import math
from math import floor
import pickle #might as well save ID's and %recipe for later when doing own binning/sampling 
import numpy as np #for making histogram
import matplotlib.pyplot as plt

with open('/home/cbuck/proteusPerRec_500rec') as f:
	recipes=[] #list to store %/amount classified as recipe
	eightyFive=[]	#list to store recipes w/ >= 85% confidence
	
	for line in f:
		line=line.strip()
		if not line:
			continue #skip if blank line in file
		data=line.split('\t') #make an array out of each line in file
		#print(data) #take out b/c comp take longer to print than to actually process
		#pgID.append(data[0])
		per=floor(100*float(data[2]))
		recipes.append(per) #get just %

		if(per>=85):
			eightyFive.append(data[0])

	#print(recipes)

print(eightyFive)
print(len(eightyFive))
#print(recipes) #take out b/c comp take longer to print than to actually process
#print(len(recipes))

plt.title('Number of "Recipes" in Poetry Collection')
#plt.hist(recipes,bins=10) #1-10% bar really high and clobber rest of data
#plt.hist(recipes, bins=[20,30,40,50,60,70,75,80,85,90,95,100]) #change bins so actually see something helpful
plt.hist(recipes, bins=[60,65,70,75,80,85,90,95,100]) #change bins so actually see something helpful

plt.show()
