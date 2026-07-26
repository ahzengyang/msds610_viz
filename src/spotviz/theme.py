"""spotviz themes as matplotlib rcParams / named styles.

The chart helpers style their own output directly, but this module lets you
apply the signature look to *any* matplotlib code — via a context manager, a
global opt-in, or a named style:

    import spotviz
    import matplotlib.pyplot as plt
    plt.style.use("spotviz-dark")          # or "spotviz-light"

    with spotviz.theme_context("dark"):    # scoped
        ...

    spotviz.apply_theme("dark")            # global, reversible via rcdefaults()
"""

import matplotlib as mpl
from matplotlib import style as _mpl_style

from ._core import sizes, theme_colors
from .palette import CATEGORICAL


def rc_params(theme="dark", presentation=False):
    """Build the rcParams dict for a theme + output mode."""
    c = theme_colors(theme)
    s = sizes(presentation)
    return {
        # surfaces
        "figure.facecolor": c["bg"],
        "axes.facecolor": c["bg"],
        "savefig.facecolor": c["bg"],
        "figure.figsize": s["figsize"],
        "figure.dpi": s["dpi"],
        "savefig.dpi": s["dpi"] + 60,
        "savefig.bbox": "tight",
        # text
        "text.color": c["text"],
        "axes.titlecolor": c["text"],
        "axes.titlesize": s["title"],
        "axes.titleweight": "bold",
        "axes.titlelocation": "left",
        "axes.titlepad": 14.0,
        "axes.labelcolor": c["subtext"],
        "axes.labelsize": s["label"],
        "xtick.color": c["subtext"],
        "ytick.color": c["subtext"],
        "xtick.labelsize": s["tick"],
        "ytick.labelsize": s["tick"],
        "xtick.labelcolor": c["subtext"],
        "ytick.labelcolor": c["subtext"],
        "font.size": s["label"],
        # color cycle (categorical; green stays reserved for accent)
        "axes.prop_cycle": mpl.cycler(color=CATEGORICAL),
        "lines.linewidth": s["linewidth"],
        # spines / declutter
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.edgecolor": c["spine"],
        "axes.linewidth": 0.8,
        # ticks
        "xtick.major.size": 0.0,
        "ytick.major.size": 0.0,
        # grid
        "axes.grid": True,
        "axes.grid.axis": "y",
        "axes.axisbelow": True,
        "grid.color": c["grid"],
        "grid.linewidth": 0.8,
        # legend
        "legend.frameon": False,
        "legend.labelcolor": c["text"],
    }


# Register named styles for plt.style.use(...).
_REGISTERED = {
    "spotviz-dark": rc_params("dark", False),
    "spotviz-light": rc_params("light", False),
    "spotviz-dark-report": rc_params("dark", True),
    "spotviz-light-report": rc_params("light", True),
}


def _register():
    try:
        for name, params in _REGISTERED.items():
            _mpl_style.library[name] = dict(params)
            if name not in _mpl_style.available:
                _mpl_style.available.append(name)
        _mpl_style.available.sort()
    except Exception:
        pass


_register()

#: Available theme names.
THEMES = ("dark", "light")


def theme_context(theme="dark", presentation=False, overrides=None):
    """Context manager applying the signature theme to plain matplotlib code."""
    params = rc_params(theme, presentation)
    if overrides:
        params.update(overrides)
    return mpl.rc_context(params)


def apply_theme(theme="dark", presentation=False, overrides=None):
    """Apply the signature theme globally (reversible via ``matplotlib.rcdefaults()``)."""
    mpl.rcParams.update(rc_params(theme, presentation))
    if overrides:
        mpl.rcParams.update(overrides)
