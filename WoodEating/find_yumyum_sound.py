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
import numpy as np
import scipy.io.wavfile
import scipy.signal
import scipy
import cv2
import matplotlib as mpl
import matplotlib.pyplot as plt
mpl.style.use( 'bmh' )
mpl.rcParams['text.usetex'] = True


rate_, data_ = 0, []
window_size_ = 2048

def spectrogram_manual( X ):
    global window_size_
    stride = 512                
    wps = rate_//stride
    Xs = np.empty([int(10*wps), window_size_])
    for i in range(Xs.shape[0]):
        Xs[i] = np.abs(np.fft.fft(X[i*stride:i*stride+window_size_]))
    return Xs

def spectrogram( X ):
    return scipy.signal.spectrogram( X, fs=rate_, nperseg = 2**9)

def gen_summary( data ):
    plt.figure()
    ax1 = plt.subplot( 311 )
    ax1.autoscale( False )
    tvec = np.arange(0, len(data)) * 1/rate_
    ax1.plot( tvec, data )
    ax1.set_title( 'Raw signal' )
    ax1.set_xlabel( 'Time (sec)' )

    ax2 = plt.subplot( 312 )
    #  f, Pxx_den = scipy.signal.periodogram(data, rate_)
    f, Pxx_den = scipy.signal.welch( data, rate_)
    ax2.semilogy( f, Pxx_den  )
    ax2.set_title( 'Power density (Welch)' )
    ax2.set_xlabel( 'Freq (Hz)' )
    ax2.set_ylabel( 'PSD[V**2/Hz]' )

    # Filtered data.
    ax3 = plt.subplot( 313, sharex=ax1 )
    b, a= scipy.signal.butter( 4, 0.375, btype='low', analog=False)
    sig = scipy.signal.filtfilt(b, a, data )
    ax3.plot( tvec, sig)
    ax3.set_title( 'Cutoff=15k' )
    ax3.set_xlabel( 'Time (sec)' )

    plt.tight_layout()
    plt.savefig( 'summary.png' )
    plt.close()

    return data

def analyze( spec ):
    frame = np.uint8( 255 * spec /spec.max())
    #  frame = cv2.blur( spec, (9,9) )

    u, s = frame.mean(), frame.std()
    frame[ frame < u + s ] = 0

    return frame


def process( data ):
    global rate_
    T = 1.0 / rate_
    tvec = np.arange(0, len(data)) * T

    plt.figure( figsize=(12,8) )
    plt.subplot( 311 )
    plt.plot( tvec, data )
    plt.xlabel( 'Time (sec)' )
    plt.subplot( 312 )

    # spectroram
    #  Xs = spectrogram_manual( data )
    #  spec = np.log10(Xs.T)
    #  plt.imshow( spec, interpolation = 'none', aspect = 'auto')
    #  plt.colorbar()
    f, t, Xs = spectrogram(data)
    spec = 1 + np.log10( Xs )
    spec[spec<0] = 0
    plt.pcolormesh( t, f, spec )
    plt.colorbar()

    # analyze spectogram
    plt.subplot( 313 )
    final = analyze( spec )
    plt.imshow( final, interpolation = 'none', aspect = 'auto')
    plt.colorbar()


    plt.savefig( 'result.png' )

def main():
    global rate_
    global freq_
    filename = sys.argv[1]
    #  data_, rate_ = soundfile.read( filename )
    rate_, data = scipy.io.wavfile.read( filename )
    assert len(data) > 0
    data = gen_summary( data )
    print( '--> Processing ...' )
    process( data[:len(data)//4] )


if __name__ == '__main__':
    main()
