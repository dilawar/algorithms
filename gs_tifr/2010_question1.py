#!/usr/bin/env python

# Filename       : 2010_question1.py 
# Created on     : 2013-09-24
# Author         : Dilawar Singh
# Email          : dilawars@ncbs.res.in
#
# Description    :
#
# Logs           :

import random 

def singleStep() :
  balls = []
  for black in range(0, 731) :
    balls.append("b")

  for white in range(0, 2000) :
    balls.append("w")


  while len(balls) > 1 :
    random.shuffle(balls)
    firstBall = balls.pop()
    secondBall = balls.pop()
    if firstBall == secondBall :
      balls.append("b")
    else :
      balls.append("w")

  print("what is left : {0}".format(balls))


if __name__ == "__main__" :
  for i in range(0, 10) :
    singleStep()
