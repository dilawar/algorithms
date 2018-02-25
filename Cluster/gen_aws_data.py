#!/usr/bin/env python

import datetime
import os 
import sys
import random
import names
import numpy as np

pis = [ names.get_full_name( ) for i in range(20) ]
specs = [ 'EE', 'NB', 'CB', 'GD', 'TB', 'UN' ]

specps = [ 0.12, 0.2, 0.12, 0.22, 0.3 ]
specps.append( 1 - sum( specps ) )

def main( ):
    today = datetime.date.today( )
    dates = [ ]
    speakers = [ ]
    for i in range( 50 ):
        for w in range( 3 ):
            date = today + datetime.timedelta( days = i * 7 )
            dates.append(date)
            speakers.append( names.get_full_name( ) )

    supervisors = np.random.choice( pis, len(dates) )
    specializations = np.random.choice( specs, len(dates), p = specps )
    for l in zip( dates, speakers, specializations, supervisors ):
        print( '%s,%s,%s,%s' % l )


if __name__ == '__main__':
    main()
