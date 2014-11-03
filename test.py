import pandas as pd

import transplot as tp


df = pd.read_csv("/home/alan/workspace/vind/test/iris.csv")

g = tp.plot.Graph(pos=df[["SepalLength", "SepalWidth"]]) \
        + tp.plot.Points(size=df["PetalLength"], color=df["PetalWidth"])
        #+ tp.plot.Points()

tp.render.renderSVG(g)
