#script to alphabetize cook/measureWords.txt
#kinda works, is a bit rough and needs some manual work to format nicely in text file (after writing list to file)

from __future__ import print_function #need this to print to file
import string #need for testing if punctuation in word

with open('measurements.txt','r+') as f:
	for line in f:
		line=line.strip() #strip newlines/blanks at beg/end of line
		if not line:
			continue #skip blank lines in file
		if line.startswith('#'):
			continue #skip comments in file
		measure=[line.rstrip('\n') for line in f]
	measure.sort()
	print(measure, file=f)