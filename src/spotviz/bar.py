"""The ``bar`` helper — a single-series bar chart, on-brand by default.

Bars encode with length from a zero baseline (accurate + honest). By default
every bar is the signature green — the resting brand look. Pass ``highlight=`` to get
the signature "one accent against muted grays" pattern: the chosen bar stays
green and the rest go muted gray.
"""

import matplotlib.pyplot as plt

from ._core import finalize, new_axes, resolve_xy, theme_colors


def bar(
    data,
    x=None,
    y=None,
    *,
    ax=None,
    theme="dark",
    presentation=False,
    highlight=None,
    accent=None,
    color=None,
    orient="vertical",
    sort=None,
    label_values=None,
    title=None,
    xlabel=None,
    ylabel=None,
    **kwargs,
):
    """Draw a clean, on-brand bar chart from a DataFrame or Series.

    Parameters
    ----------
    data : pandas.DataFrame or pandas.Series
        The data. A Series uses its index as categories; a DataFrame needs
        ``x=`` (categories) and ``y=`` (values), or a single numeric column.
    x, y : str, optional
        Category and value column names (DataFrame input).
    ax : matplotlib.axes.Axes, optional
        Axes to draw into; a new themed figure is created if omitted.
    theme : {"dark", "light"}, default "dark"
        Dark (default) or the light print variant.
    presentation : bool, default False
        Report/slide mode: larger type, 16:9, crisper.
    highlight : str or int, optional
        A category label or index to emphasize in green while the rest go gray.
    accent : str, optional
        Override the accent (highlight) color. Defaults to the signature green.
    color : str, optional
        Override the color of the non-highlighted bars.
    orient : {"vertical", "horizontal"}, default "vertical"
        Bar orientation. Horizontal reads well for ranked categories.
    sort : {None, "asc", "desc", True}, optional
        Sort bars by value. ``True`` means descending.
    label_values : bool, optional
        Draw value labels at the bar ends. Defaults to True in ``presentation``.
    title : str, optional
        Axes title (left-aligned).
    xlabel, ylabel : str, optional
        Override the auto axis labels (from the column names).
    **kwargs
        Passed through to matplotlib's ``bar``/``barh``.

    Returns
    -------
    matplotlib.axes.Axes
    """
    if orient not in ("vertical", "horizontal"):
        raise ValueError("orient must be 'vertical' or 'horizontal'.")

    cats, vals, x_auto, y_auto = resolve_xy(data, x, y)
    cats = [str(c) for c in cats]
    pairs = list(zip(cats, vals))

    if sort:
        reverse = sort in (True, "desc")
        pairs.sort(key=lambda p: p[1], reverse=reverse)
        cats, vals = [p[0] for p in pairs], [p[1] for p in pairs]

    c = theme_colors(theme)
    accent_color = accent if accent is not None else c["accent"]
    rest_color = color if color is not None else c["muted"]

    # No highlight -> all green (resting brand look). Highlight -> muted + one
    # green accent bar.
    if highlight is None:
        colors = [accent_color] * len(cats)
    else:
        if isinstance(highlight, int) and not isinstance(highlight, bool):
            hi = highlight % len(cats) if cats else None
        else:
            hi = cats.index(str(highlight)) if str(highlight) in cats else None
        colors = [accent_color if i == hi else rest_color
                  for i in range(len(cats))]

    if label_values is None:
        label_values = bool(presentation)

    ax, _created = new_axes(ax, presentation)
    positions = range(len(cats))

    if orient == "vertical":
        ax.bar(positions, vals, color=colors, width=0.72, **kwargs)
        ax.set_xticks(list(positions))
        ax.set_xticklabels(cats)
        ax.set_ylabel(y_auto)
        ax.margins(x=0.02)
        grid_axis = "y"
    else:
        ax.barh(positions, vals, color=colors, height=0.72, **kwargs)
        ax.set_yticks(list(positions))
        ax.set_yticklabels(cats)
        ax.set_xlabel(y_auto)
        ax.invert_yaxis()  # first category on top
        ax.margins(y=0.02)
        grid_axis = "x"

    # Explicit label overrides win over the auto-labels from the columns.
    if xlabel is not None:
        ax.set_xlabel(xlabel)
    if ylabel is not None:
        ax.set_ylabel(ylabel)

    finalize(ax, theme=theme, presentation=presentation,
             grid_axis=grid_axis, title=title)

    if label_values:
        _add_value_labels(ax, positions, vals, orient, theme, presentation)

    return ax


def _add_value_labels(ax, positions, vals, orient, theme, presentation):
    """Annotate bar ends with their values (report mode / opt-in)."""
    c = theme_colors(theme)
    size = 12 if presentation else 9.5
    vmax = max(vals) if len(vals) else 0
    pad = 0.01 * (vmax if vmax else 1)
    for pos, val in zip(positions, vals):
        text = f"{val:,.0f}" if abs(val) >= 100 else f"{val:,.2g}"
        if orient == "vertical":
            ax.text(pos, val + pad, text, ha="center", va="bottom",
                    color=c["text"], fontsize=size)
        else:
            ax.text(val + pad, pos, text, ha="left", va="center",
                    color=c["text"], fontsize=size)
