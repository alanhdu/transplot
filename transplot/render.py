from __future__ import division
import collections
import itertools
izip = itertools.izip

import numpy as np
import pandas as pd
import seaborn as sns

import plot


class _ScaleLinear(object):
    def __init__(self, min=0, max=1000, data=None):
        self.data = data
        self.min = min
        self.max = max

    def scaleData(self):
        min = self.data.min()
        max = self.data.max()
        if (min - max == 0).all():
            df = pos.copy()
            return self.min + df - df
        else:
            p = (self.data - min) / (max - min) # p in [0, 1]
            return self.min + p * (self.max - self.min)
    def scalePoint(self, point):
        point = (point - self.data.min()) / (self.data.max() - self.data.min())
        return self.min + point * (self.max - self.min)

def _scaleArea(pos, min=8):
    if (pos.max() - pos.min() == 0).all():
        df = pos.copy()
        return min + df - df
    else:
        return np.sqrt(pos / pos.min()) * min

def _rgb2Hex(color):
    r, g, b = color
    return "#{:02x}{:02x}{:02x}".format(int(255*r), int(255*g), int(255*b))
def _groupPalette(group):
    unique = group.data.unique()
    palette = sns.color_palette("husl", len(unique))
    p = {group : _rgb2Hex(color)
         for group, color in izip(unique, palette)}
    for group in group.data:
        yield p[group]
def _groupColormap(data):
    palette = sns.color_palette("BuPu_d", 256)
    ColorScaler = _ScaleLinear(min=0, max=255, data=data)
    for d in ColorScaler.scaleData():
        yield _rgb2Hex(palette[int(d)])

def renderSVG(graph, fname="test.svg"):
    import svgwrite
    dwg = svgwrite.Drawing(fname)
    dwg.viewbox(-100, -50, 1150, 1150)
    dwg.fit("right", "bottom", "meet")


    for glyph in graph.glyphs:
        pos = graph.pos if glyph.pos is None else glyph.pos
        transform = graph.transform if glyph.transform is None else glyph.transform
        size = graph.size if glyph.size is None else glyph.size

        scaler = _ScaleLinear(data=pos, min=0, max=1000)

        xmed, ymed = pos.median()
        
        if isinstance(glyph, plot.Points):
            p1, p2 = pos.columns
            if transform is not None and transform.pos is not None:
                pos[p1] = transform.pos.scale_1(pos[p1])
                pos[p2] = transform.pos.scale_2(pos[p2])
                xs = pd.Series(transform.pos.x(p) for p in izip(pos[p1], pos[p2]))
                ys = pd.Series(transform.pos.y(p) for p in izip(pos[p1], pos[p2]))

                scaler = _ScaleLinear(min=0, max=1000, data=pd.DataFrame({p1: xs, p2: ys}))
                scaled = scaler.scaleData()

                xpoints = []
                for c1 in np.linspace(pos[p1].min(), pos[p1].max(), 50):
                    point = (c1, ymed)
                    x, y = scaler.scalePoint(transform.pos.point(point))
                    xpoints.append((x, 1000-y))
                dwg.add(dwg.polyline(xpoints, stroke="black", stroke_width=4, fill_opacity=0))

                ypoints = []
                for c2 in np.linspace(pos[p2].min(), pos[p2].max(), 50):
                    point = (xmed, c2)
                    x, y = scaler.scalePoint(transform.pos.point(point))
                    ypoints.append((x, 1000-y))
                dwg.add(dwg.polyline(ypoints, stroke="black", stroke_width=4, fill_opacity=0))
            else:
                scaled = scaler.scaleData()

            pos = izip(scaled[p1], 1000 - scaled[p2])

            
            if not isinstance(size, collections.Iterable):
                size = itertools.repeat(size)
            else:
                size = _scaleArea(size)

            if glyph.color is None:
                if graph.color is None:
                    color = "blue"
                elif isinstance(graph.color, plot.Group):
                    color = _groupPalette(graph.color)
                else:
                    color = _groupColormap(graph.color)
            elif isinstance(glyph.color, plot.Group):
                color = _groupPalette(glyph.color)
            else:
                color = _groupColormap(glyph.color)

            for p, r, c in izip(pos, size, color):
                dwg.add(dwg.circle(p, r=r, fill=c, stroke=c))
    dwg.save()
    return dwg

def renderTk(graph):
    import Tkinter as tk

    master = tk.Tk()
    w = tk.Canvas(master, width=400, height=400)
    w.pack()


    for glyph in graph.glyphs:
        pos = graph.pos if glyph.pos is None else glyph.pos
        color = graph.color if glyph.color is None else glyph.color


        if isinstance(glyph, plot.Points):
            scale = 400.0 / (pos.max() - pos.min())
            pos = (pos - pos.min()) * scale

            p1, p2 = pos.columns
            for x, y in zip(pos[p1], pos[p2]):
                w.create_oval(x-2, y-2, x+2, y+2, fill="black")
    tk.mainloop()

