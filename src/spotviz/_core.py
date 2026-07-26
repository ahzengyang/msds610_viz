"""Shared internals for spotviz chart helpers.

Colors and sizing per theme, plus a ``finalize`` routine that stamps the theme
onto an Axes. We stamp visual properties directly on the artists (facecolors,
text colors, tick colors, spines, grid) rather than relying only on a transient
rcParams context: matplotlib resolves many of those at *draw* time, so a theme
applied only while the figure is built would be lost by the time the user calls
``savefig``. Stamping keeps the look correct without mutating global state.
"""

import matplotlib.pyplot as plt
import pandas as pd

from .palette import ACCENT, APP_BG, BLACK, CATEGORICAL, WHITE

# Per-theme color roles. Grays are tuned for legibility on each ground.
THEME = {
    "dark": {
        "bg": APP_BG,          # #121212 near-black app background
        "surface": BLACK,      # #191414 alternate surface
        "text": WHITE,         # titles / primary text
        "subtext": "#B3B3B3",  # neutral "essential gray" — ticks, axis labels
        "muted": "#6B6B6B",    # de-emphasized marks (WCAG >=3:1 on near-black)
        "grid": "#2A2A2A",     # subtle low-contrast gridlines
        "spine": "#404040",    # baseline / axis line
        "accent": ACCENT,
    },
    "light": {
        "bg": WHITE,
        "surface": "#F5F5F5",
        "text": BLACK,
        "subtext": "#4D4D4D",
        "muted": "#C7C7C7",
        "grid": "#ECECEC",
        "spine": "#CCCCCC",
        "accent": ACCENT,
    },
}

# Font sizes and figure geometry per output mode.
SIZES = {
    False: {  # analytical / exploratory (default)
        "figsize": (8.0, 5.0),
        "dpi": 110,
        "title": 15,
        "label": 12,
        "tick": 10.5,
        "linewidth": 2.0,
    },
    True: {   # presentation / report — larger, 16:9, crisper
        "figsize": (12.0, 6.75),
        "dpi": 140,
        "title": 22,
        "label": 15,
        "tick": 13,
        "linewidth": 2.6,
    },
}


def theme_colors(theme="dark"):
    """Return the color-role dict for a theme name (falls back to dark)."""
    return THEME.get(theme, THEME["dark"])


def sizes(presentation=False):
    """Return the sizing dict for the output mode."""
    return SIZES[bool(presentation)]


def new_axes(ax, presentation=False):
    """Return (ax, created) — a new themed figure/axes if ``ax`` is None."""
    if ax is not None:
        return ax, False
    s = sizes(presentation)
    fig, ax = plt.subplots(figsize=s["figsize"], dpi=s["dpi"])
    return ax, True


def resolve_xy(data, x, y):
    """Normalize DataFrame/Series input into (x_values, y_values, xlabel, ylabel).

    Accepts:
    * a Series -> index is x, values are y (name -> ylabel);
    * a DataFrame with x=, y= column names;
    * a DataFrame with one numeric column and no x/y -> index is x.
    """
    if isinstance(data, pd.Series):
        xlabel = data.index.name or ""
        return list(data.index), data.to_numpy(), str(xlabel), str(data.name or "")

    if not isinstance(data, pd.DataFrame):
        raise TypeError(
            f"expected a pandas DataFrame or Series, got {type(data).__name__}."
        )

    if x is not None and y is not None:
        return (data[x].to_numpy(), data[y].to_numpy(), str(x), str(y))

    numeric = data.select_dtypes("number").columns.tolist()
    if len(numeric) == 1:
        col = numeric[0]
        xlabel = data.index.name or ""
        return list(data.index), data[col].to_numpy(), str(xlabel), str(col)

    raise ValueError(
        "Could not infer x and y. Pass x= and y= column names, or provide a "
        "Series / a DataFrame with a single numeric column."
    )


def finalize(ax, theme="dark", presentation=False, grid_axis="y", title=None):
    """Stamp the theme onto ``ax``: surfaces, text, spines, ticks, and grid."""
    c = theme_colors(theme)
    s = sizes(presentation)
    fig = ax.figure

    # Surfaces.
    fig.set_facecolor(c["bg"])
    ax.set_facecolor(c["bg"])

    # Title (left-aligned, bold, primary text color).
    if title is not None:
        ax.set_title(title, loc="left", color=c["text"],
                     fontsize=s["title"], fontweight="bold", pad=14)
    elif ax.get_title(loc="left"):
        ax.title.set_color(c["text"])

    # Axis labels.
    ax.xaxis.label.set_color(c["subtext"])
    ax.yaxis.label.set_color(c["subtext"])
    ax.xaxis.label.set_fontsize(s["label"])
    ax.yaxis.label.set_fontsize(s["label"])

    # Spines: drop top/right (and the bounding box); keep baseline subtle.
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(c["spine"])
        ax.spines[side].set_linewidth(0.8)

    # Ticks: no marks, muted labels.
    ax.tick_params(colors=c["subtext"], labelsize=s["tick"], length=0)
    for label in ax.get_xticklabels() + ax.get_yticklabels():
        label.set_color(c["subtext"])

    # Grid: subtle, behind the data, on one axis only (none if grid_axis=None).
    ax.set_axisbelow(True)
    ax.grid(False)
    if grid_axis in ("x", "y"):
        ax.grid(True, axis=grid_axis, color=c["grid"], linewidth=0.8)
    return ax


def savefig(fig, path):
    """Save preserving the themed (dark) background regardless of rcParams."""
    fig.savefig(path, facecolor=fig.get_facecolor())
