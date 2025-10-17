import numpy as np

def oleinik(f, c, m):
    return np.min(f + c -m , axis=0)

