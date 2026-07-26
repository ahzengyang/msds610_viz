"""Color system for spotviz.

The brand colors and the categorical palette that give the library its visual
identity. the signature green is reserved as the single *accent* color and is
deliberately kept out of the categorical palette, per the brand rule that
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
# Vivid but distinct, and CVD-tuned: verified with a colorblindness simulation
# (Machado 2009 + CIELAB ΔE, see tools/check_cvd.py) to keep every pair clearly
# separable under deuteranopia, protanopia, and tritanopia — minimum pairwise
# ΔE ≈ 21 across all three. the signature green is intentionally NOT here: green stays
# reserved for the accent, so it keeps its meaning and never competes as
# "category 3".
CATEGORICAL = [
    "#FF7A5C",  # coral
    "#FFD23F",  # yellow
    "#E8338A",  # magenta
    "#A056FF",  # violet
    "#2D9CDB",  # blue
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
