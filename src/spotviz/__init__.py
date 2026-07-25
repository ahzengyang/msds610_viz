"""spotviz — clean, on-brand (Spotify-themed) charts from pandas.

A thin wrapper over pandas + matplotlib. Dark Spotify theme by default, Spotify
Green as the single accent, and polished bar/line/scatter helpers that
auto-label from your DataFrame and return the matplotlib ``Axes``.

Quick start
-----------
>>> import pandas as pd
>>> import spotviz as sv
>>> ax = sv.bar(df, x="genre", y="streams", highlight="Pop")
>>> ax = sv.line(df, x="month")                 # multi-series, direct-labeled
>>> ax = sv.scatter(df, x="energy", y="danceability", size="popularity")
"""

from .bar import bar
from .line import line
from .scatter import scatter
from .palette import (
    ACCENT,
    CATEGORICAL,
    GREEN,
    GREEN_BRIGHT,
    SEQUENTIAL,
    categorical,
)
from .theme import (
    THEMES,
    apply_theme,
    rc_params,
    theme_context,
)
from ._core import savefig, theme_colors

__version__ = "0.1.0"

__all__ = [
    "bar",
    "line",
    "scatter",
    "apply_theme",
    "theme_context",
    "rc_params",
    "theme_colors",
    "savefig",
    "THEMES",
    "ACCENT",
    "GREEN",
    "GREEN_BRIGHT",
    "CATEGORICAL",
    "SEQUENTIAL",
    "categorical",
    "__version__",
]
