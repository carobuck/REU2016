#script to make histogram of % recipe and do stratified random sampling (for precision)
#
#make hist first to get idea of shape, then decide how big i want bins before moving to sampling (don't need to sample from every bin...start at highest % and move down till precision drop off..)
import math
from math import floor
import pickle #might as well save ID's and %recipe for later when doing own binning/sampling 
import numpy as np #for making histogram
import matplotlib.pyplot as plt

with open('/home/cbuck/percentClfAsRecipe_2clf') as f:
	recipes=[] #list to store %/amount classified as recipe
	#pgID=[]
	
	for line in f:
		line=line.strip()
		if not line:
			continue #skip if blank line in file
		data=line.split('\t') #make an array out of each line in file
		#print(data) #take out b/c comp take longer to print than to actually process
		#pgID.append(data[0])
		per=floor(100*float(data[2]))
		recipes.append(per) #get just %

		#print(recipes)
				

		#break
	#print(recipes)


#print(recipes) #take out b/c comp take longer to print than to actually process
#print(len(recipes))


#plt.hist(recipes,bins=10) #1-10% bar really high and clobber rest of data
plt.hist(recipes, bins=[20,30,40,50,60,70,75,80,85,90,95,100]) #change bins so actually see something helpful
plt.show()

#save pgID and %recipe (CAN RELOAD LATER INTO LIST AND INDEX FOR SELF-BINNING)
#pickle.dump(pgID, open("savePgID.p","wb"))
#pickle.dump(recipes, open("savePercentRecipe.p","wb"))
#^^DONT REALLY NEED TO PICKLE, B/C FILE I/O SHOULDN'T BE TOO TAXING (THAT'S THE FAST PART..)