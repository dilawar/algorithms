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
import curses

words = []
stdscr = curses.initscr()
yMax, xMax = stdscr.getmaxyx()
mainWin = curses.newwin(4, 40, 0, 0)
msgWinYOffset = 5
msgWin = curses.newwin(xMax- msgWinYOffset, 40, msgWinYOffset, 0)
tries = 0

def initWindow() :
  global stdscr
  global mainWin, msgWin
  curses.noecho()
  stdscr.keypad(1)
  curses.cbreak()
  # intialize a window 
  refreshBoxedWindow(mainWin)
  refreshBoxedWindow(msgWin)
  

def populateDB(wordLength) :
  global words 
  with open("words") as f :
    allwords = f.read().split()
  for w in allwords :
    if len(w) == wordLength :
      words.append(w)

def refreshBoxedWindow(window) :
  window.box()
  window.refresh()

def putString(xloc, yloc, msg, window, overWrite=False) :
  if not overWrite :
    y , x = window.getyx()
    window.addstr(y+1, 1,  msg)
  else :
    window.addstr(xloc+1, yloc+1, msg)
  refreshBoxedWindow(window)

def printError(msg) :
  global stdscr 
  ymax, xmax = stdscr.getmaxyx()
  width, height = 40, 4
  assert(ymax - height > 0)
  assert(xmax - width > 0) 
  errorWin = curses.newwin(height, width,  0, 0)
  errorWin.box()
  errorWin.refresh()
  putString(0, 0, msg, errorWin, True)
  errorWin.getch()
  del errorWin
  stdscr.refresh()

def cowsAndBull(word, correctWord) :
  # bulls are no of letters on the same position in both words.
  global msgWin
  global mainWin 
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
  msg = " {2} has {0} bulls, {1} cows".format(bulls, len(cows), word)
  putString(1, 3, msg, msgWin)
  
  

if __name__ == "__main__" :
  initWindow()
  wordWidth = 4
  populateDB(wordWidth)
  # randomly select one word.
  chosenWord = choice(words)
  myWord = ''
  
  while(chosenWord != myWord) :
    if(myWord != "????") :
      inputMsg = "Guess, you puny human : "
      putString(0, 0, inputMsg, mainWin, True)
      msgWin.refresh()
      curses.echo()
      myWord = mainWin.getstr(1, len(inputMsg)) 
      myWord = myWord.strip()
      if(len(myWord) != wordWidth) :
        printError("ERROR: Not a {0} letter word. Try again.".format(wordWidth))
        continue
      if myWord in words :
        cowsAndBull(myWord, chosenWord)
      else :
        printError("This is not a valid word. Guess again.")
    else :
      printError("The word is : {0}".format(chosenWord))
      curses.endwin()
      sys.exit()
  printError("Congrats! This was the correct word")
  curses.endwin()
  
