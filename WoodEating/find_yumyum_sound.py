#!/usr/bin/env python
"""find_yumyum_sound.py: 

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
import scipy.io.wavfile
import scipy.signal
import scipy

rate_, data_ = 0, []

def spectrogram( X ):
    window_size = 2048          # 2048-sample fourier windows
    stride = 512                # 512 samples between windows
    wps = rate_/float(512) 
    Xs = np.empty([int(10*wps),2048])
    for i in range(Xs.shape[0]):
        Xs[i] = np.abs(scipy.fft(X[i*stride:i*stride+window_size]))
    return Xs

def process( ):
    global rate_, data_
    T = 1.0 / rate_
    tvec = np.arange(0, len(data_)) * T
    f, t, Sxx = scipy.signal.spectrogram( data_, fs=rate_)
    plt.subplot( 211 )
    plt.plot( tvec, data_ )
    plt.xlabel( 'Time (sec)' )
    plt.subplot( 212 )
    Xs = spectrogram( data_ )
    plt.imshow( Xs.T[0:150], interpolation = 'none', aspect = 'auto' )
    plt.savefig( 'summary.png' )

def main():
    global rate_, data_
    global freq_
    filename = sys.argv[1]
    #  data_, rate_ = soundfile.read( filename )
    rate_, data_ = scipy.io.wavfile.read( filename )
    assert len(data_) > 0
    process()


if __name__ == '__main__':
    main()

