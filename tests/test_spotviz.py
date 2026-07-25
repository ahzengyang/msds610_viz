"""Smoke + behavior tests for spotviz.

Run with: python -m pytest  (or: python tests/test_spotviz.py)
Uses matplotlib's headless Agg backend.
"""

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.colors import to_rgba
import pandas as pd

import spotviz as sv


def _genres():
    return pd.DataFrame({
        "genre": ["Pop", "Rock", "Jazz"],
        "streams": [9.0, 5.0, 1.0],
    })


def _listeners():
    return pd.DataFrame({
        "month": ["Jan", "Feb", "Mar"],
        "A": [1.0, 2.0, 3.0],
        "B": [3.0, 2.5, 2.0],
        "C": [2.0, 2.2, 2.4],
    })


def _tracks():
    return pd.DataFrame({
        "energy": [0.2, 0.5, 0.9],
        "dance": [0.3, 0.6, 0.8],
        "pop": [10, 50, 100],
    })


# --- palette / brand rules ---------------------------------------------------

def test_green_reserved_not_in_categorical():
    green = to_rgba(sv.GREEN)
    cat = {to_rgba(c) for c in sv.CATEGORICAL}
    assert green not in cat


def test_named_styles_registered():
    for name in ("spotify-dark", "spotify-light",
                 "spotify-dark-report", "spotify-light-report"):
        assert name in plt.style.available


# --- bar ---------------------------------------------------------------------

def test_bar_returns_axes_and_labels():
    ax = sv.bar(_genres(), x="genre", y="streams")
    assert [t.get_text() for t in ax.get_xticklabels()] == ["Pop", "Rock", "Jazz"]
    plt.close(ax.figure)


def test_bar_no_highlight_is_all_green():
    ax = sv.bar(_genres(), x="genre", y="streams")
    green = to_rgba(sv.GREEN)
    assert all(tuple(p.get_facecolor()) == green for p in ax.patches)
    plt.close(ax.figure)


def test_bar_highlight_greens_one_bar_mutes_rest():
    ax = sv.bar(_genres(), x="genre", y="streams", highlight="Rock")
    green = to_rgba(sv.GREEN)
    greens = [p for p in ax.patches if tuple(p.get_facecolor()) == green]
    assert len(greens) == 1
    plt.close(ax.figure)


def test_bar_sort_desc_orders_by_value():
    df = pd.DataFrame({"g": ["a", "b", "c"], "v": [1, 3, 2]})
    ax = sv.bar(df, x="g", y="v", sort="desc")
    assert [t.get_text() for t in ax.get_xticklabels()] == ["b", "c", "a"]
    plt.close(ax.figure)


def test_bar_starts_at_zero():
    ax = sv.bar(_genres(), x="genre", y="streams")
    assert ax.get_ylim()[0] <= 0  # honest baseline, not truncated
    plt.close(ax.figure)


# --- line --------------------------------------------------------------------

def test_line_multiseries_uses_categorical_not_green():
    ax = sv.line(_listeners(), x="month")
    green = to_rgba(sv.GREEN)
    line_colors = [to_rgba(ln.get_color()) for ln in ax.get_lines()]
    assert green not in line_colors
    assert len(line_colors) == 3
    plt.close(ax.figure)


def test_line_highlight_greens_one_series():
    ax = sv.line(_listeners(), x="month", highlight="A")
    green = to_rgba(sv.GREEN)
    greens = [ln for ln in ax.get_lines() if to_rgba(ln.get_color()) == green]
    assert len(greens) == 1
    plt.close(ax.figure)


# --- scatter -----------------------------------------------------------------

def test_scatter_size_scales_by_area_monotonically():
    ax = sv.scatter(_tracks(), x="energy", y="dance", size="pop")
    coll = ax.collections[0]
    areas = list(coll.get_sizes())
    # Larger popularity -> larger area, strictly increasing here.
    assert areas[0] < areas[1] < areas[2]
    plt.close(ax.figure)


def test_scatter_default_is_green():
    ax = sv.scatter(_tracks(), x="energy", y="dance")
    coll = ax.collections[0]
    assert tuple(coll.get_facecolor()[0]) == to_rgba(sv.GREEN, 0.85)
    plt.close(ax.figure)


# --- theme -------------------------------------------------------------------

def test_light_theme_has_white_background():
    ax = sv.bar(_genres(), x="genre", y="streams", theme="light")
    assert tuple(ax.get_facecolor()) == to_rgba("#FFFFFF")
    plt.close(ax.figure)


def test_dark_theme_has_near_black_background():
    ax = sv.bar(_genres(), x="genre", y="streams")  # dark is default
    assert tuple(ax.get_facecolor()) == to_rgba("#121212")
    plt.close(ax.figure)


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"ok  {name}")
    print("all tests passed")
