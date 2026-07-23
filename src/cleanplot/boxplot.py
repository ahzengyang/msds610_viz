"""The ``boxplot`` chart helper.

A box plot summarizes a distribution with position and length (quartiles,
whiskers) rather than area or angle, so it fits cleanplot's "encode for how
humans perceive" philosophy well. This helper:

* accepts pandas DataFrames and Series naturally, in either "wide" form (one
  numeric column per box) or "long" form (values in one column, groups in
  another via ``by=``);
* labels axes and ticks automatically from column names;
* styles the boxes with the clean theme and a single muted color, with an
  optional accent color to highlight one group;
* returns the matplotlib ``Axes`` so you can keep customizing.
"""

import matplotlib.pyplot as plt
import pandas as pd

from .palette import theme_colors
from .theme import DEFAULT_THEME, stamp_fonts, style_context


def _series_to_groups(data, column, by):
    """Normalize the many accepted input shapes into (labels, sequences).

    Returns
    -------
    labels : list of str
        One label per box.
    values : list of sequences
        The numeric values for each box (NaNs dropped).
    value_name : str or None
        Name for the value axis (e.g. the measured column).
    group_name : str or None
        Name for the category axis (e.g. the grouping column).
    """
    # Series -> a single box.
    if isinstance(data, pd.Series):
        label = data.name if data.name is not None else "value"
        return [str(label)], [data.dropna().to_numpy()], str(label), None

    if not isinstance(data, pd.DataFrame):
        raise TypeError(
            "boxplot expects a pandas DataFrame or Series, got "
            f"{type(data).__name__}."
        )

    # Long form: one value column split into groups by another column.
    if by is not None:
        if column is None:
            numeric = data.select_dtypes("number").columns.tolist()
            numeric = [c for c in numeric if c != by]
            if len(numeric) != 1:
                raise ValueError(
                    "With by=, either pass column= explicitly or make sure the "
                    "DataFrame has exactly one numeric column to plot; found "
                    f"{numeric}."
                )
            column = numeric[0]
        labels, values = [], []
        # sort=False keeps the natural first-seen group order.
        for key, sub in data.groupby(by, sort=False):
            labels.append(str(key))
            values.append(sub[column].dropna().to_numpy())
        return labels, values, str(column), str(by)

    # Wide form: one box per (selected) numeric column.
    if column is not None:
        cols = [column] if isinstance(column, str) else list(column)
    else:
        cols = data.select_dtypes("number").columns.tolist()
        if not cols:
            raise ValueError("No numeric columns found to plot.")
    labels = [str(c) for c in cols]
    values = [data[c].dropna().to_numpy() for c in cols]
    value_name = str(cols[0]) if len(cols) == 1 else None
    return labels, values, value_name, None


