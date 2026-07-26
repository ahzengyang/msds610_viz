"""The ``line`` helper — trends over an ordered x, with direct labeling.

One series is drawn in Spotify Green (the resting look). Multiple series use the
categorical palette (green stays reserved), and — when there are only a few —
each line is labeled directly at its end instead of in a legend box, which is
easier to read. Pass ``highlight=`` to emphasize one series in green and mute
the rest.
"""

import matplotlib.pyplot as plt
import pandas as pd

from ._core import finalize, new_axes, sizes, theme_colors
from .palette import categorical


def line(
    data,
    x=None,
    y=None,
    *,
    ax=None,
    theme="dark",
    presentation=False,
    highlight=None,
    accent=None,
    direct_label=True,
    title=None,
    xlabel=None,
    ylabel=None,
    **kwargs,
):
    """Draw a clean, on-brand line chart from a DataFrame.

    Parameters
    ----------
    data : pandas.DataFrame or pandas.Series
        Series -> a single line over its index. DataFrame -> ``x=`` sets the
        x column (else the index is used) and ``y=`` selects the series
        column(s) to plot (else all numeric columns).
    x : str, optional
        Column to use for the x axis. Defaults to the index.
    y : str or list of str, optional
        Series column(s) to plot. Defaults to all numeric columns (minus x).
    ax : matplotlib.axes.Axes, optional
    theme : {"dark", "light"}, default "dark"
    presentation : bool, default False
    highlight : str, optional
        Series name to emphasize in green; the rest go muted gray.
    accent : str, optional
        Override the accent color. Defaults to Spotify Green.
    direct_label : bool, default True
        Label each series at its end instead of drawing a legend (used when
        there are at most 6 series).
    title : str, optional
    **kwargs
        Passed through to matplotlib's ``plot``.

    Returns
    -------
    matplotlib.axes.Axes
    """
    if isinstance(data, pd.Series):
        xvals = list(data.index)
        series = [(str(data.name or "value"), data.to_numpy())]
        x_auto = str(data.index.name or "")
    elif isinstance(data, pd.DataFrame):
        if x is not None:
            xvals = data[x].to_numpy()
            x_auto = str(x)
        else:
            xvals = list(data.index)
            x_auto = str(data.index.name or "")
        if y is None:
            cols = [c for c in data.select_dtypes("number").columns if c != x]
        else:
            cols = [y] if isinstance(y, str) else list(y)
        series = [(str(col), data[col].to_numpy()) for col in cols]
    else:
        raise TypeError(
            f"expected a pandas DataFrame or Series, got {type(data).__name__}."
        )

    if not series:
        raise ValueError("No numeric series found to plot.")

    c = theme_colors(theme)
    s = sizes(presentation)
    accent_color = accent if accent is not None else c["accent"]
    names = [n for n, _ in series]

    # Color assignment (green reserved for accent, never a categorical hue):
    #   1 series            -> green
    #   highlight given      -> green on it, muted gray on the rest
    #   several series       -> categorical palette
    if highlight is not None and str(highlight) in names:
        hi = str(highlight)
        colors = {n: (accent_color if n == hi else c["muted"]) for n in names}
        z = {n: (3 if n == hi else 1) for n in names}
    elif len(series) == 1:
        colors = {names[0]: accent_color}
        z = {names[0]: 3}
    else:
        pal = categorical(len(series))
        colors = {n: pal[i] for i, n in enumerate(names)}
        z = {n: 2 for n in names}

    ax, _created = new_axes(ax, presentation)
    for name, yvals in series:
        ax.plot(xvals, yvals, color=colors[name], linewidth=s["linewidth"],
                solid_capstyle="round", zorder=z[name], **kwargs)

    ax.set_xlabel(x_auto)
    if xlabel is not None:
        ax.set_xlabel(xlabel)
    if ylabel is not None:
        ax.set_ylabel(ylabel)
    ax.margins(x=0.02)
    finalize(ax, theme=theme, presentation=presentation, grid_axis="y",
             title=title)

    use_direct = direct_label and len(series) <= 6
    if use_direct:
        _direct_labels(ax, xvals, series, colors, presentation)
    elif len(series) > 1:
        leg = ax.legend(names, loc="best")
        for txt in leg.get_texts():
            txt.set_color(c["text"])

    return ax


def _direct_labels(ax, xvals, series, colors, presentation):
    """Label each series at its right end, nudged apart so they don't collide.

    End y-values are sorted and pushed upward to keep a minimum vertical gap;
    the y-limit is extended if the stack needs it. When a label is moved off its
    line's true endpoint, a thin leader line connects the two.
    """
    size = 13 if presentation else 10.5
    x_last = xvals[-1] if not isinstance(xvals[-1], str) else len(xvals) - 1

    ymin, ymax = ax.get_ylim()
    rng = (ymax - ymin) or 1.0
    min_gap = 0.052 * rng * (size / 10.5)  # minimum spacing between labels

    ends = sorted(((yvals[-1], name) for name, yvals in series),
                  key=lambda t: t[0])
    placed = []
    for y, name in ends:
        if placed and y - placed[-1][0] < min_gap:
            y = placed[-1][0] + min_gap
        placed.append((y, name))

    # Make room if the pushed-up stack overflows the top.
    top = placed[-1][0] if placed else ymax
    if top > ymax:
        ax.set_ylim(ymin, top + 0.03 * rng)

    label_y = {name: y for y, name in placed}
    y_end = {name: yvals[-1] for name, yvals in series}
    xr = (max(_as_num(xvals)) - min(_as_num(xvals))) or 1.0
    pad = 0.02 * xr

    for name in label_y:
        ly, ye = label_y[name], y_end[name]
        if abs(ly - ye) > 1e-9:  # moved -> draw a thin leader
            ax.plot([x_last, x_last + pad], [ye, ly],
                    color=colors[name], linewidth=0.9, alpha=0.55,
                    zorder=1, solid_capstyle="round")
        ax.annotate(
            f" {name}",
            xy=(x_last + pad, ly),
            xytext=(3, 0),
            textcoords="offset points",
            va="center",
            ha="left",
            color=colors[name],
            fontsize=size,
            fontweight="bold",
        )
    # Give the labels room on the right.
    ax.margins(x=0.14)


def _as_num(xvals):
    """x positions as numbers (categorical strings map to 0..n-1)."""
    if len(xvals) and isinstance(xvals[-1], str):
        return list(range(len(xvals)))
    return list(xvals)
