from __future__ import division
import collections
import itertools
izip = itertools.izip

import numpy as np
import pandas as pd

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

def renderSVG(graph, fname="test.svg"):
    import svgwrite
    dwg = svgwrite.Drawing(fname)
    dwg.viewbox(-50, -50, 1100, 1100)
    dwg.fit("right", "bottom", "meet")

    for glyph in graph.glyphs:
        pos = graph.pos if glyph.pos is None else glyph.pos
        color = graph.color if glyph.color is None else glyph.color
        size = graph.size if glyph.size is None else glyph.size

        if isinstance(glyph, plot.Points):
            p1, p2 = pos.columns
            scaled = _scaleLinear(pos)
            pos = izip(scaled[p1], scaled[p1])

            if not isinstance(size, collections.Iterable):
                size = itertools.repeat(size)
            else:
                size = _scaleArea(size)
            for x, y, r in izip(scaled[p1], scaled[p2], size):
                dwg.add(dwg.circle( (x,y), r=r))
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

