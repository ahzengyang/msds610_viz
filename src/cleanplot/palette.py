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


# --- "chinese" theme palette -------------------------------------------------
# A categorical palette drawn from traditional Chinese colors (中国传统色):
# ink-and-paper aesthetic with china red as the natural accent. Hues are kept
# reasonably distinct, but this palette is chosen for its look, not for the
# strict colorblind-safety of the default palette above.
CHINESE = [
    "#C1272D",  # 中国红  china red
    "#1E6A8C",  # 靛青    indigo blue
    "#5A8F5A",  # 竹青    bamboo green
    "#E0A32E",  # 藤黄    gamboge yellow
    "#6E5773",  # 黛紫    dark purple
    "#A6572F",  # 赭石    ochre
    "#7BA9A0",  # 天青    celadon
    "#33312B",  # 墨      ink
]

# Warm neutrals for the ink-on-paper look.
PAPER = "#F7F2E7"       # 宣纸  rice-paper background
INK = "#33312B"         # 墨    text / strong lines
INK_MID = "#6E6A5E"     # softer ink for secondary lines
STONE = "#C8C0AD"       # muted warm fill for de-emphasized marks
PAPER_GRID = "#DDD5C4"  # faint warm gridlines
CHINESE_ACCENT = CHINESE[0]  # china red


# Per-theme color roles used by the chart helpers so a helper's muted/accent
# colors follow whichever theme is in use. Keys: neutral (muted fill), accent
# (highlight), ink (strong lines/edges), mid (secondary lines).
THEME_COLORS = {
    "cleanplot": {
        "neutral": GRAY,
        "accent": ACCENT,
        "ink": GRAY_DARK,
        "mid": GRAY_MID,
    },
    "chinese": {
        "neutral": STONE,
        "accent": CHINESE_ACCENT,
        "ink": INK,
        "mid": INK_MID,
    },
}


def theme_colors(name="cleanplot"):
    """Return the color roles dict for a theme name (falls back to default)."""
    return THEME_COLORS.get(name, THEME_COLORS["cleanplot"])


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
