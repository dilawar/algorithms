"""exp1.py: 

System of bistable switches with interaction.

"""
    
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2016, Dilawar Singh"
__credits__          = ["NCBS Bangalore"]
__license__          = "GNU GPL"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"
__status__           = "Development"

import sys
import os
import matplotlib.pyplot as plt
import numpy as np
import markov

ss0, ss1, ss2 = [], [], []
xvec = []
for i in range( 20 ):
    delP = 0.04 * i
    xvec.append( delP )
    expr="0.09 0.09 0;0.09 0 (0.1+{0})*0.9;0.09 0 (0.1+{0})*0.9;0 0.09 0.09".format( delP )
    mc = markov.MarkovChain( expr )
    state = mc.find_steady_state( )
    s0, s1, s2 = state[0], sum( state[1:3] ), state[3]
    ss0.append( s0 )
    ss1.append( s1 )
    ss2.append( s2 )

plt.plot( xvec, ss0, label = '0' )
plt.plot( xvec, ss1, label = '1' )
plt.plot( xvec, ss2, label = '2' )
plt.title( 'Two interacting bistable with pUp = %s, pDown = %s' % (0.1, 0.1) )
plt.xlabel( 'delta P (interaction)' )
plt.legend( )
plt.savefig( '%s.png' % sys.argv[0] )
