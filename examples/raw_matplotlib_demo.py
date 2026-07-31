"""Raw matplotlib baseline for the same two datasets spotviz styles.

This is the "before" in a before/after comparison: it uses matplotlib's
out-of-the-box defaults with no spotviz theming, so you can see exactly what
the library adds (color identity, decluttering, direct labels, honest sizing).

Renders side-by-side against examples/spotify_demo.py, which plots the same
CSVs with spotviz.

Run:  python examples/raw_matplotlib_demo.py
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # headless

import matplotlib.pyplot as plt
import pandas as pd

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "data"


def raw_bar():
    """Most-streamed songs, plain matplotlib horizontal bar chart."""
    tracks = pd.read_csv(DATA / "top_streamed_tracks.csv")
    tracks = tracks.sort_values("streams_billions")  # barh reads bottom-up

    fig, ax = plt.subplots()
    ax.barh(tracks["track"], tracks["streams_billions"])
    ax.set_title("Most-streamed songs on Spotify (all-time, billions)")
    ax.set_xlabel("streams_billions")

    fig.savefig(HERE / "raw_top_tracks.png")
    plt.close(fig)
    print("wrote raw_top_tracks.png")


def raw_line():
    """Spotify user growth, plain matplotlib multi-line chart with a legend."""
    growth = pd.read_csv(DATA / "spotify_user_growth.csv")

    fig, ax = plt.subplots()
    ax.plot(growth["year"], growth["MAU"], label="MAU")
    ax.plot(growth["year"], growth["Premium"], label="Premium")
    ax.set_title("Spotify user growth (year-end, millions)")
    ax.set_xlabel("year")
    ax.set_ylabel("Users (millions)")
    ax.legend()

    fig.savefig(HERE / "raw_user_growth.png")
    plt.close(fig)
    print("wrote raw_user_growth.png")


def main():
    raw_bar()
    raw_line()


if __name__ == "__main__":
    main()
