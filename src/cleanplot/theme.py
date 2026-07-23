"""The cleanplot default theme.

The theme is expressed as a plain dict of matplotlib ``rcParams``. It strips
matplotlib's default clutter (top/right spines, heavy gridlines, long tick
marks), sets generous, legible typography, and installs the colorblind-safe
categorical palette as the default color cycle.

Two ways to use it:

* ``style_context()`` — a context manager that applies the theme only for the
  block it wraps. cleanplot's own chart helpers use this internally, so they
  never mutate your global matplotlib state unexpectedly.
* ``apply_style()`` — opt in globally for a whole session/script. Reversible
  with matplotlib's own ``matplotlib.rcdefaults()`` or ``style_context``.
"""

import matplotlib as mpl

from .palette import CATEGORICAL, GRAY_DARK, GRAY_LIGHT

#: The theme as matplotlib rcParams. Exposed so users can inspect or tweak it.
RC_PARAMS = {
    # --- figure -------------------------------------------------------------
    "figure.figsize": (8.0, 5.0),
    "figure.dpi": 110,
    "figure.facecolor": "white",
    "savefig.dpi": 200,
    "savefig.bbox": "tight",
    "savefig.facecolor": "white",

    # --- typography ---------------------------------------------------------
    "font.size": 11,
    "axes.titlesize": 14,
    "axes.labelsize": 11.5,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "legend.fontsize": 10,

    # --- color cycle --------------------------------------------------------
    "axes.prop_cycle": mpl.cycler(color=CATEGORICAL),

    # --- data-ink: spines ---------------------------------------------------
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.edgecolor": GRAY_DARK,
    "axes.linewidth": 0.8,

    # --- data-ink: title / label placement ----------------------------------
    "axes.titlelocation": "left",
    "axes.titlepad": 12.0,
    "axes.titleweight": "bold",
    "axes.labelpad": 6.0,
    "axes.labelcolor": GRAY_DARK,
    "text.color": GRAY_DARK,

    # --- data-ink: gridlines (light, y-only, behind the data) ---------------
    "axes.grid": True,
    "axes.grid.axis": "y",
    "axes.axisbelow": True,
    "grid.color": GRAY_LIGHT,
    "grid.linewidth": 0.8,
    "grid.linestyle": "-",

    # --- data-ink: ticks (short, thin, muted) -------------------------------
    "xtick.color": GRAY_DARK,
    "ytick.color": GRAY_DARK,
    "xtick.major.size": 0.0,
    "ytick.major.size": 0.0,
    "xtick.major.width": 0.8,
    "ytick.major.width": 0.8,
    "xtick.major.pad": 6.0,
    "ytick.major.pad": 6.0,

    # --- legend -------------------------------------------------------------
    "legend.frameon": False,
    "legend.borderaxespad": 0.0,
}


def style_context(overrides=None):
    """Return a context manager that applies the cleanplot theme temporarily.

    Parameters
    ----------
    overrides : dict, optional
        Extra rcParams merged on top of the theme for this block.

    Examples
    --------
    >>> import matplotlib.pyplot as plt
    >>> from cleanplot.theme import style_context
    >>> with style_context():
    ...     fig, ax = plt.subplots()
    ...     ax.plot([0, 1], [0, 1])
    """
    params = dict(RC_PARAMS)
    if overrides:
        params.update(overrides)
    return mpl.rc_context(params)


def apply_style(overrides=None):
    """Apply the cleanplot theme to matplotlib's global rcParams.

    Affects every subsequent plot in the session. This is opt-in and fully
    reversible: call ``matplotlib.rcdefaults()`` to restore matplotlib's
    defaults.

    Parameters
    ----------
    overrides : dict, optional
        Extra rcParams merged on top of the theme.
    """
    mpl.rcParams.update(RC_PARAMS)
    if overrides:
        mpl.rcParams.update(overrides)
