"""
Compute mean and std with the assumption that a cicurlar buffer of size N is
storing the values.

Here we compare the error in our approach. 

DO NOT USE IT IN PRODUCTION.
"""

__author__ = "Dilawar Singh"
__email__ = "dilawar@subcom.tech"

import librosa  # to load audio data (excellent library)
import numpy as np
import matplotlib.pyplot as plt


def main():
    x, sr = librosa.load(librosa.example("trumpet"), sr=16000)

    # 2 second long buffer size.
    BUFFER_SIZE = 2 * sr
    print(f"[INFO] {BUFFER_SIZE=}")

    # mean using rolling windows: This is the ground truth.
    x1 = np.zeros_like(x)
    s1 = np.zeros_like(x)
    for i in range(0, len(x)):
        x1[i] = np.mean(x[i : i + BUFFER_SIZE])
        s1[i] = np.std(x[i : i + BUFFER_SIZE])

    x2 = np.zeros_like(x)
    s2 = np.zeros_like(x)

    u: float = 0.0
    s: float = 0.0

    # My std algorithm. Though it catches on quickly it does not decay fast
    # enough unless the buffer size is much smaller than the one we have used
    # for the mean.
    for i, _x in enumerate(x):
        uu : float = (_x + u * BUFFER_SIZE) / (1 + BUFFER_SIZE)
        x2[i] = uu
        s : float = s + ((_x - u) * (_x - uu) - s) / (BUFFER_SIZE//20)
        u = uu
        s2[i] = s ** 0.5

    plt.subplot(311)
    plt.plot(x, label="raw data")
    plt.legend()
    plt.subplot(312)
    plt.plot(x1, alpha=0.8, label="mean")
    plt.plot(x2, alpha=0.8, label="my mean")
    plt.plot((x1 - x2) ** 2, alpha=0.8, label="err")
    plt.legend()
    plt.subplot(313)
    plt.plot(s1, alpha=0.8, label="std")
    plt.plot(s2, alpha=0.8, label="my std")

    plt.show()


if __name__ == "__main__":
    main()
