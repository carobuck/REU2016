#***RANDOM FOREST CLASSIFIER; says y/n with rand forest
#harder to get 'ranked list' output for this; just weird quirk of way clf works...

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
param_grid=[{'criterion':['gini','entropy'],'max_features':['auto','sqrt','log2'],'n_estimators':[100],'max_depth':[10]}]

#Create a learning set/test set split
#*****CAN CHANGE TO .75 IN TEST AND STILL GET 90-92% ACCURACY!!*****
Xlearn,Xtest,Ylearn,Ytest,names_learn,names_test = cross_validation.train_test_split(X_train, y_train,names, test_size=0.25, random_state=42)
#random state shuffles data so its random; then test_size takes off 25% to validate

#Do search for optimal parameters using 
#5-fold cross validation on the learning set   ******IF WANT TO 'FIX' CLF, GIVE IT A SPECIFIC RANDOM STATE; w/out, it will randomly change each time it runs
clf=GridSearchCV(ensemble.RandomForestClassifier(random_state=42),param_grid,cv=5)
#clf=GridSearchCV(ensemble.RandomForestClassifier(),param_grid,cv=5)

#fit the classifier
clf.fit(Xlearn,Ylearn)

#print optimal parameter set
print ("Optimal Parameters:", clf.best_params_)

#make predictions using model
Yhat=clf.predict(Xtest) #expected outcomes, using the model
#Yhat=clf.predict(Xlearn) #see if it can predict the training ones right at all (if not, 3 features are currently garbage)
Yd=clf.predict_proba(Xtest) #changed Xtest to Xlearn

#print(Yd) #this gives probability for a page of being recipe or not (% rec, % not) 
#try adding in function to score data points, to see how far off things are from being marked as recipe or not
score=clf.score(Xtest,Ytest)
print(score) #this score is accuracy for randforestclf

print('\n'+'\n'+'poooop'+'\n')

confusion=confusion_matrix(Ytest,Yhat)
print(confusion)

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


print('\n'+'\n'+'poooop'+'\n')


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

clf2 = clf #can just put in a different variable; don't need to pickle
bk500X,ytrash=load_svmlight_file('MLfile_indianMealBk2')
#print(bk500X,ytrash)
predict500=clf2.predict(bk500X)

#THESE LINES MESS AROUND WITH TRYING TO GET SOME SORT OF RANKING...NOT SURE WORKS..
#score=clf2.predict_proba(bk500X)
#print(score)
#percentRecipe=score[:,0]

#for idx, [a,b] in enumerate(score):
#	print(idx, a,b)
#print(percentRecipe)

names500 = []
with open('MLfile_indianMealBk2') as f:
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

#now get a random sample out of the predicted 100% recipes (store in list: randomRec); set replace=False so don't get duplicates
#randomRec=np.random.choice(rec100,30,replace=False) 
#print(randomRec)





#report error rate
Err=1-metrics.jaccard_similarity_score(Yhat,Ytest) #CHANGED YTEST TO YLEARN
print("Training Error Rate is: %.4f"%(Err,))
