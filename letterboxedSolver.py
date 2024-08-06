import random
from copy import copy

words = open("words small.txt").readlines()
for i in range(len(words)):
	words[i] = words[i][:-1].lower()
board = ["nai","row","ued","gfb"]

print("__________________________________________")
print()

print("Board to check: ",end="")
print(board)
print()

def getValidWords(board):
	global words
	validWords = []
	for word in words:
		valid = True
		#print("checking word "+word)
		for letterindex in range(len(word)):
			currentLetter = word[letterindex]
			#print("checking letter "+str(currentLetter))
			onBoard = False
			for sideindex in range(len(board)):
				if currentLetter in board[sideindex]:
					onBoard = True
					side = sideindex
					#print(str(currentLetter) +" was found on board in row "+board[sideindex])
			if not onBoard:
				valid = False
				break
			else:
				if letterindex != 0:
					beforeindex = letterindex - 1
					for sideindex in range(len(board)):
						if word[beforeindex] in board[sideindex]:
							onBoard = True
							beforeside = sideindex
					if beforeside == side:
						valid = False
						break
		if valid and (len(word) > 2):
			validWords.append(word)
			#print(word+" is valid on board")
		#else:
		#print(word+" not valid because of letter "+currentLetter)
	return validWords


validWords = getValidWords(board)
validWords.sort(key=len)

tempLength = len(validWords)
iter = 0
while iter < tempLength:
	if len(validWords[iter]) < 4:
		del validWords[iter]
		tempLength -= 1
	iter += 1

print(str(len(validWords)) + " possible words found on this board!")
print()

def treeConv(tree):
	output = ""
	for word in tree:
		output += word
	return output


def findNextWords(tree, validWords):  # should be done
	validnextwords = []
	for word in validWords:
		if word[0] == tree[-1][-1]:
			validnextwords.append(word)
	return validnextwords


def checkTree(tree, lettersOnBoardV):  # should be done
	#print(tree)
	lettersOnBoardL = ""
	lettersOnBoardVTemp = copy(lettersOnBoardV)
	for side in board:
		lettersOnBoardL += side
	for letter in treeConv(tree):
		if letter in lettersOnBoardL:
			lettersOnBoardVTemp[letter] = True
	#print(lettersOnBoardL)
	#print(lettersOnBoardV)
	return all(lettersOnBoardVTemp.values())

# MEMORY INTENSIVE METHOD - do not care about anything else at this point - a list of a billion things? sure

def addLayer(trees,validWords): # STORES ALL NEW POSSIBLE TREES FROM OLD POSSIBLE TREES - FUCK YOUR RAM
	newtrees = []
	for tree in trees:
		nextValidWords = findNextWords(tree,validWords)
		for word in nextValidWords:
			temptree = copy(tree)
			temptree.append(word)
			newtrees.append(temptree)
	return newtrees

def genBoardCheck(board):
	lettersOnBoardV = {}
	for side in board:
		for letter in side:
			lettersOnBoardV[letter] = False
	return lettersOnBoardV

def checkLayer(layer,board): # checks entire layer, adds tree to validTrees if it is valid
	validTrees = []
	for tree in layer:
		if checkTree(tree,board):
			validTrees.append(tree)
	return validTrees

def findTreesDepth(validWords,depth,board):
	curLayer = 0
	trees = []
	for word in validWords:
		trees.append([word]) # turning validWords into valid trees (lists instead of strings)

	lettersOnBoardV = genBoardCheck(board)
	print("generating layer 1...")
	solutions = []
	while curLayer != depth:
		print(str(len(trees)) + " trees to check...")
		solutions.append(checkLayer(trees,lettersOnBoardV)) # adding valid solutions
		print(str(len(solutions[curLayer]))+" solutions found on this layer")
		print()
		curLayer += 1
		if curLayer == depth:
			break
		print("generating layer " +str(curLayer+1)+"...")
		trees = addLayer(trees,validWords) # expanding the trees 1 level deeper
	return solutions
		
results = findTreesDepth(validWords,2,board)
input("see results?")
print(results)