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
import soundfile

rate_, data_ = 0, []

def process( ):
    global rate_, data_
    data_ = data_[::2]
    T = 1.0 / rate_
    #  data_ = np.abs( data_ )
    tvec = np.arange(0, len(data_)) * T
    f, t, Sxx = scipy.signal.spectrogram( data_, rate_ )
    plt.subplot( 211 )
    plt.plot( tvec, data_ )
    plt.xlabel( 'Time (sec)' )
    plt.subplot( 212 )
    plt.pcolormesh( t, f, Sxx)
    plt.savefig( 'summary.png' )

def main():
    global rate_, data_
    global freq_
    filename = sys.argv[1]
    data_, rate_ = soundfile.read( filename )
    assert len(data_) > 0
    process()


if __name__ == '__main__':
    main()

