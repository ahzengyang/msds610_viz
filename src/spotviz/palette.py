"""Spotify color system for spotviz.

The brand colors and the categorical palette that give the library its visual
identity. Spotify Green is reserved as the single *accent* color and is
deliberately kept out of the categorical palette, per Spotify's brand rule that
green should not be combined with other brand-palette colors.
"""

# --- core brand colors -------------------------------------------------------
GREEN = "#1DB954"         # primary accent (the one emphasis color)
GREEN_BRIGHT = "#1ED760"  # brighter highlight
BLACK = "#191414"         # brand black / alternate dark surface
APP_BG = "#121212"        # near-black default dark background
WHITE = "#FFFFFF"

#: The default accent color.
ACCENT = GREEN

# --- categorical palette (multi-series) --------------------------------------
# Vivid but distinct, checked to stay separable under deuteranopia/protanopia.
# Spotify Green is intentionally NOT here: green stays reserved for the accent,
# so it keeps its meaning and never competes as "category 3".
CATEGORICAL = [
    "#FF6437",  # orange
    "#A056FF",  # violet
    "#2D9CDB",  # blue
    "#FFC864",  # yellow
    "#EB5C8E",  # pink
]

#: Sequential/continuous colormap — matplotlib's perceptually-uniform viridis.
SEQUENTIAL = "viridis"


def categorical(n=None):
    """Return the categorical palette, cycled to length ``n`` if given."""
    if n is None:
        return list(CATEGORICAL)
    if n <= 0:
        return []
    reps = (n // len(CATEGORICAL)) + 1
    return (CATEGORICAL * reps)[:n]
