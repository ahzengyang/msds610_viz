"""cleanplot — clean, honest matplotlib charts from pandas, by default.

A thin wrapper over pandas + matplotlib. Call a simple function on your
DataFrame and get a chart that's more readable than raw matplotlib, with no
configuration required. Every helper returns the matplotlib ``Axes`` so you
can keep customizing.

Quick start
-----------
>>> import pandas as pd
>>> import cleanplot as cp
>>> ax = cp.boxplot(df, column="score", by="section")
"""

from .boxplot import boxplot
from .palette import CATEGORICAL, CHINESE, SEQUENTIAL, categorical, theme_colors
from .theme import (
    DEFAULT_THEME,
    RC_PARAMS,
    STYLE_NAME,
    STYLE_PATH,
    STYLE_PATHS,
    THEMES,
    apply_style,
    style_context,
    theme_rc,
)

__version__ = "0.1.0"

__all__ = [
    "boxplot",
    "apply_style",
    "style_context",
    "theme_rc",
    "theme_colors",
    "DEFAULT_THEME",
    "THEMES",
    "RC_PARAMS",
    "STYLE_NAME",
    "STYLE_PATH",
    "STYLE_PATHS",
    "CATEGORICAL",
    "CHINESE",
    "SEQUENTIAL",
    "categorical",
    "__version__",
]
