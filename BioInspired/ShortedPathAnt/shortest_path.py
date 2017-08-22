"""shortest_path.py: 

"""
    
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2017-, Dilawar Singh"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"
__status__           = "Development"

import sys
import os
import random
import matplotlib.pyplot as plt
import numpy as np
import scipy.interpolate
import math
import cv2

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

def spline_fit( path ):
    nPoints = 4 * int( distance( path[0], path[-1] ))
    tck, u = scipy.interpolate.splprep( zip(*path), s=0.0 )
    xi, yi = scipy.interpolate.splev( np.linspace(0,1,nPoints), tck )
    pts = np.array( zip( xi, yi ), np.int32 )
    return pts

N = 1000
grid_ = np.zeros( shape=(N,N) )
x = 300
colony_ = (x,x)
source_ = (N-x,N-x)

# Initially all ants are colony
ants_ = [ Ant(i, x=colony_[0], y=colony_[1]) for i in range( 1 ) ]
speed_ = 5                                  # au per au time.

#grid_ = cv2.circle( grid_, colony_, 5, 255, 2 )
#grid_ = cv2.circle( grid_, source_, 5, 255, 2 )

pp1_ = [ colony_, (200,200), (300,150), (500,100), (800, 200), (850,400), source_ ]
pp2_ = [ colony_, (400,400), (550,800), source_ ]
pp3_ = [ colony_, (400,800), (800,800), source_ ]

p1_ = spline_fit( pp1_ )
p2_ = spline_fit( pp2_ )
p3_ = spline_fit( pp3_ )
paths_ = [ p1_, p2_, p3_ ]

def show_img( img ):
    cv2.imshow( "grid", img )
    cv2.waitKey( 10 )

def show_path( path, img, weight = 1 ):
    cv2.polylines( img, [path], False, weight, 2)

def sensePixals( a ):
    global grid_
    p0 = a.x, a.y
    # next pixal to take.
    px, wx = [ ], [ ]
    for i in range(-1, 1):
        for j in range(-1,1):
            x, y = a.x + i, a.y + j
            if (x,y) == p0:
                continue
            if grid_[x, y ] > 0:
                px.append((x,y))
                wx.append( grid_[x,y] )

    # if no pixal found with pheromone, continue in random direction.
    if not px:
        px.append( (a.x + random.randint(1, 5), a.y + random.randint(1,5) ) )
        wx.append( 1 )

    return px, wx

def chooseNextPoint( a, pixals, weights ):
    toselect, cost = [ ], [ ]
    for i, p in enumerate( pixals ):
        theta = abs( angle( (a.x, a.y), p ) - a.angle )
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

def scanAndMove( a ):
    global grid_
    pixals, weights = sensePixals( a )
    point = chooseNextPoint( a, pixals, weights )
    # Add some pheromone 
    grid_[ a.x, a.y ] += 10
    a.updatePos( point )

def updateAnts(  ):
    global ants_
    # Scan in neighbouring direction and select the best direction to
    [ scanAndMove( a ) for a in ants_ ]

def show_ants( length = 20 ):
    global grid_
    global ants_
    img = np.copy( grid_ )
    for a in ants_:
        draw_ant( a, img, length )
    show_img( img )

def draw_ant( a, img, length = 10 ):
    # OpenCV works in 4th quadrant
    p1 = a.x, a.y
    p2 = a.x + int(length * math.cos( a.angle)), a.y - int(length * math.sin( a.angle))
    cv2.arrowedLine( img, p1, p2, 255, 1 )

def simulate(  ):
    while True:
        updateAnts( )
        show_ants(  )


def test( ):
    while True:
        a = Ant( 0, x = 200, y = 100 )
        a.angle = PI / 2.0

        b = Ant( 0, x = 100, y = 200 )
        b.angle = PI / 3.0
        show_img( grid_ )

        draw_ant( a, grid_  )
        draw_ant( b, grid_  )
        show_img( grid_ )

def main( ):
    global grid_
    show_path( p1_, grid_ )
    show_path( p2_, grid_ )
    show_path( p3_, grid_ )
    simulate( )
    # test( )

if __name__ == '__main__':
    main()
