from collections import namedtuple

import numpy as np

import render

class Polar(object):
    @staticmethod
    def scale_1(pos):
        return pos
    @staticmethod
    def scale_2(pos):
        return render._scaleLinear(pos, min=0, max=2*np.pi)
    @staticmethod
    def x(pos):
        r, theta = pos
        return r * np.cos(theta)
    @staticmethod
    def y(pos):
        r, theta = pos
        return r * np.sin(theta)

class Transform(namedtuple("Transform", ["pos", "color", "size"])):
    def __new__(cls, pos=None, color=None, size=None):
        return super(Transform, cls).__new__(cls, pos, color,size)
