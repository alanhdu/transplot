from collections import namedtuple

import blaze as bz
import pandas as pd

class Graph(object):
    def __init__(self, pos, color=None, size=None, group=None, transform=None, glyphs=()):
        self.pos = bz.into(pd.DataFrame, pos)
        self.color = color
        self.size = size
        self.group = group
        self.transform = transform
        self.glyphs = glyphs

    def __add__(self, other):
        if isinstance(other, Glyph):
            return Graph(self.pos, self.color, self.size, self.group, self.transform, self.glyphs + (other,))
    def __radd(self, other):
        return self + other

class Transform(namedtuple("Transform", ["pos", "color", "size"])):
    def __new__(cls, pos=None, color=None, size=None):
        return super(Transform, cls).__new__(cls, pos, color,size)

class Glyph(object): 
    pass

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
