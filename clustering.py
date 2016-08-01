"""
script to try clustering output from running 2clf (enhanced classifier w/ more training data) on 100k bks from cluster

using this guy's code/assistance: https://github.com/brandomr/document_cluster/blob/master/cluster_analysis.ipynb

This script will cluster the recipes, but it is hard to evaluate what it clusters the recipes on
this needs work if clustering the recipes found in books is a goal (perhaps try other clustering algorithms?)

This script makes a TFIDF matrix of the words in the files (in recipes) and attempts to cluster using K-Means
"""
from __future__ import print_function #need this to print  
import string

import numpy as np
import pandas as pd
import nltk
import re
import os
import codecs
from sklearn import feature_extraction
import os
from os import listdir #need for reading all files from folder
from nltk.stem.snowball import SnowballStemmer #need for stemming
from sklearn.feature_extraction.text import TfidfVectorizer #need for making Tf-idf 
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
from sklearn.feature_extraction import text #need for trying to add stopwords 

stemmer=SnowballStemmer("english")


#GETTING ALL THE WORDS READ IN FROM RECIPES
fTitles=[] #make list to store all file names; the "titles" for each recipe/pg
recipes=[] #list of lists w/ all words from all the pages
rec=[]  #temp recipes
#fullPathRec=[]

#try taking out cook and measure words from recipes (sort of forcing them into stop words)
with open('cookingWords.txt') as f1:
	for line in f1:
		line=line.strip() #strip newlines/blanks at beg/end of line
		if not line:
			continue #skip blank lines in file
		if line.startswith('#'):
			continue #skip comments in file
		cookWords=set([line.rstrip('\n') for line in f1])
with open('measurements.txt') as f2:
	for line in f2:
		line=line.strip()
		if not line:
			continue #skip blanks in file
		if line.startswith('#'):
			continue #skip comments in file
		measures=set([line.rstrip('\n') for line in f2])
#try and add own words to stop_words
my_words=cookWords.union(measures) #make union of 2 sets
my_stop_words=text.ENGLISH_STOP_WORDS.union(my_words)
for word in my_stop_words:
	word=stemmer.stem(word)

punctuation_set = set(string.punctuation)

files=os.listdir('/home/cbuck/recipePages') #use idx to only read in a few lines for debugging, or to see that code is still running
for idx, file in enumerate(files):
	if idx%2000==0:
		print(idx)
		#print(file) #debugging
	fTitles.append(file)
	rec=open('/home/cbuck/recipePages/'+file).read()
	""" #rougher version of measure/cooking stop words; commented out because have union above
	for r in rec:
		if r not in cookWords:
			if r not in measures:
				#print(r)
				recipes.append(r)
	#fullPathRec.append('/home/cbuck/recipePages/'+file)
	"""
	recipe_cleaned = ''.join(ch for ch in rec if ch not in punctuation_set)
	recipes.append(recipe_cleaned.lower().split())

print(len(fTitles))
print(len(recipes)) 
#print(fullPathRec)
randomSample=np.random.choice(fTitles,100,replace=False) 
print(randomSample)

#STEMMING FUNCTION (DON'T NEED TO TOKENIZE, B/C ALREADY HAVE SINGLE WORDS)
def stem(text): #text already tokenized I think...
	filtered_tokens=[] #filter out any words not containing letters (ie #'s, pure punc)
	for token in text:
		if re.search('[a-zA-Z]', token):
			filtered_tokens.append(token)
	stems = [stemmer.stem(t) for t in filtered_tokens] #stem tokens
	return stems

def justToken(text): #this just filters out #'s and pure punc; need so indexes of stemmed words line up w/ orig versions
	filtered_tokens=[] #filter out any words not containing letters (ie #'s, pure punc)
	for token in text:
		#if isalpha(token):
		if re.search('[a-zA-Z]', token):
			filtered_tokens.append(token) #INCL STRING.PUNC HERE in translate?? GET ERROR FOR TOO MANY ARG TO .TRANSLATE, BUT THAT'S WHAT EX DID ONLINE..
	return filtered_tokens

#NOW MAKE 2 VOCABULARIES, FOR ALL WORDS IN PAGES; ONE STEMMED AND ONE NOT. 
#THEN MAKE PANDA DATAFRAME FOR EFFICIENT WAY TO LOOK UP STEM & RETURN FULL TOKEN
totalvocab_stemmed = []
totalvocab_tokenized = []
for i in recipes:
    allwords_stemmed = stem(i)
    totalvocab_stemmed.extend(allwords_stemmed)
   # print(allwords_stemmed)
    
    allwords_tokenized = justToken(i)
    totalvocab_tokenized.extend(allwords_tokenized)
    #print(allwords_tokenized)

def tokenize_and_stem(text):
	return stem(text.lower().split(" "))

vocab_frame = pd.DataFrame({'words': totalvocab_tokenized}, index = totalvocab_stemmed)
# (stemmed vocab is index, tokenized/orig words as column)
#print(vocab_frame) #debugging

#MAKE TF-IDF MATRIX; THEN USE FOR ALL SORTS OF CLUSTERING FUN
tfidf_vectorizer=TfidfVectorizer(max_df=0.8, #play with how often a word can appear
	max_features=200000, min_df=0.2, 
	stop_words=set(my_stop_words), use_idf=True, 
	tokenizer=tokenize_and_stem, ngram_range=(1,3))
tfidf_matrix=tfidf_vectorizer.fit_transform([' '.join(x) for x in recipes]) #CAN JUST PASS ALL THE FILES; DON'T NEED TO MAKE ALL THE OTHER LISTS!!
print(tfidf_matrix.shape)

terms=tfidf_vectorizer.get_feature_names()
#print(terms) #debugging
dist=1-cosine_similarity(tfidf_matrix)


#NOW ON TO CLUSTERING FOR FUNSIES
cwfile=open('clusterWords','w')
num_clusters=50 #play around w/ this for kmeans
km=KMeans(n_clusters=num_clusters)
km.fit(tfidf_matrix)
clusters=km.labels_.tolist()


recipePages={'title':fTitles,'recipe':recipes,'cluster':clusters}
frame=pd.DataFrame(recipePages, index=[clusters],columns=['title','recipe','cluster'])
print(frame['cluster'].value_counts())

print("top terms per cluster:")
order_centroids=km.cluster_centers_.argsort()[:,::-1]
for i in range(num_clusters):
	print("cluster %d words:" %i, end='')
	print("cluster %d words:" %i, end='',file=cwfile)

	word_ids = order_centroids[i, :6]
	print(word_ids)
	print([terms[i] for i in word_ids])
	for ind in order_centroids[i, :6]: #get top 6 words for each cluster
		print(' %s' % vocab_frame.ix[terms[ind].split(' ')].values.tolist()[0][0].encode('utf-8','ignore'),end=',',file=cwfile)
	print('\n',file=cwfile)
	print('\n')
	print("Cluster %d titles:" % i, end='')
	print("Cluster %d titles:" % i, end='',file=cwfile)
	#print(frame.ix[i])
	#for title in frame.ix[i]['title'].values.tolist():
		#print(' %s,' % title, end='',file=cwfile)
		#print('\n',file=cwfile)

"""
play around with # of clusters; try to print more/all words from a cluster??
also, change max/min_df to try to get different/better results?? run over more recipes too...

Not sure the stemming/stop words is working as it should (some still occasionally show up in clusters)

#HELPFUL SITES:
# https://github.com/brandomr/document_cluster/blob/master/cluster_analysis.ipynb
# http://brandonrose.org/top100
# http://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html#sklearn.feature_extraction.text.TfidfVectorizer.get_feature_names

"""