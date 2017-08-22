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
import matplotlib.pyplot as plt
import numpy as np
import scipy.interpolate
import math
import cv2

class Ant( ):
    def __init__( self, id, x=0, y=0, t=0 ):
        self.id = id 
        self.x = x
        self.y = y
        self.t = t
        self.angle = 0


def spline_fit( path ):
    tck, u = scipy.interpolate.splprep( zip(*path), s=0.0 )
    xi, yi = scipy.interpolate.splev( np.linspace(0,1,500), tck )
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

def distance( p1, p2 ):
    return ((p1[0] - p2[0]) ** 2.0 + (p1[1] - p2[1])**2 ) ** 0.5

def angle( p1, p2 ):
    return math.atan2( ( p2[1] - p1[1] ), float( p2[0] - p1[0] ) )

def show_img( img ):
    cv2.imshow( "grid", img )
    cv2.waitKey( 100 )

def show_path( path, img, weight = 1 ):
    cv2.polylines( img, [ path ], False, weight, 1 )

def pixalsWithPheromone( a ):
    global grid_
    pixals, amount = [ ], [ ]
    p = a.x, a.y
    for i in [-1, 1]:
        for j in [-1, 1]:
            x = p[0] + i
            y = p[0] + j
            if grid_[ x, y ] > 0:
                pixals.append( (x, y) )
                amount.append( grid_[ x, y ] )
    return pixals, amount

def scanAndChooseDirection( ant ):
    global grid_
    p = ant.x, ant.y 
    w = grid_[ p ]
    direction, pheromone = [ ], [ ]
    for dtheta in range( -30, 30, 5 ):
        # Scan next 5 points in this direction 
        totalP = grid_[ p ]
        theta = ant.angle + (math.pi * dtheta / 180.0 )
        for i in range( 5 ):
            x = int( ant.x + 4 * math.cos( theta ))
            y = int( ant.y + 4 * math.sin( theta ))
            if (x, y) != p and grid_[x, y] > w:
                totalP += grid_[ x, y ]
        direction.append( theta )
        pheromone.append( totalP )
    pick = np.random.choice( direction, 1, p = pheromone / np.sum( pheromone ) )
    return pick[0]


def updateAnts(  ):
    global ants_
    global grid_
    for a in ants_:
        # Sense which path and walk.
        p = a.x, a.y
        points, pheromone = pixalsWithPheromone( a )
        # Select the point with the probability proportional to pheromone
        if points:
            # Scan in neighbouring direction and select the best direction to
            # move ahead.
            directionToTake = scanAndChooseDirection( a )
            a.angle = directionToTake
            print( 'Dir', directionToTake )
        else:
            # This ant is stuck
            pass

def show_ants( length = 20 ):
    global grid_
    global ants_
    img = np.copy( grid_ )
    for a in ants_:
        p1 = a.x, a.y
        p2 = a.x + int(length * math.cos( a.angle)), a.y + int(length * math.sin( a.angle))
        cv2.arrowedLine( img, p1, p2, 255, 2 )
    show_img( img )

def simulate( steps ):
    print( 'Simulating for %d steps ' % steps )
    for i in range( steps ):
        print( 'Step %d is done' % i )
        updateAnts( )
        show_ants(  )

def main( ):
    global grid_
    show_path( p1_, grid_ )
    show_path( p2_, grid_ )
    show_path( p3_, grid_ )
    show_img( grid_ )
    simulate( 1000 )

if __name__ == '__main__':
    main()
