#!/usr/bin/env python

# Filename       : cows_bulls.py 
# Created on     : 2013-10-06
# Author         : Dilawar Singh
# Email          : dilawars@ncbs.res.in
#
# Description    : A kind of game.
#
# Logs           :


import sys
import cmd
from random import choice

words = []

def populateDB(wordLength) :
  global words 
  with open("words") as f :
    allwords = f.read().split()
  for w in allwords :
    if len(w) == wordLength :
      words.append(w)

def cowsAndBull(word, correctWord) :
  # bulls are no of letters on the same position in both words.
  wordA = word
  wordB = correctWord
  assert len(wordA) == len(wordB)
  bulls = 0
  cows = 0
  for i in range(0, len(wordA)-1) :
    if wordA[i] == wordB[i] :
      bulls += 1
      if len(wordA) != i-1 :
        wordA = wordA[:i] + wordA[i+1:]
        wordB = wordB[:i] + wordB[i+1:]
      else :
        wordA = wordA[:-1]
        wordA = wordB[:-1]
    else : pass 
  setA = set(wordA)
  setB = set(wordB)
  cows = setA.intersection(setB)
  print("{2} has {0} bulls, {1} cows".format(bulls, len(cows), word))
  

if __name__ == "__main__" :
  wordWidth = 4
  populateDB(wordWidth)
  # randomly select one word.
  chosenWord = choice(words)
  myWord = ''
  while(chosenWord != myWord) :
    if(myWord != "????") :
      myWord = raw_input("Guess a word : ")
      myWord = myWord.strip()
      if(len(myWord) != wordWidth) :
        print("ERROR: Not a {0} letter word. Try again.".format(wordWidth))
        continue
      if myWord in words :
        cowsAndBull(myWord, chosenWord)
      else :
        print("This is not a valid word. Guess again.")
    else :
      print("The word is : {0}".format(chosenWord))
      sys.exit()
  print("Congrats! This was the correct word")
  
