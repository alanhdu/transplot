import numpy as np
import pandas as pd

class _ScaleLinear(object):
    def __init__(self, min=0, max=1000, data=None):
        self.data = data
        self.min = min
        self.max = max
    def scaleData(self):
        min = self.data.min()
        max = self.data.max()
        if (min - max == 0).all():
            df = pos.copy()
            return self.min + df - df
        else:
            p = (self.data - min) / (max - min) # p in [0, 1]
            return self.min + p * (self.max - self.min)
    def scalePoint(self, point):
        point = (point - self.data.min()) / (self.data.max() - self.data.min())
        return self.min + point * (self.max - self.min)

def _scaleArea(pos, min=8):
    if (pos.max() - pos.min() == 0).all():
        df = pos.copy()
        return min + df - df
    else:
        return np.sqrt(pos / pos.min()) * min

def _rgb2Hex(color):
    r, g, b = color
    return "#{:02x}{:02x}{:02x}".format(int(255*r), int(255*g), int(255*b))
