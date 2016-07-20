
outf=open('MLfileRecipe_train_Wcluster','w')
outf2=open('testML_cluster','w')

with open('MLfile_cluster_truth') as f:#open file for machine learning output
	for idx, line in enumerate(f):
		if idx%2==0: #want every third line in
			print(line) 
			print(line,file=outf2)
		else:
			print("blah")
			print(line,file=outf)


outf.close()
outf2.close()
