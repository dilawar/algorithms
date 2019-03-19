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
    newFs = []
    for f in fs:
        f = cv2.resize(f, None, fx=0.4, fy=0.4)
        f = cv2.equalizeHist(f)
        f1 = f.copy()
        #  f = cv2.medianBlur(f, 3)
        #  cnts = cd.contours(f)
        #  cv2.drawContours(f, cnts, -1, 255)
        f[f < f.max()-10] = 0
        f = cv2.morphologyEx(f, cv2.MORPH_OPEN, kernel)
        #  show_frame(f)
        newFs.append(f)

    # params for ShiTomasi corner detection
    feature_params = dict( maxCorners = 100,
            qualityLevel = 0.3,
            minDistance = 7,
            blockSize = 7 )
    # Parameters for lucas kanade optical flow
    lk_params = dict( winSize  = (15,15),
            maxLevel = 2,
            criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
    p0 = cv2.goodFeaturesToTrack(newFs[0], mask = None, **feature_params)

    # Create a mask image for drawing purposes
    mask = np.zeros_like(newFs[0])

    # Create some random colors
    color = np.random.randint(0,255,(100,3))

    for fo, fn in zip(newFs, newFs[1:]):
        # calculate optical flow
        p1, st, err = cv2.calcOpticalFlowPyrLK(fo, fn, p0, None, **lk_params)
        # Select good points
        good_new = p1[st==1]
        good_old = p0[st==1]
        # draw the tracks
        for i,(new,old) in enumerate(zip(good_new,good_old)):
            a,b = new.ravel()
            c,d = old.ravel()
            cv2.line(mask, (a,b),(c,d), color[i].tolist(), 2)
            cv2.circle(fn,(a,b),5,color[i].tolist(),-1)

        fn = cv2.add(fn, mask)

        show_frame(fn)
        # Now update the previous frame and previous points
        fo = fn.copy()
        p0 = good_new.reshape(-1,1,2)

def main():
    process(sys.argv[1])

if __name__ == '__main__':
    main()

