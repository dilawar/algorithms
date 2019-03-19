#!/usr/bin/env python
from __future__ import division
"""main.py: 

"""
    
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2017-, Dilawar Singh"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"
__status__           = "Development"

import sys
sys.path.append( '../image_analysis')
import os
import numpy as np
import frame_reader as fr
import contour_detector as cd
import cv2

def show_frame(f, wait=200):
    cv2.imshow("frame", f)
    cv2.waitKey(wait)

def process(filename):
    fs = fr.read_frames(filename)
    kernel = np.ones((3,3), np.uint8)
    for f in fs:
        f = cv2.resize(f, None, fx=0.4, fy=0.4)
        f = cv2.equalizeHist(f)
        f1 = f.copy()
        #  f = cv2.medianBlur(f, 3)
        #  cnts = cd.contours(f)
        #  cv2.drawContours(f, cnts, -1, 255)
        f[f < f.max()-10] = 0
        f = cv2.morphologyEx(f, cv2.MORPH_OPEN, kernel)
        show_frame(f)


def main():
    process(sys.argv[1])

if __name__ == '__main__':
    main()

