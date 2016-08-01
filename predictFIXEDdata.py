"""
Script to predict on book pages that have truth data (can use to evaluate how well classifiers do)
this script is similar to predictBooks.py, but has more for reporting error rates of prediction
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
from sklearn.metrics import confusion_matrix


clf=pickle.load(open("saveModel.p","rb")) #original classifier/model
clf2=pickle.load(open("saveModel_2clf.p","rb"))	#load learned model in enhanced classifier


outf=open('test_cluster_recPercent','w')
Xtest, Ytest=load_svmlight_file("otherClusterTest_ML") #testML_cluster for 179 test set
count=0													#otherClusterTest_ML has stuff sampled from 2nd clf, with 6 pages removed
for i in Ytest:
	if i==1:
		count+=1
print(count) #getting how many 'no'/'yes'

names_test = []
with open('otherClusterTest_ML') as f: #FIXED data set (never trained on)
	for line in f:
		line=line.strip()
		if not line:
			continue #skip blank lines in file
		data=line.split(' ')
		names_test.append(data[10].strip('#'))
print(len(names_test))

predictPgs=clf.predict_proba(Xtest) #use predict_proba if want % a page is a recipe
predictPgs2=clf2.predict_proba(Xtest) #USE SECOND, RETRAINED CLF HERE
print(len(predictPgs)) #debugging	
print(len(predictPgs2)) #debugging
print(predictPgs2) #debugging

rec=0
recipe1=0
recipe2=0

for i in range(len(predictPgs)):
	if predictPgs[i,1]!=0 and predictPgs2[i,1]!=0: #predicted as >0% recipe for both clf
		rec+=1
		#print(names_test[i])
		print(names_test[i]+'\t'+str(predictPgs[i,1])+'\t'+str(predictPgs2[i,1]),file=outf) #print pgID and %recipe
	if predictPgs[i,1]!=0:
		#print(names_test[i])
		recipe1+=1
	if predictPgs2[i,1]!=0:
		recipe2+=1
		#print(names_test[i])
print(rec)
print(recipe1)
print(recipe2)


confusion1=confusion_matrix(Ytest,predictPgs)
print(confusion1)
Err=1-metrics.jaccard_similarity_score(predictPgs,Ytest) 
print("Training Error Rate is: %.4f"%(Err,))

confusion2=confusion_matrix(Ytest,predictPgs2)
print(confusion2)
Err=1-metrics.jaccard_similarity_score(predictPgs2,Ytest) 
print("Training Error Rate is: %.4f"%(Err,))