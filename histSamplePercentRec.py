"""
script to sample from bins of various confidences/% recipe
Can get random samples, and can also plot a histogram for # of books in various confidence levels
if just want histogram: use makeHist.py (if have large file, sorting into bins and sampling takes a few minutes)
"""

import math
from math import floor
import pickle #might as well save ID's and %recipe for later when doing own binning/sampling 
import numpy as np #for making histogram
import matplotlib.pyplot as plt


with open('/home/cbuck/percentClfAsRecipe_2clf') as f:
	recipes=[] #list to store %/amount classified as recipe
	
	sixty=[]   #make lists to store pgs that fall into these % of recipe clf
	seventy=[]	#these names are LOWER BOUNDS of list (ex, sixty has 60<=x<70)
	seventyFive=[]
	eighty=[]
	eightyFive=[]
	ninety=[]
	ninetyFive=[]
	nSix=[]
	nSeven=[]
	nEight=[]
	nNine=[]
	hundred=[]
	
	for line in f:
		line=line.strip()
		if not line:
			continue #skip if blank line in file
		data=line.split('\t') #make an array out of each line in file
		#print(data) #take out b/c comp take longer to print than to actually process
		#pgID.append(data[0])
		if data[0] in sixPages:
			print(data[0])
			print(data[1])
		per=floor(100*float(data[2]))
		#recipes.append(per) #get just %
		if(per>=60 and per<70):
			sixty.append(data[0])
			continue #go to next line in file
		if(per>=70 and per<75):
			seventy.append(data[0])
			continue #go to next line in file
		if(per>=75 and per<80):
			seventyFive.append(data[0])
			continue #go to next line in file
		if(per>=80 and per<85):
			eighty.append(data[0])
			continue #go to next line in file
		if(per>=85 and per<90):
			eightyFive.append(data[0])
			continue #go to next line in file
		if(per>=90 and per<95):
			ninety.append(data[0])
			continue #go to next line in file

	#INDIVIDUALLY SAMPLE FROM 95-100%		
		if(per==95):
			ninetyFive.append(data[0])
			continue #go to next line in file
		if(per==96):
			nSix.append(data[0])
			continue #go to next line in file
		if(per==97):
			nSeven.append(data[0])
			continue #go to next line in file
		if(per==98):
			nEight.append(data[0])
			continue #go to next line in file	
		if(per==99):
			nNine.append(data[0])
			continue #go to next line in file
		if(per==100):
			hundred.append(data[0])
			continue

				
	#print(recipes)


#print(recipes) #take out b/c comp take longer to print than to actually process
#print(len(recipes))

print(len(sixty))
print(len(seventy))
print(len(seventyFive))
print(len(eighty))
print(len(eightyFive))
print(len(ninety))
print(len(ninetyFive))
print(len(nSix))
print(len(nSeven))
print(len(nEight))
print(len(nNine))
print(len(hundred))




#get random samples of 30 from each of the upper bins (estimating precision)
random60=np.random.choice(sixty,30,replace=False) 
print(random60)

random70=np.random.choice(seventy,30,replace=False) 
print(random70)

random75=np.random.choice(seventyFive,30,replace=False) 
print(random75)

random80=np.random.choice(eighty,30,replace=False) 
print(random80)

random85=np.random.choice(eightyFive,30,replace=False) 
print(random85)

random90=np.random.choice(ninety,30,replace=False) 
print(random90)

random95=np.random.choice(ninetyFive,30,replace=False) 
print(random95)

random96=np.random.choice(nSix,30,replace=False) 
print(random96)

random97=np.random.choice(nSeven,30,replace=False) 
print(random97)

random98=np.random.choice(nEight,30,replace=False) 
print(random98)

random99=np.random.choice(nNine,30,replace=False) 
print(random99)

random100=np.random.choice(hundred,30,replace=False)
print(random100)



#plt.hist(recipes,bins=10) #1-10% bar really high and clobber rest of data
plt.hist(recipes, bins=[20,30,40,50,60,70,75,80,85,90,95,100]) #change bins so actually see something helpful
#plt.show()

