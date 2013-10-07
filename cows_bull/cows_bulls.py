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

curses.start_color()

curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
headerWin = curses.newwin(4, 40, 0, 0)
headerWin.box()
headerWin.addstr(0, 2, "  Cows and bulls!")
headerWin.addstr(1, 2, "  Type ???? to ruin the fun", curses.color_pair(1))
headerWin.addstr(2, 2, "  Type xxxx to exit", curses.color_pair(1))
headerWin.refresh()

yMax, xMax = stdscr.getmaxyx()
mainWin = curses.newwin(4, 40, 3, 0)
msgWinYOffset = 6
msgWin = curses.newwin(yMax- msgWinYOffset , 40, msgWinYOffset, 0)
width, height = 40, 4
errorWin = curses.newwin(height, width,  3, 0)
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
      if '\'' not in w :
        words.append(w.lower())

def refreshBoxedWindow(window) :
  window.box()
  window.refresh()

def putString(xloc, yloc, msg, window, overWrite=False) :
  if not overWrite :
    y , x = window.getyx()
    window.addstr(y+1, 1,  msg)
  else :
    window.addstr(xloc+1, yloc+1, msg)
    window.clrtobot()
  refreshBoxedWindow(window)

def printError(msg) :
  global stdscr 
  global mainWin, msgWin
  ymax, xmax = stdscr.getmaxyx()
  assert(ymax - height > 0)
  assert(xmax - width > 0) 
  errorWin.box()
  errorWin.refresh()
  putString(0, 0, msg+". Press a key to continue", errorWin, True)
  errorWin.refresh()
  errorWin.getch()

def cowsAndBull(word, correctWord) :
  # bulls are no of letters on the same position in both words.
  global msgWin
  global mainWin 
  global tries 
  bullsChars = []
  bulls = 0
  cows = 0
  for i in range(0, len(word)-1) :
    if word[i] == correctWord[i] :
      bulls += 1
      bullsChars.append(word[i])
    else : pass 
  setA = set(word)
  setB = set(correctWord)
  cowsSet = setA.intersection(setB)
  for c in cowsSet :
    if c in bullsChars : pass 
    else : cows += 1
  msg = " {2} : {0} bulls, {1} cows".format(bulls, cows, word)
  putString(len(word), len(word), msg, msgWin)
  
  

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
      curses.echo()
      stdscr.touchwin()
      msgWin.refresh()
      mainWin.refresh()
      myWord = mainWin.getstr(1, len(inputMsg)) 
      myWord = myWord.strip()
      if(len(myWord) != wordWidth) :
        printError("ERROR: Not a {0} letter word. Try again.".format(wordWidth))
        continue
      if myWord in words :
        cowsAndBull(myWord, chosenWord)
      elif myWord == "xxxx" :
        curses.endwin()
        sys.exit()
      elif myWord != "????" :
        printError("This is not a valid word. Guess again.")
        continue
      else : continue 
    else :
      printError("The word is : {0}".format(chosenWord))
      curses.endwin()
      sys.exit()
  printError("Congrats! This was the correct word")
  curses.endwin()
  
