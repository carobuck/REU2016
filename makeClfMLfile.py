from __future__ import print_function #need this to print to file

outf=open('MLfile_indianMealBk2','w') #open file for machine learning output
with open('extract_indianMealBk2') as f:
	for line in f:
	 	#strip() gets rid of newlines (on right and left)
		arr=line.strip().split('\t')
		#print(arr)
		featureStr='1' #for load_svmlight_file to work, need something here (just store in ytrash in scikit.py, so ignore it)
		for i in range(len(arr[1:])): #len is getting # of features
			featureStr+=' '+str(i+1)+':'+arr[i+1] #add all features to featureStr with proper formatting
		featureStr+='#'+arr[0]
		print(featureStr,file=outf) #print feature string to output file
outf.close()
