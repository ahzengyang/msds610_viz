"""Generate a small, reproducible sample dataset for the cleanplot examples.

Uses only pandas and the Python standard library (``random``), consistent with
the project's pandas + matplotlib dependency constraint (no numpy import).

The dataset is exam scores for students across four course sections. Each
section has a different underlying score distribution, which makes it a good
fit for a box plot (comparing distributions across categories).

Run directly to (re)write ``data/section_scores.csv``:

    python data/generate_data.py
"""

import random
from pathlib import Path

import pandas as pd

# Per-section (mean, standard deviation, n students). Distinct centers and
# spreads so the box plot has something to show.
SECTIONS = {
    "Section A": (82.0, 6.0, 40),
    "Section B": (75.0, 11.0, 38),
    "Section C": (88.0, 4.5, 42),
    "Section D": (70.0, 14.0, 36),
}


def make_scores(seed=610):
    """Return a long-format DataFrame with columns ['section', 'score']."""
    rng = random.Random(seed)
    rows = []
    for section, (mean, sd, n) in SECTIONS.items():
        for _ in range(n):
            # Clamp to a plausible 0-100 exam range.
            score = min(100.0, max(0.0, rng.gauss(mean, sd)))
            rows.append({"section": section, "score": round(score, 1)})
    return pd.DataFrame(rows)


def main():
    df = make_scores()
    out = Path(__file__).parent / "section_scores.csv"
    df.to_csv(out, index=False)
    print(f"Wrote {len(df)} rows to {out}")
    print(df.groupby("section")["score"].describe()[["mean", "min", "max"]])


if __name__ == "__main__":
    main()
