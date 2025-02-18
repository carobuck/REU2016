"""
SCRIPT JUST TO PREDICT BOOKS (USES IMPORTED/pickled MODEL FROM RAND FOREST CLF)
Predicts either y/n (learns a cutoff point with .predict) or gives confidences/% recipe for pages (using .predict_proba)
"""
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

clf=pickle.load(open("saveModel.p","rb")) #original classifier
clf2=pickle.load(open("saveModel_2clf.p","rb"))	#load learned model in 2nd classifier
												#"enhanced" classifier; same features as original, just with more training data

#open a file to record names of pages classified as recipes
outf=open('FIXED_data_predictions','w') 

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
		#pgs.append('\n') #new line (make 2d array???)	<--for sklearn, can give predict a numpy matrix (2d arr), or can give a python list of list, which is what I do
		pgs += [p]
		names.append(arr[0])
	#print(pgs) #debugging
	#predictPgs=clf2.predict(pgs) #use predict if just want y/n, 1 or -1 classification
	predictPgs=clf.predict_proba(pgs) #use predict_proba if want % a page is a recipe
	predictPgs2=clf2.predict_proba(pgs) #USE SECOND, RETRAINED CLF HERE
	#print(predictPgs) #debugging
	#print(predictPgs2) #debugging
	rec=0
	for i in range(len(predictPgs)):
		if predictPgs[i,1]!=0 and predictPgs2[i,1]!=0: #predicted as >0% recipe for both clf
			rec+=1
			#print(names[i])
			print(names[i]+'\t'+str(predictPgs[i,1])+'\t'+str(predictPgs2[i,1])+'\n',file=outf) #print pgID and %recipe
	return(rec)

#trying to get only 1000 lines at a time from giant file...
with open("extract_500poemsProteus") as bigF:
	afew = []
	recipes=0
	for idx, line in enumerate(bigF):
		if idx%20000==0:
			print(idx)
		if(len(afew) >= 100):
			#print(afew) #debugging
			recipes+=process(afew)
			#break		#can use break to play around with for debugging purposes
						#and can deal with just a few lines at a time, like 5, rather than 1000
			afew = [] #clear list again to read in new things...
		afew += [line]
	#process(afew); #process/deal with last few lines in file (that are leftover/not more than 1000 or whatever cutoff is for len(afew))
	print(recipes) #print total # of pages flagged as recipe
	