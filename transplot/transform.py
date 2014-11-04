from collections import namedtuple

import numpy as np

import render

class Polar(object):
    @staticmethod
    def scale_1(pos):
        return pos
    @staticmethod
    def scale_2(pos):
        s = render._ScaleLinear(min=0, max=2*np.pi)
        return s.scaleData(pos)
    @staticmethod
    def x(pos):
        r, theta = pos
        return r * np.cos(theta)
    @staticmethod
    def y(pos):
        r, theta = pos
        return r * np.sin(theta)

class Parabolic(object):
    @staticmethod
    def scale_1(pos):
        return pos
    @staticmethod
    def scale_2(pos):
        return pos
    @staticmethod
    def x(pos):
        tau, sigma = pos
        return tau * sigma
    @staticmethod
    def y(pos):
        tau, sigma = pos
        return (tau * tau - sigma * sigma) / 2

class Transform(namedtuple("Transform", ["pos", "color", "size"])):
    def __new__(cls, pos=None, color=None, size=None):
        return super(Transform, cls).__new__(cls, pos, color,size)
