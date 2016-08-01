"""
This is linear/SVM machine learning script. Not used for model because randomForest Classifier worked better for predicting

"""

#MACHINE LEARNING AND PLOTTING SCRIPT
#ON THIS SCRIPT, CAN GO BACK AND FORTH BETWEEN YTEST AND YLEARN, TO SEE HOW WELL MACHINE PREDICTS FOR XTEST VS XLEARN (want xlearn to be perfect...)


#scikit learn
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

#%matplotlib inline

X_train, y_train=load_svmlight_file("MLfileRecipe_train4")
names = []
with open('MLfileRecipe_train4') as f:
	for line in f:
		if '#' in line:
			pos = line.index('#')
			names += [line[pos:]]
#print(names)


C=1 #regularization setting; how tight to fit data
kernel='rbf'
g=1 #gamma; how "fast it falls off"/how smooth distiction is between groups

#Define the parameter grid ; give poss values of C and gamma (parameters to search over to see what best)
#param_grid = [{'C': [0.01,0.1,1, 10, 100], 'kernel': ['rbf','poly','linear'],'gamma': [0.1,1,10,100]}]

#OTHER param_grids FOR OTHER LEARNING ALG
#param_grid = [{'nu':[0.1,0.5,0.9],'kernel': ['rbf','poly','linear'],'gamma': [0.1,1,10,100]}] #use for svm.NuSVC
#param_grid = [{'C': [0.01,0.1,1, 10, 100], 'kernel': ['rbf'],'gamma': [0.1,1,10,100]}] #use for svm.SVR
param_grid = [{'C': [1,10,50,100,150,500,1000],'random_state':[17,27,3,42,75]}] #use for svm.LinearSVC

#Create a learning set/test set split
Xlearn,Xtest,Ylearn,Ytest,names_learn,names_test = cross_validation.train_test_split(X_train, y_train,names, test_size=0.25, random_state=42)
#random state shuffles data so its random; then test_size takes off 25% to validate

#Do search for optimal parameters using 
#5-fold cross validation on the learning set
#clf = GridSearchCV(svm.SVC(C=1, probability=True), param_grid, cv=5)

#try other alg for svm

#clf = GridSearchCV(svm.NuSVC(nu=.5, probability=True), param_grid, cv=5)
#clf = GridSearchCV(svm.SVR(degree=3), param_grid, cv=5)
clf = GridSearchCV(svm.LinearSVC(C=1, random_state=1), param_grid, cv=5)
#^^FOUND LINEARSVC works best for my data right now...



#fit the classifier
#clf=svm.SVC(C=C, kernel=kernel, gamma=g) #use this line if only run once, w/out param grid
clf.fit(Xlearn,Ylearn)

#print optimal parameter set
print ("Optimal Parameters:", clf.best_params_)

#make predictions using model
Yhat=clf.predict(Xtest) #expected outcomes, using the model
#Yhat=clf.predict(Xlearn) #see if it can predict the training ones right at all (if not, 3 features are currently garbage)
Yd=clf.decision_function(Xtest) #changed Xtest to Xlearn

# decision_function is similar to predict_proba, but for LinearSVC (bigger # means comp more confident about it's prediction; closer to 0=less confident)

#try adding in function to score data points, to see how far off things are from being marked as recipe or not
#score=clf.predict_proba(Xtest) 
#print(score)


#compute precision-recall and plot curve
precision=dict()
recall=dict()
average_precision=dict()
for i in range(2): #2 b/c have two target values (recipe or not)
	precision[i], recall[i],_=precision_recall_curve(Ytest,Yd)    #CHANGED TO YLEARN FROM YTEST
	average_precision[i]=average_precision_score(Ytest,Yd)

#try to print names of pages that were WRONGLY predicted
sumWrong=0
for i in range(len(names_test)):
	if Ytest[i] != Yhat[i]: #TRY ALSO WITH Yd??? #CHANGED TO yLEARN FROM YTEST
		sumWrong+=1
		print(names_test[i])
		print(Yd[i])
		#print(score[i]) #print info about misses (scores and feature values)
		print(Xtest[i])
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
#bk500X,ytrash=load_svmlight_file('MLfile500_3')
#print(bk500X,ytrash)
#predict500=clf2.predict(bk500X)

#names500 = []
#with open('MLfile500_3') as f:
#	for line in f:
#		if '#' in line:
#			pos = line.index('#')
#			names500 += [line[pos:]]
#recipes=0
#for i in range(len(predict500)):
#	if predict500[i]==1:
#		#print(predict500[i])
#		print(names500[i]+'\t'+'0')
#		recipes+=1
#print(recipes)
#print(len(predict500))

#Plot precision-recall curve (THIS IS PLOT OF TEST DATA; WHAT USED TO TRAIN MACHINE)
plt.clf()
plt.plot(recall[0],precision[0],label='Precision-Recall curve')
plt.xlabel('Recall')
plt.ylabel('Precision')
plt.ylim([0.0,1.05])
plt.xlim([0.0,1.0])
plt.show()




#report error rate
Err=1-metrics.jaccard_similarity_score(Yhat,Ytest) #CHANGED YTEST TO YLEARN
print("Training Error Rate is: %.4f"%(Err,))

#other metrics to try: average_precision_score; precision_score; accuracy_score (used this in bootcamp)
#b/c why not: jaccard_similarity_score (how much the sets of actual and predicted Y overlap)

#trying other metrics:
#print(metrics.auc(Yhat,Ytest))
#print(metrics.precision_recall_curve(Ytest,Yhat))

#ON THIS SCRIPT, CAN GO BACK AND FORTH BETWEEN YTEST AND YLEARN, TO SEE HOW WELL MACHINE PREDICTS FOR XTEST VS XLEARN (want xlearn to be perfect...)
