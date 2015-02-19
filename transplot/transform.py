from collections import namedtuple
from functools import partial

import numpy as np
import pandas as pd

from . import util

class _Transform(object):
    def __init__(self, graph, pos=None, color=None, size=None):
        self.graph = graph
        if pos is not None:
            self.pos = pos(self.graph.pos)
        else:
            self.pos = None
        if color is not None:
            self.color = pos(self.graph.color)
        else:
            self.color = None
        if size is not None:
            self.size = size(self.graph.size)
        else:
            self.size = None

def Transform(pos=None, color=None, size=None):
    def _trans(graph):
        return _Transform(graph, pos=pos, color=color, size=size)
    return _trans

class PosTransform(object):
    custom_axis = False
    def __init__(self, pos):
        pass
    def scale(self, pos):
        return pos
    def point(self, scaled):
        return pd.DataFrame({"x": scaled[scaled.columns[0]],
                             "y": scaled[scaled.columns[1]]})

identity = Transform(pos=PosTransform)


class Polar(PosTransform):
    custom_axis = True
    def __init__(self, pos):
        self.pos = pos
        self.scaler = util.LinearScaler(pos[pos.columns[1]], 0, 2 * np.pi)

    def scale(self, pos):
        pos = pos.copy()
        pos[pos.columns[1]] = self.scaler.scale(pos[pos.columns[1]])
        return pos

    def point(self, scaled):
        r = scaled[scaled.columns[0]]
        theta = scaled[scaled.columns[1]]

        ret =  pd.DataFrame({"x": r * np.cos(theta),
                             "y": r * np.sin(theta)})
        return ret

class Parabolic(PosTransform):
    custom_axis = True
    def point(self, scaled):
        tau = scaled[scaled.columns[0]]
        sigma = scaled[scaled.columns[1]]

        return pd.DataFrame({"x": tau * sigma,
                             "y": (tau ** 2 - sigma ** 2) / 2})

class Elliptic(PosTransform):
    custom_axis = True
    def __init__(self, pos):
        self.pos = pos
        self.scaler = util.LinearScaler(pos[pos.columns[1]], 0, 2 * np.pi)

    def scale(self, pos):
        pos = pos.copy()
        pos[pos.columns[1]] = self.scaler.scale(pos[pos.columns[1]])
        return pos

    def point(self, scaled):
        mu = scaled[scaled.columns[0]]
        nu = scaled[scaled.columns[1]]

        return pd.DataFrame({"x": np.cosh(mu) * np.cos(nu),
                             "y": np.sinh(mu) * np.sin(nu)})
