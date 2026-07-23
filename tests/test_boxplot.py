"""Basic smoke tests for cleanplot.boxplot.

Run with: python -m pytest  (or: python tests/test_boxplot.py)
Uses matplotlib's non-interactive Agg backend so it runs headless.
"""

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd

import cleanplot as cp


def _wide_df():
    return pd.DataFrame({"A": [1, 2, 3, 4, 5], "B": [2, 4, 6, 8, 20]})


def _long_df():
    return pd.DataFrame(
        {
            "section": ["x", "x", "x", "y", "y", "y"],
            "score": [1.0, 2.0, 3.0, 4.0, 5.0, 6.0],
        }
    )


def test_wide_one_box_per_numeric_column():
    ax = cp.boxplot(_wide_df())
    labels = [t.get_text() for t in ax.get_xticklabels()]
    assert labels == ["A", "B"]
    plt.close(ax.figure)


def test_long_grouped_by_column():
    ax = cp.boxplot(_long_df(), column="score", by="section")
    labels = [t.get_text() for t in ax.get_xticklabels()]
    assert labels == ["x", "y"]
    assert ax.get_xlabel() == "section"
    assert ax.get_ylabel() == "score"
    plt.close(ax.figure)


def test_series_single_box():
    s = pd.Series([1, 2, 3, 4], name="height")
    ax = cp.boxplot(s)
    assert [t.get_text() for t in ax.get_xticklabels()] == ["height"]
    plt.close(ax.figure)


def test_returns_axes_and_respects_passed_ax():
    fig, ax = plt.subplots()
    returned = cp.boxplot(_wide_df(), ax=ax)
    assert returned is ax
    plt.close(fig)


def test_highlight_sets_one_accent_box():
    ax = cp.boxplot(_long_df(), column="score", by="section", highlight="y")
    faces = [tuple(p.get_facecolor()) for p in ax.patches]
    # Two boxes, distinct fills (one accent, one muted gray).
    assert len(faces) == 2
    assert faces[0] != faces[1]
    plt.close(ax.figure)


def test_horizontal_orientation():
    ax = cp.boxplot(_long_df(), column="score", by="section", orient="horizontal")
    assert ax.get_ylabel() == "section"
    assert ax.get_xlabel() == "score"
    plt.close(ax.figure)


def test_named_style_registered():
    # Importing cleanplot registers the theme under a name for plt.style.use.
    assert cp.STYLE_NAME in plt.style.available
    assert cp.STYLE_PATH.exists()


def test_cjk_font_stamped_on_labels():
    # The theme font (with CJK fallback) must be pinned onto the text artists
    # so Chinese labels survive to draw time instead of reverting to a
    # Latin-only default font.
    df = pd.DataFrame({"班级": ["甲", "甲", "乙", "乙"], "成绩": [1.0, 2.0, 3.0, 4.0]})
    ax = cp.boxplot(df, column="成绩", by="班级", title="标题")
    expected = list(cp.RC_PARAMS["font.sans-serif"])
    for label in (ax.xaxis.label, ax.yaxis.label):
        assert list(label.get_fontfamily()) == expected
    # Title (left-located) must be stamped too.
    left_title = getattr(ax, "_left_title", None) or ax.title
    assert list(left_title.get_fontfamily()) == expected
    plt.close(ax.figure)


def test_unicode_minus_disabled_in_theme():
    # CJK fonts often lack a proper minus glyph; the theme uses ASCII hyphen.
    assert cp.RC_PARAMS["axes.unicode_minus"] is False


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"ok  {name}")
    print("all tests passed")
