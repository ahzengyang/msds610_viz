"""cleanplot themes.

Themes are matplotlib style sheets that ship alongside this module and are the
single source of truth for each look. Two are provided:

* ``"cleanplot"`` (default) — a clean, minimal, colorblind-safe theme.
* ``"chinese"`` — a traditional Chinese ink-and-paper aesthetic (中国风): warm
  rice-paper surfaces, ink type, and a palette of traditional Chinese colors.

Every theme strips matplotlib's clutter (top/right spines, heavy gridlines,
long tick marks), sets legible typography, and configures a CJK-capable font
fallback so non-Latin text renders instead of blank boxes.

Ways to use a theme:

* ``plt.style.use("cleanplot")`` / ``plt.style.use("cleanplot-chinese")`` — the
  plain-matplotlib way. Importing ``cleanplot`` registers both names.
* ``style_context("chinese")`` — a context manager that applies a theme only
  for the block it wraps. cleanplot's chart helpers use this internally, so
  they never mutate your global matplotlib state unexpectedly.
* ``apply_style("chinese")`` — opt in globally for a whole session/script.
  Reversible with matplotlib's own ``matplotlib.rcdefaults()``.
"""

from pathlib import Path

import matplotlib as mpl
from matplotlib import style as _mpl_style

_HERE = Path(__file__).parent

#: Theme name -> shipped style-sheet path.
STYLE_PATHS = {
    "cleanplot": _HERE / "cleanplot.mplstyle",
    "chinese": _HERE / "chinese.mplstyle",
}

#: Theme name -> the name it is registered under for ``plt.style.use``.
_REGISTERED_NAMES = {
    "cleanplot": "cleanplot",
    "chinese": "cleanplot-chinese",
}

#: The default theme name.
DEFAULT_THEME = "cleanplot"
STYLE_NAME = _REGISTERED_NAMES[DEFAULT_THEME]

#: Theme name -> loaded rcParams. ``use_default_template=False`` keeps only the
#: keys each style sheet actually sets.
_RC = {
    name: mpl.rc_params_from_file(path, use_default_template=False)
    for name, path in STYLE_PATHS.items()
}

#: The default theme's rcParams, exposed for inspection/tweaking (back-compat).
RC_PARAMS = _RC[DEFAULT_THEME]

#: Path to the default theme's style sheet (back-compat).
STYLE_PATH = STYLE_PATHS[DEFAULT_THEME]

#: The theme names available.
THEMES = tuple(STYLE_PATHS)


def theme_rc(name=DEFAULT_THEME):
    """Return the rcParams dict for a theme name (falls back to the default)."""
    return _RC.get(name, _RC[DEFAULT_THEME])


def _register_styles():
    """Register every theme in matplotlib's style library.

    Makes ``plt.style.use("cleanplot")`` / ``"cleanplot-chinese"`` work without
    knowing the file path. Best-effort and idempotent.
    """
    try:
        for name, params in _RC.items():
            reg = _REGISTERED_NAMES[name]
            _mpl_style.library[reg] = dict(params)
            if reg not in _mpl_style.available:
                _mpl_style.available.append(reg)
        _mpl_style.available.sort()
    except Exception:
        # If matplotlib internals change, fall back to path-based use; the rest
        # of cleanplot still works via style_context()/apply_style().
        pass


_register_styles()


def stamp_fonts(ax, name=DEFAULT_THEME):
    """Pin the theme's font family onto the text artists of ``ax``.

    Font resolution happens at *draw* time, not when text is created. Because
    cleanplot's helpers style within a temporary rcParams context that has been
    exited by the time the user calls ``savefig``, the theme's CJK-capable font
    fallback would otherwise be lost and non-Latin text (e.g. Chinese) would
    render as blank "tofu" boxes. Stamping the font family directly on the Text
    artists makes it stick, and preserves matplotlib's per-glyph fallback so
    Latin text still renders normally.
    """
    fam = theme_rc(name).get("font.sans-serif")
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


def style_context(name=DEFAULT_THEME, overrides=None):
    """Return a context manager that applies a theme temporarily.

    Parameters
    ----------
    name : str, default "cleanplot"
        Theme name: ``"cleanplot"`` or ``"chinese"``.
    overrides : dict, optional
        Extra rcParams merged on top of the theme for this block.

    Examples
    --------
    >>> import matplotlib.pyplot as plt
    >>> from cleanplot import style_context
    >>> with style_context("chinese"):
    ...     fig, ax = plt.subplots()
    ...     ax.plot([0, 1], [0, 1])
    """
    params = dict(theme_rc(name))
    if overrides:
        params.update(overrides)
    return mpl.rc_context(params)


def apply_style(name=DEFAULT_THEME, overrides=None):
    """Apply a theme to matplotlib's global rcParams.

    Affects every subsequent plot in the session. Opt-in and fully reversible:
    call ``matplotlib.rcdefaults()`` to restore matplotlib's defaults.

    Parameters
    ----------
    name : str, default "cleanplot"
        Theme name: ``"cleanplot"`` or ``"chinese"``.
    overrides : dict, optional
        Extra rcParams merged on top of the theme.
    """
    mpl.rcParams.update(theme_rc(name))
    if overrides:
        mpl.rcParams.update(overrides)
