from collections import namedtuple

import blaze as bz
import pandas as pd

import transform

class Graph(object):
    def __init__(self, pos, color=None, size=10, transform=transform.identity, glyphs=()):
        self.pos = bz.into(pd.DataFrame, pos)
        self.color = color
        self.size = size
        self.transform = transform
        self.glyphs = glyphs

    def __add__(self, other):
        if isinstance(other, Glyph):
            return Graph(self.pos, self.color, self.size, self.transform, self.glyphs + (other,))
    def __radd(self, other):
        return self + other

    def __mul__(self, other):
        if isinstance(other, transform.Transform):
            return Graph(self.pos, self.color, self.size, other, self.glyphs)
    def __rmul__(self, other):
        return other * self

class Glyph(object): 
    pass

Group = namedtuple("Group", ["data"])

class Points(namedtuple("Points", ["pos", "color", "size", "transform"]),
             Glyph):
    def __new__(cls, pos=None, color=None, size=None, transform=None):
        pos = bz.into(pd.DataFrame, pos) if pos is not None else pos
        return super(Points, cls).__new__(cls, pos, color, size, transform)

class Line(namedtuple("Line", ["pos", "color", "size", "transform"]),
           Glyph):
    def __new__(cls, pos=None, color=None, size=None, transform=None):
        pos = bz.into(pd.DataFrame, pos) if pos is not None else pos
        return super(Points, cls).__new__(cls, pos, color, size, transform)
