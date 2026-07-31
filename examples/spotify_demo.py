"""Demo the bar and line helpers on real-world Spotify data.

Regenerate the data first if needed:  python data/spotify_stats.py
Then:                                  python examples/spotify_demo.py

Writes two PNGs next to this file.
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # headless

import pandas as pd

import spotviz as sv

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "data"


def main():
    # --- Bar: most-streamed songs, one bar highlighted -----------------------
    tracks = pd.read_csv(DATA / "top_streamed_tracks.csv")
    ax = sv.bar(
        tracks,
        x="track",
        y="streams_billions",
        sort="desc",
        highlight="Blinding Lights",       # the #1 pops in green; rest muted
        orient="horizontal",               # long song titles read better sideways
        label_values=True,
        title="Most-streamed songs on Spotify (all-time, billions)",
        xlabel="Cumulative streams (billions)",
        ylabel="",
    )
    sv.savefig(ax.figure, HERE / "spotify_top_tracks.png")
    print("wrote spotify_top_tracks.png")

    # --- Line: user growth, two series with direct labels --------------------
    growth = pd.read_csv(DATA / "spotify_user_growth.csv")
    ax = sv.line(
        growth,
        x="year",
        title="Spotify user growth (year-end, millions)",
        xlabel="Year",
        ylabel="Users (millions)",
    )
    sv.savefig(ax.figure, HERE / "spotify_user_growth.png")
    print("wrote spotify_user_growth.png")


if __name__ == "__main__":
    main()
