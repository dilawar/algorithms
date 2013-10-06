#!/usr/bin/env python

# Filename       : cows_bulls.py 
# Created on     : 2013-10-06
# Author         : Dilawar Singh
# Email          : dilawars@ncbs.res.in
#
# Description    : A kind of game.
#
# Logs           :


import os 
import sys
from random import choice

words = []

def populateDB() :
  global words 
  with open("./sgb-words.txt") as f :
    words = f.read().split()

def cowsAndBull(word, correctWord) :
  # bulls are no of letters on the same position in both words.
  wordA = word
  wordB = correctWord
  assert len(wordA) == len(wordB)
  bulls = 0
  cows = 0
  for i in range(0, len(wordA)-1) :
    print i
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
  return bulls, cows 
  

if __name__ == "__main__" :
  populateDB()
  # randomly select one word.
  chosenWord = choice(words)
  guessedWords = ''
  while(chosenWord != guessedWords) :
    fiveLetterWord = raw_input("Guess a word : ")
    fiveLetterWord = fiveLetterWord.strip()
    while(len(fiveLetterWord) != 5) :
      print("ERROR: Not a five letter word. Try again.")
      fiveLetterWord = raw_input("Guess a word : ")
      fiveLetterWord = fiveLetterWord.strip()
    print cowsAndBull(fiveLetterWord, chosenWord)
