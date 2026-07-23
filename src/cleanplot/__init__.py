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
from .palette import CATEGORICAL, SEQUENTIAL, categorical
from .theme import (
    RC_PARAMS,
    STYLE_NAME,
    STYLE_PATH,
    apply_style,
    style_context,
)

__version__ = "0.1.0"

__all__ = [
    "boxplot",
    "apply_style",
    "style_context",
    "RC_PARAMS",
    "STYLE_NAME",
    "STYLE_PATH",
    "CATEGORICAL",
    "SEQUENTIAL",
    "categorical",
    "__version__",
]
