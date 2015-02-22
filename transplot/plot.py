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
    def custom_grid(self, plot, transform):
        min, max = self.pos.min(), self.pos.max()
        # pass in columns to preserve order
        df = pd.DataFrame({col: np.linspace(min[i], max[i], 50)
                           for i, col in enumerate(self.pos.columns)},
                          columns=self.pos.columns)

        for dim in range(len(min)):
            for c in np.linspace(min[dim], max[dim], 6):
                df[df.columns[dim]] = c
                xs, ys = transform.pos.point(transform.pos.scale(df))
                plot.line(xs, ys)

            # reset change
            df[df.columns[dim]] = np.linspace(min[dim], max[dim], 50)

    def render(self):
        plot = bk.figure()
        transform = self.transform(self)
        scaled_pos = transform.pos.scale(self.pos)

        if transform.pos.custom_axis:
            plot = bk.figure(x_axis_type=None, y_axis_type=None)
            plot.grid.grid_line_color = None

            self.custom_grid(plot, transform)
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
