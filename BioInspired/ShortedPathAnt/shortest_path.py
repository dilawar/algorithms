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
import Ant
from environment import grid_


PI = math.pi

def spline_fit( path ):
    nPoints = 4 * int( Ant.distance( path[0], path[-1] ))
    tck, u = scipy.interpolate.splprep( zip(*path), s=0.0 )
    xi, yi = scipy.interpolate.splev( np.linspace(0,1,nPoints), tck )
    pts = np.array( zip( xi, yi ), np.int32 )
    return pts

x = 300
colony_ = (x,x)
source_ = map(lambda a: a - x, grid_.shape) 


pp1_ = [ colony_, (200,200), (300,150), (500,100), (800, 200), (850,400), source_ ]
pp2_ = [ colony_, (400,400), (550,800), source_ ]
pp3_ = [ colony_, (400,800), (800,800), source_ ]

p1_ = spline_fit( pp1_ )
p2_ = spline_fit( pp2_ )
p3_ = spline_fit( pp3_ )
paths_ = [ p1_, p2_, p3_ ]

# Initially all ants are colony
ants_ = [ Ant.Ant(i, x=colony_[0], y=colony_[1]) for i in range( 10000 ) ]

def show_img( img ):
    cv2.imshow( "grid", img )
    cv2.waitKey( 10 )

def show_path( path, img, weight = 1 ):
    cv2.polylines( img, [path], False, weight, 1)

def updateAnts(  ):
    global ants_
    # Scan in neighbouring direction and select the best direction to
    [ a.scanAndMove( ) for a in ants_ ]

def show_ants( length = 5 ):
    global grid_
    global ants_
    img = np.copy( grid_ )
    for a in ants_:
        draw_ant( a, img, length )
    show_img( img )

def draw_ant( a, img, length = 5 ):
    # OpenCV works in 4th quadrant
    p1 = a.x, a.y
    p2 = a.x + int(length * math.cos( a.angle)), a.y - int(length * math.sin( a.angle))
    cv2.arrowedLine( img, (p2[1], p2[0]), (p1[1], p1[0]), 255, 2 )

def simulate(  ):
    while True:
        updateAnts( )
        show_ants(  )


def test( ):
    a = Ant.Ant( 0, x = 200, y = 100 )
    b = Ant.Ant( 0, x = 100, y = 200 )
    while True:
        a.angle = 0
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
    #  test( )

if __name__ == '__main__':
    main()
