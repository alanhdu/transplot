from collections import namedtuple
from functools import partial

import numpy as np
import pandas as pd

from .util import LinearScaler

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
        return scaled[scaled.columns[0]], scaled[scaled.columns[1]]

identity = Transform(pos=PosTransform)


class Polar(PosTransform):
    custom_axis = True
    def __init__(self, pos):
        self.pos = pos
        self.scaler = LinearScaler(pos[pos.columns[1]], 0, 2 * np.pi)

    def scale(self, pos):
        pos = pos.copy()
        pos[pos.columns[1]] = self.scaler.scale(pos[pos.columns[1]])
        return pos

    def point(self, scaled):
        r, theta = scaled[scaled.columns[0]], scaled[scaled.columns[1]] 
        return r * np.cos(theta), r * np.sin(theta)

class Parabolic(PosTransform):
    custom_axis = True
    def point(self, scaled):
        tau = scaled[scaled.columns[0]]
        sigma = scaled[scaled.columns[1]]

        return tau * sigma, (tau ** 2 - sigma ** 2) / 2

class Elliptic(PosTransform):
    custom_axis = True
    def __init__(self, pos):
        self.pos = pos
        self.scaler = LinearScaler(pos[pos.columns[1]], 0, 2 * np.pi)

    def scale(self, pos):
        pos = pos.copy()
        pos[pos.columns[1]] = self.scaler.scale(pos[pos.columns[1]])
        return pos

    def point(self, scaled):
        mu = scaled[scaled.columns[0]]
        nu = scaled[scaled.columns[1]]

        return np.cosh(mu) * np.cos(nu), np.sinh(mu) * np.sin(nu)
