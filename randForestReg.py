"""
****Did not use this classifier for final model (Random forest classifier performed best)
**RANDOM FOREST REGRESSION can learn and predict model with regression
#maybe use this rather than randForestClf to try to get ranked list output****
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

#import to try to get plots
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import average_precision_score
from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import label_binarize
from sklearn.multiclass import OneVsRestClassifier
from sklearn.metrics import confusion_matrix

X_train, y_train=load_svmlight_file("MLfileRecipe_train5")
names = []
with open('MLfileRecipe_train5') as f:
	for line in f:
		if '#' in line:
			pos = line.index('#')
			names += [line[pos:]]
#print(names)

#Define the parameter grid 
param_grid=[{'n_estimators':[5,10,15],'max_features':['auto','sqrt','log2']}]

#Create a learning set/test set split
#*****CAN CHANGE TO .75 IN TEST AND STILL GET 90-92% ACCURACY!!*****
Xlearn,Xtest,Ylearn,Ytest,names_learn,names_test = cross_validation.train_test_split(X_train, y_train,names, test_size=0.25, random_state=42)
#random state shuffles data so its random; then test_size takes off 25% to validate

#Do search for optimal parameters using 
#5-fold cross validation on the learning set *****IF GIVE RANDOM_STATE, WILL GIVE SAME RESULTS EACH TIME RUN; otherwise, randomizes differently each time!!
clf=GridSearchCV(ensemble.RandomForestRegressor(random_state=17),param_grid,cv=5)

#fit the classifier
clf.fit(Xlearn,Ylearn)

#print optimal parameter set
print ("Optimal Parameters:", clf.best_params_)

#make predictions using model 
Yhat=clf.predict(Xtest) #expected outcomes, using the model
#Yhat=clf.predict(Xlearn) #see if it can predict the training ones right at all (if not, 3 features are currently garbage)
print(Yhat)

#try adding in function to score data points, to see how far off things are from being marked as recipe or not
score=clf.score(Xtest,Ytest)
print(score)


#try to print names of pages that were WRONGLY predicted
sumWrong=0
for i in range(len(names_test)):
	if Ytest[i] != Yhat[i]: #TRY ALSO WITH Yd??? #CHANGED TO yLEARN FROM YTEST
		sumWrong+=1
		print(names_test[i])
		print(Yhat[i])
		#print(score[i]) #print info about misses (scores and feature values)
		#print(Xtest[i])
print(sumWrong,float(sumWrong)/float(len(names_test))) #CHANGED NAMES_TEST TO NAMES_LEARN




#print info (scores and feature values) about correct predictions
#for i in range(len(names_test)):
#	if Ytest[i]==Yhat[i]:
#		if Ytest[i]==1:
#			print(names_test[i])
#			print(score[i]) 
#			print(Xtest[i])

#NOW TRY TO USE MODEL TO PREDICT/IDENTIFY RECIPES IN RANDOM BOOKS
#import pickle 	
#model=pickle.dumps(clf) 	#Store learned model
#clf2=pickle.loads(model)	#load learned model in 2nd classifier

clf2 = clf  #DON'T NEED TO PICKLE; CAN JUST STORE IN ANOTHER VARIABLE
bk500X,ytrash=load_svmlight_file('MLfile_FIXED_data')
#print(bk500X,ytrash) #debugging
predict500=clf2.predict(bk500X)
#score=clf2.predict_proba(bk500X)
#print(score)
#percentRecipe=score[:,0]

#for idx, [a,b] in enumerate(score):
#	print(idx, a,b)

#print(percentRecipe)
names500 = []
with open('MLfile_FIXED_data') as f:
	for line in f:
		if '#' in line:
			pos = line.index('#')
			names500 += [line[pos:]]
recipes=0
toRank = []
for i in range(len(predict500)):
	toRank += [(predict500[i], names500[i], i)] #make a tuple out of prediction, name/ID, index
	if predict500[i]==1: #ie, algorithm says this is "100% a recipe"
		#print(predict500[i])
		print(names500[i]+'\t'+'0')
		#print(percentRecipe[i])
		recipes+=1
ranked = sorted(toRank, reverse=True)[:7000] #this last bit takes just the top 100; reverse ranks from high->low
print(ranked) #print top 100 "recipes"
print(recipes)
print(len(predict500))

