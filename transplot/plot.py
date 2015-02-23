from collections import namedtuple

import numpy as np
import pandas as pd
import bokeh.plotting as bk

from . import transform

class Graph(object):
    def __init__(self, data, pos, color=None, size=None, 
                 transform=transform.identity, glyphs=()):
        self.data = data
        self.pos = pos
        self.color = color
        self.size = size
        self.transform = transform
        self.glyphs = glyphs

    def __add__(self, other):
        if isinstance(other, Glyph):
            return Graph(self.data, self.pos, self.color, self.size, 
                         self.transform, self.glyphs + (other,))
    def __radd(self, other):
        return self + other
    def custom_grid(self, plot, transform):
        min, max = self.data[self.pos].min(), self.data[self.pos].max()
        # pass in columns to preserve order
        df = pd.DataFrame({col: np.linspace(min[i], max[i], 50)
                           for i, col in enumerate(self.pos)},
                          columns=self.pos)

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

        if transform.pos.custom_axis:
            plot = bk.figure(x_axis_type=None, y_axis_type=None)
            plot.grid.grid_line_color = None

            self.custom_grid(plot, transform)
        else:
            pass

        pos = pd.DataFrame(self.data[self.pos])
        xs, ys = transform.pos.point(transform.pos.scale(pos))

        colors = None
        if self.color is not None:
            colors = pd.DataFrame(self.data[self.color])
            colors = transform.color.color(transform.color.scale(colors))
        
        for glyph in self.glyphs:
            glyph.render(plot, transform, pos=(xs, ys), colors=colors)
        return plot

class Glyph(object): 
    def render(self, graph, plot):
        pass

class Point(Glyph):
    def render(self, plot, transform, pos, colors):
        categorical = isinstance(colors, pd.Categorical)
        string = colors.dtype in {np.dtype(object), np.dtype(str), np.dtype(bytes)}
        if categorical or string:
            pass
        else:
            pass

        xs, ys = pos
        plot.scatter(xs, ys)
