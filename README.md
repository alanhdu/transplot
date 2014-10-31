transplot
====

A (hopefully) nice plotting library. Essentially ggplot but with easy coordinate transforms and segregation of rendering.

# Goals
* **Intelligent:** It should be easy to make nice, intelligent plots that look good. That means intelligent APIs (more like ggplot than matplotlib) and intelligent defaults (no jet colormap).
* **Powerful:** You should be able to create almost any chart you want here. Coordinate transforms, faceting, colors, animation, all should be easy.
* **Flexible:** Strict separation between the graph and the image. It should be able to write custom renderers for different backends (e.g. png file vs embedded in html).
* **Fast:** You should be able to deal with large amounts of data quickly. Not only should the computation be fast, but abstract rendering and downsampling should be built-in.
* **Usable:** It should work intelligently with other projects like Pandas or NumPy. I will also try to write good documentation, although we'll see about that. 

# Vision
* Graph = [Coordinate System + Glyphs + Label] x Faceting
* Image = Render(Graph)
* Glyph = Point | Line | Text | Interval
* Coordinate System = Animation(Dimensions x Transform)
* Dimension = Position | Color | Size
* Transform can be arbitrary functions. 
    * Single-variable function (e.g. log transform)
    * N -> N, like Cartesian -> Spherical
    * Common built-ins like Cartesian, Polar, Spherical, RGB, HSL
* Animation = function(time)

# Proposed Examples
```
# Scatter plot with trend line
graph = coord(pos=(log("wealth"), sqrt("height")), group="gender") \
    + glyph.points(size="weight") \
    + glyph.interpolate(smooth="linear_model", free="wealth", group=False)   # Only one trend line

# Pie Chart
graph = coord(pos=(proportion("favorite food"), stack), transform=(r, theta)) \
    + glyph.interval()

# Interaction Plot
graph = coord(pos=("SAT Score", "GPA"))
graph += glyph.interpolate(smooth=interaction("SAT", "GPA"), type=contour)

# Heatmap
graph = coord(pos=("SAT", "GPA")) \
    + glyph.interpolate(smooth=age_based_on("SAT", "GPA"), type=heatmap)

# Matrix Plot
graph = coord(pos=("SAT Score", "GPA")) * facet(x="age", y="state") \
    + glyph.points()
```
