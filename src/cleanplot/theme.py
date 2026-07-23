"""The cleanplot default theme.

The theme is defined in a matplotlib style sheet, ``cleanplot.mplstyle``, which
ships alongside this module and is the single source of truth. It strips
matplotlib's default clutter (top/right spines, heavy gridlines, long tick
marks), sets generous, legible typography, installs the colorblind-safe
categorical palette as the color cycle, and configures a CJK-capable font
fallback so Chinese (and other non-Latin) text renders instead of blank boxes.

Three ways to use it:

* ``plt.style.use("cleanplot")`` — the plain-matplotlib way. Importing
  ``cleanplot`` registers the style under this name.
* ``style_context()`` — a context manager that applies the theme only for the
  block it wraps. cleanplot's own chart helpers use this internally, so they
  never mutate your global matplotlib state unexpectedly.
* ``apply_style()`` — opt in globally for a whole session/script. Reversible
  with matplotlib's own ``matplotlib.rcdefaults()``.
"""

from pathlib import Path

import matplotlib as mpl
from matplotlib import style as _mpl_style

#: Path to the shipped style sheet.
STYLE_PATH = Path(__file__).with_name("cleanplot.mplstyle")

#: The theme as matplotlib rcParams, loaded from the style sheet. Exposed so
#: users can inspect or tweak it. ``use_default_template=False`` keeps only the
#: keys the style sheet actually sets.
RC_PARAMS = mpl.rc_params_from_file(STYLE_PATH, use_default_template=False)

#: The name the style is registered under for ``plt.style.use``.
STYLE_NAME = "cleanplot"


def _register_style():
    """Register the theme in matplotlib's style library as ``cleanplot``.

    Makes ``plt.style.use("cleanplot")`` work without knowing the file path.
    Best-effort and idempotent; safe to call more than once.
    """
    try:
        _mpl_style.library[STYLE_NAME] = dict(RC_PARAMS)
        # Keep the public ``available`` list in sync.
        if STYLE_NAME not in _mpl_style.available:
            _mpl_style.available.append(STYLE_NAME)
            _mpl_style.available.sort()
    except Exception:
        # If matplotlib's internals change, fall back to path-based use; the
        # rest of cleanplot still works via style_context()/apply_style().
        pass


_register_style()


def stamp_fonts(ax):
    """Pin the theme's font family onto the text artists of ``ax``.

    Font resolution happens at *draw* time, not when text is created. Because
    cleanplot's helpers style within a temporary rcParams context that has been
    exited by the time the user calls ``savefig``, the theme's CJK-capable font
    fallback would otherwise be lost and non-Latin text (e.g. Chinese) would
    render as blank "tofu" boxes. Stamping the font family directly on the Text
    artists makes it stick, and preserves matplotlib's per-glyph fallback so
    Latin text still renders normally.
    """
    fam = RC_PARAMS.get("font.sans-serif")
    if not fam:
        return
    fam = list(fam)
    texts = [ax.xaxis.label, ax.yaxis.label]
    # Titles: with titlelocation="left" the text lives on the left title slot,
    # not the centered ax.title, so stamp all three defensively.
    for attr in ("title", "_left_title", "_right_title"):
        title = getattr(ax, attr, None)
        if title is not None:
            texts.append(title)
    texts += list(ax.get_xticklabels()) + list(ax.get_yticklabels())
    legend = ax.get_legend()
    if legend is not None:
        texts += list(legend.get_texts())
    for text in texts:
        text.set_fontfamily(fam)


def style_context(overrides=None):
    """Return a context manager that applies the cleanplot theme temporarily.

    Parameters
    ----------
    overrides : dict, optional
        Extra rcParams merged on top of the theme for this block.

    Examples
    --------
    >>> import matplotlib.pyplot as plt
    >>> from cleanplot import style_context
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
