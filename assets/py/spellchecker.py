#!/usr/bin/env python
from SimpleXMLRPCServer import SimpleXMLRPCServer
import logging
import os
import re
import heapq

# Don McCurdy, Februray 2012
# Run: "nohup ./spellchecker.py &" to keep in the background.

# A few constants: the alphabat, and some arbitrarily assigned weights.
alph = 'abcdefghijklmnopqrstuvwxyz'	
weights = {"remove":0.25, "add":2, "swap":10, "split":5, "replace":8}

# Set up logging
logging.basicConfig(level=logging.DEBUG)
server = SimpleXMLRPCServer(('206.217.131.124', 9000), logRequests=True)

#####BEGIN LIST OF ALLOWED SHORT WORDS#####
#list of short words is blatantly copied from
#Scrabble's official list, with a few additions.
f = open('ShortWords.txt')
shortWords = { }
lines = f.readlines()
for i in lines:
	wordsInLine = re.findall(r'\w+',i)
	for w in wordsInLine:
		w = w.lower()
		shortWords[w] = 1

#####BEGIN CODE TO PARSE MOBY DICK#####
f = open('MobyDick.txt','r');
myDictionary = { }
lines = f.readlines()
for i in lines:
	wordsInLine = re.findall(r'\w+', i) 
	#technically doesn't handle possesives ('s) especially gracefully.
	for w in wordsInLine:
		w = w.strip('1234567890')
		w = w.lower()
		if len(w) == 0:
			continue
		if len(w) < 4:
			if w not in shortWords:	#if the word is short, make sure it's on the list
				continue
		if w not in myDictionary:	#add to dictionary or increment weight
			myDictionary[w] = 1
		else:
			myDictionary[w] += 1

print 'Words in myDictionary after parse: ', len(myDictionary)

	
##### MAIN SPELLCHECK FUNCTION #####	
def spellcheck(word):
	word = word.lower()
	if word in myDictionary:		#return true if word is correct
		return [True,word]
	else:							#if not, try to find similar words that are.
		h = [ ]
		
		addChar(word, h, 2)
		removeChar(word, h, 2)	
		swap(word, h)
		splitWords(word,h)
		replaceChar(word,h,1)
	
		if len(h) == 0:	
			return [ False, 'SERVER_EMPTY_RESPONSE' ]
		else:
			return [ False , heapq.heappop(h)[1] ]


###### REMOVE LETTERS ######
def removeChar(word, h, depth):
	removeCharH(word,h,1,depth)

def removeCharH(word, h, iterNum, depth):
	for i in range(0,len(word)):			#for each letter
		attempt = word[:i] + word[i+1:]		#see if result after removal is a word
		if 	attempt in myDictionary:
			heapq.heappush(h, (iterNum*iterNum*1000000/(len(word)*myDictionary[attempt]*weights['remove']) , attempt))
		if iterNum < depth :				#recursive, if depth > 1
			removeCharH(attempt, h, iterNum+1, depth)

##### ADD LETTERS #####
def addChar (word, h, depth):
	addCharH(word,h,1, depth)

def addCharH (word, h, iterNum, depth):
	for az in range(0,26):					#try adding each letter A-Z
		for i in range (0,len(word)+1):		#at each position in word
			attempt = word[:i] + alph[az] + word[i:]
			if attempt in myDictionary:	
				heapq.heappush(h, (iterNum*iterNum*1000000/(len(word)*myDictionary[attempt]*weights['add']) , attempt))
			if iterNum < depth : 			#recursive, if depth > 1
				addCharH(attempt, h, iterNum+1, depth)

##### REPLACE LETTERS #####
def replaceChar (word, h, depth):
	replaceCharH(word,h,1,depth)

def replaceCharH (word, h, iterNum, depth):
	for i in range (0, len(word)):			#try replacing each letter
		for az in range(0,26):				#with every other possible letter
			attempt = word[:i] + alph[az] + word[i+1:]
			if attempt in myDictionary:	
				heapq.heappush(h, (iterNum*iterNum*1000000/(myDictionary[attempt]*weights['replace']) , attempt))
			if iterNum < depth :
				replaceCharH(attempt, h, iterNum+1, depth)

##### SWAP TWO CONSECUTIVE LETTERS #####			
def swap (word, h):
	if len(word) is not 1:
		for i in range(0, len(word)-1):		
			attempt = word[:i] + word[i+1] + word[i] + word[i+2:] #swap letters i and i+1
			if 	attempt in myDictionary:
				heapq.heappush(h, (1000000/(myDictionary[attempt]*weights['swap']) , attempt))

##### SPLIT INTO TWO WORDS #####
def splitWords (word, h):
	if len(word) is not 1:
		for i in range(1, len(word)-1):		#try splitting word at each possible location
			if word[:i] in myDictionary and word[i:] in myDictionary:
				heapq.heappush(h, (1000000/((myDictionary[word[:i]] + myDictionary[word[i:]])*weights['split']), word[:i] + " " + word[i:]))

			

server.register_function(spellcheck)

try:
	print 'Spellcheck server running on port 9000.'
	server.serve_forever()
except KeyboardInterrupt:
    print 'Exiting.'
