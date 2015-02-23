import pandas as pd

import transplot as tp
import bokeh.plotting as bk

df = pd.read_csv("data/iris.csv")
df.Name = pd.Categorical(df.Name, ordered=False)

graph = tp.Graph(data=df, pos=["SepalLength", "PetalLength"], color="Name",
                 transform=tp.Transform(pos=tp.Parabolic)) + \
            tp.Point()

plot = graph.render()
bk.output_file("test.html")
bk.save(obj=plot)

