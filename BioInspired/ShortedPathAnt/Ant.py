"""Ant.py: 

"""
    
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2017-, Dilawar Singh"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"
__status__           = "Development"

import sys
import random
import cv2
import numpy as np
import os
import math
from environment import grid_

PI = math.pi

def distance( p1, p2 ):
    return ((p1[0] - p2[0]) ** 2.0 + (p1[1] - p2[1])**2 ) ** 0.5

def angle( p1, p2 ):
    t = math.atan2( ( p2[1] - p1[1] ), float( p2[0] - p1[0] ) )
    if t < 0:
        t = PI - t
    return t

class Ant( ):
    def __init__( self, id, x=0, y=0, t=0 ):
        self.id = id 
        self.x = x
        self.y = y
        self.t = t
        self.prevX, self.prevY = 0, 0
        self.angle = random.random( ) * 2 * PI

    def updatePos( self, point ):
        x, y = point
        self.prevX, self.prevY = self.x, self.y
        self.x, self.y = x, y
        self.angle = angle( (x,y), (self.prevX, self.prevY ) )

    def __repr__( self ):
        return '%d, %d, %f' % (self.x, self.y, self.angle)

    def sensePixals( self ):
        global grid_
        p0 = self.x, self.y
        # next pixal to take.
        px, wx = [ ], [ ]
        for i in range(-1, 1):
            for j in range(-1,1):
                x, y = self.x + i, self.y + j
                if (x,y) == p0:
                    continue
                if grid_[x, y ] > 0:
                    px.append((x,y))
                    wx.append( grid_[x,y] )
        # if no pixal found with pheromone, continue in random direction.
        if not px:
            px.append( (self.x + random.randint(1, 5), self.y + random.randint(1,5) ) )
            wx.append( 1 )

        return px, wx

    def chooseNextPoint( self, pixals, weights ):
        toselect, cost = [ ], [ ]
        for i, p in enumerate( pixals ):
            theta = abs( angle( (self.x, self.y), p ) - self.angle )
            turn = math.sin( theta / 4.0 )             # max at 0, min at 2pi
            w = weights[ i ]
            if turn > 0.3:
                cost.append( w * turn )
            else:
                cost.append( 1e-6)
            toselect.append( p )

        probs = map( lambda x: x / sum( cost ), cost )
        i = np.random.choice( range(len(toselect)), 1, p = probs )[0]
        return pixals[i]

    def scanAndMove( self ):
        global grid_
        pixals, weights = self.sensePixals(  )
        point = self.chooseNextPoint( pixals, weights )
        # Add some pheromone 
        grid_[ self.x, self.y ] += 1
        self.updatePos( point )

