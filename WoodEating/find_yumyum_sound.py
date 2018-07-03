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

def spectrogram( X, nperseg=2**8 ):
    return scipy.signal.spectrogram( X, fs=rate_, nperseg = nperseg)

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

def print_stat( frame ):
    print( 'Mean %f, std: %f, min: %f, max: %s' % (
        frame.mean(), frame.std(), frame.min(), frame.max()) 
        )

def analyze_by_row_col_values( frame, rows = True, cols = True ):
    u, s = frame.mean(), frame.std()
    if cols:
        # Ignore those columns, whose mean is less the backgroud mean.
        colMean = np.mean( frame, axis=0 )
        nothingCol = np.where( colMean < u )[0]
        frame[:, nothingCol] = 0

    if rows:
        # Ignore those row which does have a single pixel which is close to high
        # value.
        rowMax = np.max( frame, axis = 1 )
        nothingRow = np.where( rowMax < u + s )[0]
        frame[nothingRow, :] = 0
    return frame

def remove_cols( frame, threshold):
    # Ignore those columns, whose mean is less the backgroud mean.
    cy = np.mean( frame, axis=0 )
    nothingCol = np.where( cy < threshold )[0]
    frame[:, nothingCol] = 0
    return frame


def blur_in_freq( frame, N=11, method = 'A' ):
    # blur in frequency direction (y) and not in time direction.
    if method == 'G':
        frame = cv2.GaussianBlur( frame, (1,N), 0)
    else:
        frame = cv2.blur( frame, (1, N) )
    return frame

def renormalize_frame( spec ):
    spec = spec - spec.min()
    frame = np.uint8( 255 * spec /spec.max())
    return frame

def analyze( spec ):
    # Turn everything to positive
    frame = renormalize_frame( spec ) 

    #  frame = blur_in_freq( frame, 9 )
    #  u, s = frame.mean(), frame.std()
    # Now remove all colums where mean acitvity is less than global mean
    # activity. This can be dangerous for longer samples i.e. more than few
    # seconds. Or probably not. Not sure about it.
    #  frame = remove_cols( frame, u )
    # Now we have stripes where some noise has been made by insect at low
    # frequency at least.

    frame = frame - frame.mean()
    frame[ frame < 0 ] = 0

    yumyumVec = np.mean( frame, axis=0)
    res = yumyumVec - yumyumVec.mean()
    res[ res < 0 ] = 0

    return res, frame

def analyze_gauss( spec ):
    frame = renormalize_frame( spec )
    a, b = 9, 7
    f1 = cv2.GaussianBlur(frame, (a,a), 0) 
    f2 = cv2.GaussianBlur( frame, (b,b), 0)
    return f1 - f2


def process( data, plot = False ):
    global rate_
    T = 1.0 / rate_
    # For longer data, this analysis would not make sense. Chop signal into 2
    # sec windows and analyze.
    if plot:
        plt.figure( figsize=(12,8) )
        tvec = np.arange(0, len(data)) * T
        plt.subplot( 311 )
        plt.plot( tvec, data )
        plt.xlabel( 'Time (sec)' )

    # spectroram
    #  Xs = spectrogram_manual( data )
    #  spec = np.log10(Xs.T)
    #  plt.imshow( spec, interpolation = 'none', aspect = 'auto')
    #  plt.colorbar()
    f, t, Xs = spectrogram(data, 2**9)
    spec = np.log10( Xs )
    if plot:
        plt.pcolormesh( t, f, spec )
        plt.title( "Spectrogram" )

    # analyze spectogram
    yumyum, img = analyze( spec )
    if plot:
        plt.subplot( 312 )
        plt.imshow( img, interpolation = 'none', aspect = 'auto')
        #  plt.colorbar()

        plt.subplot( 313 )
        plt.plot(t, yumyum )
        plt.xlabel( 'Time (sec)' )
        plt.ylabel( 'Yum Yum' )
        plt.savefig( 'result.png' )
    return yumyum

def find_peaks( yvecs, threshold, separation = 2 ):
    xd = np.diff( yvecs )
    pIds = [0]
    for i, (a, b) in enumerate( zip( xd, xd[1:] ) ):
        if a > 0:
            if yvecs[i+1] > threshold:
                if i > pIds[-1] + separation:
                    pIds.append( i+1)
    return np.array(pIds[1:])

def main():
    global rate_
    global freq_
    filename = sys.argv[1]
    #  data_, rate_ = soundfile.read( filename )
    rate_, data = scipy.io.wavfile.read( filename )
    assert len(data) > 0

    # Window of 2 second each.
    print( 'Rate = %f' % rate_ )

    N = rate_
    yvec = []
    time = []
    for i in range(0, len(data)//N):
        print( '%d sec. ' % i*2 )
        a, b = i*N, (i+1)*N
        res = process( data[a:b] )
        yvec.append( res )
        time.append( np.linspace(a/rate_, b/rate_, len(res)) )

    yumyum = np.hstack( yvec )
    time = np.hstack( time )
    pIds = find_peaks( yumyum, 1, 3)
    plt.subplot(211)
    plt.plot( time, yumyum )
    plt.plot( time[pIds], np.ones(len(pIds))+yumyum.max(), '.'
            , label='NUM-NUM event' 
            )
    plt.legend()
    plt.xlabel( 'Time (sec)' )
    plt.ylabel( 'NUM-NUM Index (au)' )

    plt.subplot(223)
    vals = np.diff( time[pIds] )
    plt.hist( vals, range=(0, vals.max()), bins = 20 )
    plt.title( 'Time betwen NUM-NUM event' )
    plt.xlabel( 'Time (sec)' )
    plt.ylabel( 'Count' )

    plt.subplot( 224 )
    vals = yumyum 
    plt.hist( yumyum, range=(0, yumyum.max()), bins = 20 )
    plt.xlabel( 'NUM-NUM index (au)' )
    plt.title( 'Power in NUM-NUM' )


    plt.tight_layout()
    plt.savefig( 'result.png' )


if __name__ == '__main__':
    main()
