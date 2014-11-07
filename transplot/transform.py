from collections import namedtuple

import numpy as np
import pandas as pd

import util

class Transform(namedtuple("Transform", ["pos", "color", "size"])):
    def __new__(cls, pos=None, color=None, size=None):
        return super(Transform, cls).__new__(cls, pos, color,size)


class PosTransform(object):
    @classmethod
    def scale_1(cls, pos):
        return pos
    @classmethod
    def scale_2(cls, pos):
        return pos
    @classmethod
    def point(cls, pos):
        return pd.DataFrame({"x": cls.x(pos), "y": cls.y(pos)})
    @classmethod
    def x(cls, pos):
        return pos[pos.columns[0]]
    @classmethod
    def y(cls, pos):
        return pos[pos.columns[1]]

identity = Transform(pos=PosTransform)

class Polar(PosTransform):
    @classmethod
    def scale_2(cls, pos):
        s = util._ScaleLinear(min=0, max=2*np.pi, data=pos)
        return s.scaleData()
    @staticmethod
    def x(pos):
        r = pos[pos.columns[0]]
        theta = pos[pos.columns[1]]
        return r * np.cos(theta)
    @staticmethod
    def y(pos):
        r = pos[pos.columns[0]]
        theta = pos[pos.columns[1]]
        return r * np.sin(theta)

class Parabolic(PosTransform):
    @classmethod
    def x(cls, pos):
        tau = pos[pos.columns[0]]
        sigma = pos[pos.columns[1]]
        return tau * sigma
    @classmethod
    def y(cls, pos):
        tau = pos[pos.columns[0]]
        sigma = pos[pos.columns[1]]
        return (tau * tau - sigma * sigma) / 2

class Elliptic(PosTransform):
    @classmethod
    def scale_2(cls, pos):
        s = util._ScaleLinear(min=0, max=2*np.pi, data=pos)
        return s.scaleData()

    @classmethod
    def x(cls, pos):
        mu = pos[pos.columns[0]]
        nu = pos[pos.columns[1]]
        return np.cosh(mu) * np.cos(nu)
    @classmethod
    def y(cls, pos):
        mu = pos[pos.columns[0]]
        nu = pos[pos.columns[1]]
        return np.sinh(mu) * np.sin(nu)
