from __future__ import division
import collections
import itertools
izip = itertools.izip

import numpy as np
import pandas as pd
import seaborn as sns

import plot
import util


def _groupPalette(group):
    unique = group.data.unique()
    palette = sns.color_palette("husl", len(unique))
    p = {group : util._rgb2Hex(color)
         for group, color in izip(unique, palette)}
    for group in group.data:
        yield p[group]
def _groupColormap(data):
    palette = sns.color_palette("BuPu_d", 256)
    ColorScaler = util._ScaleLinear(min=0, max=255, data=data)
    for d in ColorScaler.scaleData():
        yield util._rgb2Hex(palette[int(d)])

def renderSVG(graph, fname="test.svg"):
    import svgwrite
    dwg = svgwrite.Drawing(fname)
    dwg.viewbox(-100, -50, 1150, 1150)
    dwg.fit("right", "bottom", "meet")  # aspect ratio settings

    dwg.add(dwg.rect((0,0), (1000, 1000), fill="#CCCCCC"))

    for glyph in graph.glyphs:
        pos = graph.pos if glyph.pos is None else glyph.pos
        transform = graph.transform if glyph.transform is None else glyph.transform
        size = graph.size if glyph.size is None else glyph.size

        scaler = util._ScaleLinear(data=pos, min=0, max=1000)

        xmed, ymed = pos.median()
        
        if isinstance(glyph, plot.Points):
            p1, p2 = pos.columns
            pos[p1] = transform.pos.scale_1(pos[p1])
            pos[p2] = transform.pos.scale_2(pos[p2])

            transformed = transform.pos.point(pos)
            min, max = pos.min(), pos.max()
            scaler = util._ScaleLinear(min=0, max=1000, data=transformed)
            scaled = scaler.scaleData()

            for c2 in np.linspace(min[1], max[1], 6):
                xpoints = collections.deque() 
                df = pd.DataFrame({p1: np.linspace(min[0], max[0], 50), p2: c2})
                df = scaler.scalePoint(transform.pos.point(df))
                dwg.add(dwg.polyline(util.toPoint(df), stroke="white",
                                     stroke_width=4, fill_opacity=0))
            for c1 in np.linspace(min[0], max[0], 6):
                xpoints = collections.deque() 
                df = pd.DataFrame({p1: c1, p2: np.linspace(min[1], max[1], 50)})
                df = scaler.scalePoint(transform.pos.point(df))
                dwg.add(dwg.polyline(util.toPoint(df), stroke="white",
                                     stroke_width=4, fill_opacity=0))

            pos = util.toPoint(scaled)
            
            if not isinstance(size, collections.Iterable):
                size = itertools.repeat(size)
            else:
                size = util._scaleArea(size)

            if glyph.color is None:
                if graph.color is None:
                    color = itertools.repeat("#292F59")
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

