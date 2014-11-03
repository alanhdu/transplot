from __future__ import division
import collections
import itertools
izip = itertools.izip

import numpy as np
import pandas as pd
import seaborn as sns

import plot

def _scaleLinear(pos, min=0, max=1000):
    if (pos.max() - pos.min() == 0).all():
        df = pos.copy()
        return min + df - df
    else:
        p = (pos - pos.min()) / (pos.max() - pos.min()) # p in [0, 1]
        return min + p * (max - min)

def _scaleArea(pos, min=8):
    if (pos.max() - pos.min() == 0).all():
        df = pos.copy()
        return min + df - df
    else:
        return np.sqrt(pos / pos.min()) * min

def _rgb2Hex(r, g, b):
    return "#{:02x}{:02x}{:02x}".format(int(255*r), int(255*g), int(255*b))
def _groupPalette(group):
    unique = group.data.unique()
    palette = sns.color_palette("husl", len(unique))
    p = {group : _rgb2Hex(r, g, b)
         for group, (r, g, b) in izip(unique, palette)}
    for group in group.data:
        yield p[group]

def _groupColormap(data):
    pass

def renderSVG(graph, fname="test.svg"):
    import svgwrite
    dwg = svgwrite.Drawing(fname)
    dwg.viewbox(-50, -50, 1100, 1100)
    dwg.fit("right", "bottom", "meet")

    for glyph in graph.glyphs:
        pos = graph.pos if glyph.pos is None else glyph.pos
        size = graph.size if glyph.size is None else glyph.size

        if isinstance(glyph, plot.Points):
            p1, p2 = pos.columns
            scaled = _scaleLinear(pos)
            pos = izip(scaled[p1], scaled[p2])

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
                dwg.add(dwg.circle(p, r=r, fill=c))
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

