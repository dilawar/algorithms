__author__ = "Dilawar Singh"
__email__ = "dilawar@subcom.tech"

import numpy as np
import matplotlib.pyplot as plt

def main():
    N = 10**4
    y1 = np.random.normal(500, 500, N)
    y2 = np.random.normal(1000, 500, N)
    x = np.hstack((y1, y2, y1, y2))
    
    x1 = np.convolve(x, np.ones(100)/100, 'same')

    x2 = []
    u = 0.0
    for _x in x:
        u = (_x + u * 100) / 101
        x2.append(u)

    
    plt.plot(x, label='raw data')
    plt.plot(x1, label='np.convole')
    plt.plot(x2, label='my windowed mean')
    plt.legend()

    plt.show()

if __name__ == '__main__':
    main()

