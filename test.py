import pandas as pd

import transplot as tp


df = pd.read_csv("/home/alan/workspace/vind/test/iris.csv")

def pointGroup():
    g = tp.plot.Graph(pos=df[["SepalLength", "SepalWidth"]]) \
            + tp.plot.Points(size=df["PetalLength"], color=tp.plot.Group(df["Name"]))

    tp.render.renderSVG(g, fname="img/pointGroup.svg")

def pointTransform():
    g = tp.plot.Graph(pos=df[["SepalLength", "SepalWidth"]]) * tp.transform.Transform(pos=tp.transform.Parabolic) \
            + tp.plot.Points()

    tp.render.renderSVG(g, fname="img/pointTransform.svg")

def pointColormap():
    g = tp.plot.Graph(pos=df[["SepalLength", "SepalWidth"]]) \
            + tp.plot.Points(size=df["PetalLength"], color=df["PetalWidth"])

    tp.render.renderSVG(g, fname="img/pointColormap.svg")

pointGroup()
pointColormap()
pointTransform()
