"""Example: a clean box plot of exam scores by course section.

Run from the project root (after `pip install -e .`):

    python examples/boxplot_example.py

Writes ``examples/boxplot_sections.png``.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

import cleanplot as cp

DATA = Path(__file__).resolve().parent.parent / "data" / "section_scores.csv"


def main():
    df = pd.read_csv(DATA)

    # Zero-config: pass the long-format frame, name the value column and the
    # grouping column. Axes label themselves from those column names.
    ax = cp.boxplot(
        df,
        column="score",
        by="section",
        highlight="Section C",   # one accent box against muted grays
        title="Exam scores by section",
    )

    out = Path(__file__).resolve().parent / "boxplot_sections.png"
    ax.figure.savefig(out)
    print(f"Saved {out}")


if __name__ == "__main__":
    main()
