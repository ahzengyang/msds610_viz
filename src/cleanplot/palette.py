"""Color palettes for cleanplot.

The categorical palette is the Okabe-Ito qualitative palette, a widely used
set of eight hues chosen to stay distinguishable under the common forms of
color-vision deficiency (deuteranopia, protanopia, tritanopia). It is our
default so that "use the defaults" already means "colorblind-safe".

For continuous data we deliberately keep matplotlib's ``viridis`` (a
perceptually uniform, luminance-varying map) rather than shipping our own.
"""

# Okabe-Ito colorblind-safe qualitative palette.
# Reference order, black moved last so the first colors are vivid.
CATEGORICAL = [
    "#0072B2",  # blue
    "#E69F00",  # orange
    "#009E73",  # bluish green
    "#D55E00",  # vermillion
    "#56B4E9",  # sky blue
    "#CC79A7",  # reddish purple
    "#F0E442",  # yellow
    "#000000",  # black
]

# Neutral grays used to mute non-emphasized elements. Contrast, not variety,
# is what directs the eye, so most marks default to a muted gray and a single
# accent color carries the emphasis.
GRAY = "#BDBDBD"          # muted fill for de-emphasized marks
GRAY_DARK = "#4D4D4D"     # text / strong lines
GRAY_MID = "#888888"      # secondary lines (whiskers, etc.)
GRAY_LIGHT = "#DDDDDD"    # gridlines

# Default single accent color, used when a helper highlights one thing.
ACCENT = CATEGORICAL[0]   # blue

# Default sequential colormap name for continuous data (matplotlib built-in).
SEQUENTIAL = "viridis"


def categorical(n=None):
    """Return the categorical palette, cycled to length ``n`` if given.

    Parameters
    ----------
    n : int, optional
        Number of colors requested. If ``None``, the full base palette is
        returned. If larger than the palette, colors are cycled.
    """
    if n is None:
        return list(CATEGORICAL)
    if n <= 0:
        return []
    reps = (n // len(CATEGORICAL)) + 1
    return (CATEGORICAL * reps)[:n]
