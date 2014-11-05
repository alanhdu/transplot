from collections import namedtuple

import numpy as np

import render

class PosTransform(object):
    @classmethod
    def point(cls, pos):
        return cls.x(pos), cls.y(pos)
    @classmethod
    def scale_1(cls, pos):
        return pos
    @classmethod
    def scale_2(cls, pos):
        return pos
    @classmethod
    def x(cls, pos):
        return pos[0]
    @classmethod
    def y(cls, pos):
        return pos[1]

class Polar(PosTransform):
    @classmethod
    def scale_2(cls, pos):
        s = render._ScaleLinear(min=0, max=2*np.pi, data=pos)
        return s.scaleData()
    @staticmethod
    def x(pos):
        r, theta = pos
        return r * np.cos(theta)
    @staticmethod
    def y(pos):
        r, theta = pos
        return r * np.sin(theta)

class Parabolic(PosTransform):
    @classmethod
    def x(cls, pos):
        tau, sigma = pos
        return tau * sigma
    @classmethod
    def y(cls, pos):
        tau, sigma = pos
        return (tau * tau - sigma * sigma) / 2

class Transform(namedtuple("Transform", ["pos", "color", "size"])):
    def __new__(cls, pos=None, color=None, size=None):
        return super(Transform, cls).__new__(cls, pos, color,size)