def boxplot(
    data,
    column=None,
    by=None,
    *,
    ax=None,
    theme=DEFAULT_THEME,
    orient="vertical",
    accent=None,
    highlight=None,
    color=None,
    showfliers=True,
    title=None,
    **kwargs,
):
    """Draw a clean, self-labeling box plot from a DataFrame or Series.

    Parameters
    ----------
    data : pandas.DataFrame or pandas.Series
        The data to summarize. In "wide" form each selected numeric column
        becomes one box. In "long" form pass ``by=`` to split a value column
        into one box per group.
    column : str or list of str, optional
        Which column(s) hold the values. In wide form, the column(s) to draw
        (defaults to all numeric columns). In long form (with ``by=``), the
        single value column (defaults to the one numeric column present).
    by : str, optional
        Column to group by (long form). One box is drawn per distinct value.
    ax : matplotlib.axes.Axes, optional
        Axes to draw into. If ``None``, a new figure and axes are created using
        the selected theme.
    theme : str, default "cleanplot"
        Theme name driving the muted/accent colors and (when creating a new
        figure) the styling: ``"cleanplot"`` or ``"chinese"``.
    orient : {"vertical", "horizontal"}, default "vertical"
        Box orientation.
    accent : str, optional
        Accent color for the highlighted box (see ``highlight``). Defaults to
        the theme's accent color when ``highlight`` is given.
    highlight : str or int, optional
        A group label or positional index to emphasize with the accent color
        while the rest stay muted gray. Directs the eye with contrast.
    color : str, optional
        Override the muted fill color used for all (non-highlighted) boxes.
    showfliers : bool, default True
        Whether to draw outlier points. They are drawn small and muted so they
        don't dominate.
    title : str, optional
        Axes title. If omitted, no title is set (you can add one later).
    **kwargs
        Passed through to matplotlib's ``Axes.boxplot`` (user intent wins).

    Returns
    -------
    matplotlib.axes.Axes
        The axes the box plot was drawn on.

    Examples
    --------
    >>> import pandas as pd, cleanplot as cp
    >>> df = pd.DataFrame({"A": [1, 2, 3, 4], "B": [2, 3, 4, 9]})
    >>> ax = cp.boxplot(df)                       # one box per column
    >>> ax = cp.boxplot(df_long, column="score", by="section")  # grouped
    """
    if orient not in ("vertical", "horizontal"):
        raise ValueError("orient must be 'vertical' or 'horizontal'.")

    labels, values, value_name, group_name = _series_to_groups(data, column, by)
    vertical = orient == "vertical"

    # Theme-driven colors: muted neutral fill, one accent, ink/mid line colors.
    colors = theme_colors(theme)
    ink, mid = colors["ink"], colors["mid"]
    base_color = color if color is not None else colors["neutral"]

    # Resolve which box (if any) to highlight, by label or index.
    hi_index = None
    if highlight is not None:
        if isinstance(highlight, int) and not isinstance(highlight, bool):
            if -len(labels) <= highlight < len(labels):
                hi_index = highlight % len(labels)
        elif str(highlight) in labels:
            hi_index = labels.index(str(highlight))
    hi_color = accent if accent is not None else colors["accent"]

    def _draw(target_ax):
        bp = target_ax.boxplot(
            values,
            vert=vertical,
            tick_labels=labels,
            patch_artist=True,          # filled boxes so we can color them
            widths=0.6,
            showfliers=showfliers,
            medianprops={"color": ink, "linewidth": 1.6},
            whiskerprops={"color": mid, "linewidth": 1.0},
            capprops={"color": mid, "linewidth": 1.0},
            flierprops={
                "marker": "o",
                "markersize": 3,
                "markerfacecolor": mid,
                "markeredgecolor": "none",
                "alpha": 0.6,
            },
            **kwargs,
        )
        # Color the box fills: muted by default, accent on the highlighted one.
        for i, patch in enumerate(bp["boxes"]):
            emphasized = i == hi_index
            patch.set_facecolor(hi_color if emphasized else base_color)
            patch.set_edgecolor(ink if emphasized else mid)
            patch.set_linewidth(1.2 if emphasized else 1.0)
            patch.set_alpha(1.0 if emphasized else 0.9)

        # Self-labeling from column names. The category axis carries the group
        # name; the value axis carries the measured column name.
        cat_label = group_name
        val_label = value_name
        if vertical:
            if cat_label:
                target_ax.set_xlabel(cat_label)
            if val_label:
                target_ax.set_ylabel(val_label)
        else:
            if cat_label:
                target_ax.set_ylabel(cat_label)
            if val_label:
                target_ax.set_xlabel(val_label)
            # Horizontal box plots read top-to-bottom in data order.
            target_ax.invert_yaxis()
            # Grid belongs on the value axis, which is now x.
            target_ax.grid(axis="x", visible=True)
            target_ax.grid(axis="y", visible=False)

        if title is not None:
            target_ax.set_title(title)

        # Pin the theme font onto the labels we just created so non-Latin text
        # (e.g. Chinese) survives to draw time instead of reverting to the
        # default font and rendering as tofu boxes.
        stamp_fonts(target_ax, theme)
        return target_ax

    # Only wrap figure creation in the theme so we never mutate a user's global
    # state or restyle axes they passed in.
    if ax is None:
        with style_context(theme):
            _fig, ax = plt.subplots()
            _draw(ax)
    else:
        _draw(ax)
    return ax
