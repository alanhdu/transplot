import numpy as np
import pandas as pd

class LinearScaler(object):
    def __init__(self, data, min=0, max=1000):
        self.min = min
        self.max = max

        self.data_min = data.min()
        self.data_max = data.max()

    def scale(self, pos):
        p = (pos - self.data_min) / (self.data_max - self.data_min)
        return self.min + p * (self.max - self.min)

    @property
    def range(self):
        return self.data_min, self.data_max

def _scaleArea(pos, min=8):
    if (pos.max() - pos.min() == 0).all():
        df = pos.copy()
        return min + df - df
    else:
        return np.sqrt(pos / pos.min()) * min

def _rgb2Hex(color):
    r, g, b = color
    return "#{:02x}{:02x}{:02x}".format(int(255*r), int(255*g), int(255*b))
