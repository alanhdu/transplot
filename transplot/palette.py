import numpy as np
import husl


def husl_palette(n_colors=6, h=.01, s=.9, l=.65):
    """Get a set of evenly spaced colors in HUSL hue space.

    h, s, and l should be between 0 and 1

    Parameters
    ----------

    n_colors : int
        number of colors in the palette
    h : float
        first hue
    s : float
        saturation
    l : float
        lightness

    Returns
    -------
    palette : list of tuples
        color palette

    """
    hues = np.linspace(h, 1 + h, n_colors, endpoint=False)
    hues = 359 * (hues % 1)
    s *= 99
    l *= 99
    return [rgb_to_hex(husl.husl_to_rgb(h_i, s, l)) for h_i in hues]

def rgb_to_hex(color):
    r, g, b = color
    return "#{:02x}{:02x}{:02x}".format(int(255*r), int(255*g), int(255*b))
