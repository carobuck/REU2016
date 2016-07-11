#SCRIPT JUST TO PREDICT BOOKS (USES IMPORTED MODEL FROM RAND FOREST CLF)

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from scipy import linalg
from sklearn import neighbors
from sklearn import metrics
from sklearn import svm
from sklearn import cross_validation
from sklearn.grid_search import GridSearchCV
from sklearn.datasets import load_svmlight_file #import command for using my svmlight-style file
from sklearn import ensemble #need for randomForestClassifier
import pickle

clf2=pickle.load(open("saveModel.p","rb"))	#load learned model in 2nd classifier


#clf2 = clf #can just put in a different variable; don't need to pickle
bk500X,ytrash=load_svmlight_file('MLfile_natHist2')
#print(bk500X,ytrash)
predict500=clf2.predict(bk500X)

names500 = []
with open('MLfile_natHist2') as f:
	for line in f:
		if '#' in line:
			pos = line.index('#')
			names500 += [line[pos:]]
#rec100=[] #100% a recipe according to alg; list to store page names
recipes=0
for i in range(len(predict500)):
	if predict500[i]==1:
		#rec100.append(names500[i])
		#print(predict500[i])
		print(names500[i])
		#print(percentRecipe[i])
		recipes+=1
print(recipes)
print(len(predict500))

#open a file to record names of pages classified as recipes
#outf=open('clfAsRecipe','w') #WANT 'W' OR 'A' FOR THIS?!?! WRITE OR APPEND??
outf=open('percentClfAsRecipe','w')

#process function runs model over lines (bk pages) and predicts if they have recipe
def process(lines):
	#pass #pass is equivalent to {} empty function
	
	pgs=[] #make empty array to predict on???
	names=[]
	for line in lines:
		p=[]
		arr=line.strip().split('\t')
		for i in range(len(arr[1:])):
			p.append(float(arr[i+1]))
			#pgs.append(' ') #doesn't like this string...
		#pgs.append('\n') #new line (make 2d array???)	<--for sklearn, can give predict a numpy matrix (2d arr), or can give a python list of list, which is what I do
		pgs += [p]
		names.append(arr[0])
	#print(pgs) #debugging
	#predictPgs=clf2.predict(pgs) #use predict if just want y/n, 1 or -1 classification
	predictPgs=clf2.predict_proba(pgs) #use predict_proba if want % a page is a recipe
	print(predictPgs)
	rec=0
	for i in range(len(predictPgs)):
		if predictPgs[i,1]!=0:
			rec+=1
			print(names[i])
			print(names[i]+'\t'+str(predictPgs[i,1])+'\n',file=outf) #print pgID and %recipe
	return(rec)

#trying to get only 1000 lines at a time from giant file...
with open("/home/cbuck/some_features") as bigF:
	afew = []
	recipes=0
	for line in bigF:
		if(len(afew) >= 100):
			#print(afew) #debugging
			recipes+=process(afew)
			break		#can use break to play around with for debugging purposes
						#and can deal with just a few lines at a time, like 5, rather than 1000
			afew = [] #clear list again to read in new things...
		afew += [line]
	#process(afew); #process/deal with last few lines in file (that are leftover/not more than 1000 or whatever cutoff is for len(afew))
	print(recipes) #print total # of pages flagged as recipe
	



#THESE LINES MESS AROUND WITH TRYING TO GET SOME SORT OF RANKING...NOT SURE WORKS..
#score=clf2.predict_proba(bk500X)
#print(score)
#percentRecipe=score[:,0]

#for idx, [a,b] in enumerate(score):
#	print(idx, a,b)
#print(percentRecipe)



#now get a random sample out of the predicted 100% recipes (store in list: randomRec); set replace=False so don't get duplicates
#randomRec=np.random.choice(rec100,30,replace=False) 
#print(randomRec)





