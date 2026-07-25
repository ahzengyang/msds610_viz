"""The ``scatter`` helper — position encoding, with honest area-scaled sizes.

Points are Spotify Green by default. When you map a column to marker size, the
value is scaled by **area** (matplotlib's ``s`` is area in points^2), not
radius, so magnitudes aren't visually exaggerated — you can't get this wrong.
Optionally color by a continuous column using viridis.
"""

import matplotlib.pyplot as plt

from ._core import finalize, new_axes, theme_colors
from .palette import SEQUENTIAL

# Marker area range (points^2) that size values map into.
_AREA_MIN = 30.0
_AREA_MAX = 600.0


def scatter(
    data,
    x,
    y,
    *,
    size=None,
    color=None,
    ax=None,
    theme="dark",
    presentation=False,
    accent=None,
    alpha=0.85,
    title=None,
    colorbar=True,
    **kwargs,
):
    """Draw a clean, on-brand scatter plot from a DataFrame.

    Parameters
    ----------
    data : pandas.DataFrame
    x, y : str
        Column names for the two position axes.
    size : str, optional
        Column mapped to marker size. Values are scaled by **area** so they are
        not exaggerated.
    color : str, optional
        Column mapped to a continuous viridis color. If omitted, points are
        Spotify Green.
    ax : matplotlib.axes.Axes, optional
    theme : {"dark", "light"}, default "dark"
    presentation : bool, default False
    accent : str, optional
        Override the point color (single-color case). Defaults to Spotify Green.
    alpha : float, default 0.85
    title : str, optional
    colorbar : bool, default True
        Draw a colorbar when ``color`` is given.
    **kwargs
        Passed through to matplotlib's ``scatter``.

    Returns
    -------
    matplotlib.axes.Axes
    """
    c = theme_colors(theme)
    xvals = data[x].to_numpy()
    yvals = data[y].to_numpy()

    # Area-proportional sizing: linearly map values into an *area* range, since
    # matplotlib's ``s`` already is area (points^2). area ∝ value, not radius.
    if size is not None:
        svals = data[size].to_numpy(dtype="float64")
        lo, hi = float(svals.min()), float(svals.max())
        if hi > lo:
            frac = (svals - lo) / (hi - lo)
        else:
            frac = svals * 0.0 + 0.5
        s_area = _AREA_MIN + frac * (_AREA_MAX - _AREA_MIN)
    else:
        s_area = 90.0 if not presentation else 140.0

    ax, _created = new_axes(ax, presentation)

    if color is not None:
        cvals = data[color].to_numpy()
        sc = ax.scatter(xvals, yvals, s=s_area, c=cvals, cmap=SEQUENTIAL,
                        alpha=alpha, edgecolors="none", **kwargs)
        if colorbar:
            cb = ax.figure.colorbar(sc, ax=ax, pad=0.02)
            cb.set_label(str(color), color=c["subtext"])
            cb.ax.yaxis.set_tick_params(color=c["subtext"], labelcolor=c["subtext"])
            cb.outline.set_edgecolor(c["spine"])
    else:
        point = accent if accent is not None else c["accent"]
        ax.scatter(xvals, yvals, s=s_area, color=point, alpha=alpha,
                   edgecolors="none", **kwargs)

    ax.set_xlabel(str(x))
    ax.set_ylabel(str(y))
    # Scatter reads best with no grid (or a faint one); default to none.
    finalize(ax, theme=theme, presentation=presentation, grid_axis=None,
             title=title)
    return ax
