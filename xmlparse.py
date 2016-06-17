#THIS IS OLDER/ROUGHER COPY OF SOME FEATURE FUNCTIONS (EXTRACT_BOOK2 HAS ALL THE THINGS)


import xml.etree.ElementTree as ET
import string #need for testing if punctuation in word

#this one commented out b/c is really big book; takes long time to run
#tree=ET.parse('betterfruit09wash_djvu.xml') #this line parses the xml file and makes it into a big tree
tree=ET.parse('foodNewsletter.xml') #line to parse file
#print type(tree)

#do I need this line?
root=tree.getroot() #gets root of tree and names it 'root'

pages=tree.findall(".//OBJECT") #this makes a list with all of the pages in the book (128 pages,0-127)
#print type(pages)
#print len(pages)



def moreThan10(page):
	pg=page.findall(".//WORD")
	if len(pg)==0: 
		return 0 #blank page, return 0
	else:
		alphaWord=0
		for tag in pg:
			word=tag.text
			if word.isalpha():
				alphaWord+=1
		if alphaWord>10:
			print('1')
		else:
			print('0')	

for p in pages:
	moreThan10(p)

#****WRITING DIG/PUNC AS FUNC
def numDigits(a):
	digPunc=0
	pg=pages[a].findall(".//WORD")
	for tag in pg:
		word=tag.text
		num=False
		punc=False
		if word.isdigit():
			print word
			digPunc+=1
		else:
			for c in word:
				if c in string.punctuation:
					punc=True
				if c.isdigit():
					num=True
			if punc and num:
				digPunc+=1
				print word
	return digPunc

print numDigits(33)

def numDigitsBad(a): #doesn't work
	digPunc=0
	pg=pages[a].findall(".//WORD")
	for i in range(len(pg)):
		word=pg[i].text
		num=False
		punc=False
		if word.isdigit():
			digPunc+=1
		for c in word:
			if c in string.punctuation:
				punc=True
			if c in string.digits:
				num=True
			if punc and num:
				digPunc+=1
	return digPunc

print numDigitsBad(34)

def tryDig(a): #don't work
	digPunc=0
	#ET.dump(pages[a])
	pg=pages[a]
	for i in range(len(pg)):
		canPrint=False
		notJustLetter=False
		word=pg[i].text
		#print(word)
		if word in string.printable:
			canPrint=True
		if not word in string.letters:
			notJustLetter=True
		if canPrint and notJustLetter:
			digPunc+=1
	return digPunc

print tryDig(34) 

def moreThan10(page):
	pg=page.findall(".//WORD")
	if len(pg)==0: 
		return 0 #blank page, return 0
	else:
		alphaWord=0
		for tag in pg:
			word=tag.text
			if word.isalpha():
				alphaWord+=1
		if alphaWord>10:
			return 1
		else:
			return 0	




#TO INDENT NICELY: DOWNLOAD XML FILE, PUT IN FOLDER ON FLASHDRIVE, DRAG AND DROP INTO SUBLIME,
# THEN CTRL K F 

#test punc func (WORKS)
def punct(a):
	punc=0
	pg=pages[a].findall(".//WORD")
	for i in range(len(pg)):
		for c in pg[i].text:
			if c in string.punctuation:
				punc+=1
	return float(punc)/len(pg)

print punct(31),punct(33),punct(34),punct(35),punct(42),punct(43),punct(51)

#function for # of words on a page
def numWords(a):
	pg=pages[a].findall(".//WORD")
	return len(pg)

print numWords(31),numWords(33),numWords(34),numWords(35),numWords(42), numWords(43),numWords(51)



#COUNT NUMBER OF WORDS ON PAGE; just loop up to range(len(pages))
for i in range(10): #use for loop so don't have to do all 128 pages
	pg1=pages[i].findall(".//WORD") #finds # of words on a page
	print i,len(pg1)

#playing with page 34 of book (lots of words, is ex of prose; pg about textured veg protein products)
pg34=pages[34].findall(".//WORD")
