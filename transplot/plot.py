from collections import namedtuple

import numpy as np
import pandas as pd
import bokeh.plotting as bk

from . import transform

class Graph(object):
    def __init__(self, pos, color=None, size=None, 
                 transform=transform.identity, glyphs=()):
        self.pos = pos
        self.color = color
        self.size = size
        self.transform = transform
        self.glyphs = glyphs


    def __add__(self, other):
        if isinstance(other, Glyph):
            return Graph(self.pos, self.color, self.size, self.transform, self.glyphs + (other,))
    def __radd(self, other):
        return self + other
    def render(self):
        plot = bk.figure()
        transform = self.transform(self)
        scaled_pos = transform.pos.scale(self.pos)

        if transform.pos.custom_axis:
            plot = bk.figure(x_axis_type=None, y_axis_type=None)
            plot.grid.grid_line_color = None

            p1, p2 = scaled_pos.columns
            min, max = self.pos.min(), self.pos.max()
            for c2 in np.linspace(min[1], max[1], 6):
                df = pd.DataFrame({p1: np.linspace(min[0], max[0], 50),
                                   p2: c2},
                                  columns=[p1, p2])
                xs, ys = transform.pos.point(transform.pos.scale(df))

                plot.line(xs, ys)


            for c1 in np.linspace(min[0], max[0], 6):
                df = pd.DataFrame({p1: c1,
                                   p2: np.linspace(min[1], max[1], 50)},
                                   columns=[p1, p2])
                xs, ys = transform.pos.point(transform.pos.scale(df))
                plot.line(xs, ys)

        else:
            pass

        for glyph in self.glyphs:
            glyph.render(plot, transform, scaled_pos)
        return plot

class Glyph(object): 
    def render(self, graph, plot):
        pass

class Point(Glyph):
    def render(self, plot, transform, pos):
        xs, ys = transform.pos.point(pos)
        plot.scatter(xs, ys)
