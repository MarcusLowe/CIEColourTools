import numpy as np

def ASCIIXYtoArr(filename):
    f = np.loadtxt(filename)
    print(f)