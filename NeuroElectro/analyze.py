"""analyze.py: 

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
import pandas as pd

def main():
    df = pd.read_csv('./article_ephys_metadata_curated.csv', sep='\t')
    cols = list(df.columns)
    print(sorted(cols))
    print( [ x for x in cols if 'volt' in x] )
    for i, x in enumerate(['tau']):
        plt.subplot(3, 3, i+1)
        x = df[x]
        x = x.dropna()
        plt.hist(x, bins=20)
        plt.title(f'mean={np.mean(x):.2f}', fontsize=10)

    plt.show()

if __name__ == '__main__':
    main()
