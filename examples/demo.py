"""spotviz demo — bar, line, and scatter across the Spotify themes.

Run from the project root (after ``pip install -e .``):

    python examples/demo.py

Writes PNGs into ``examples/``.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

import spotviz as sv

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "data"


def main():
    genres = pd.read_csv(DATA / "genre_streams.csv")
    genres["streams_bn"] = genres["streams"] / 1e9
    listeners = pd.read_csv(DATA / "monthly_listeners.csv")
    tracks = pd.read_csv(DATA / "tracks.csv")

    # 1) Bar (dark, default): highlight one category in green, rest muted.
    ax = sv.bar(genres, x="genre", y="streams_bn", sort="desc",
                highlight="Pop", title="Streams by genre",
                ylabel="Streams (billions)")
    sv.savefig(ax.figure, HERE / "bar_dark.png")
    plt.close(ax.figure)

    # 2) Bar (report/presentation): horizontal, sorted, value labels.
    ax = sv.bar(genres, x="genre", y="streams_bn", sort="desc",
                orient="horizontal", presentation=True,
                highlight="Pop", title="Streams by genre",
                xlabel="Streams (billions)")
    sv.savefig(ax.figure, HERE / "bar_report.png")
    plt.close(ax.figure)

    # 3) Line (dark): multi-series with the categorical palette + direct labels.
    ax = sv.line(listeners, x="month",
                 title="Monthly listeners",
                 xlabel="Month", ylabel="Listeners (millions)")
    sv.savefig(ax.figure, HERE / "line_dark.png")
    plt.close(ax.figure)

    # 4) Line (dark): emphasize one series in green, mute the rest.
    ax = sv.line(listeners, x="month", highlight="Aurora Skye",
                 title="Monthly listeners — Aurora Skye leads",
                 xlabel="Month", ylabel="Listeners (millions)")
    sv.savefig(ax.figure, HERE / "line_highlight.png")
    plt.close(ax.figure)

    # 5) Scatter (dark): size by area, color by a continuous feature (viridis).
    ax = sv.scatter(tracks, x="energy", y="danceability",
                    size="popularity", color="popularity",
                    title="Audio features (size & color = popularity)",
                    xlabel="Energy", ylabel="Danceability")
    sv.savefig(ax.figure, HERE / "scatter_dark.png")
    plt.close(ax.figure)

    # 6) Light variant: same bar, one argument away.
    ax = sv.bar(genres, x="genre", y="streams_bn", sort="desc",
                theme="light", highlight="Pop",
                title="Streams by genre — light theme",
                ylabel="Streams (billions)")
    sv.savefig(ax.figure, HERE / "bar_light.png")
    plt.close(ax.figure)

    print("Saved bar_dark, bar_report, line_dark, line_highlight, "
          "scatter_dark, bar_light")


if __name__ == "__main__":
    main()
