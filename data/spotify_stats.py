"""Build two small, real-world demo datasets for the bar and line helpers.

Unlike ``generate_data.py`` (which synthesizes random sample data), this script
writes *real*, publicly reported figures so the charts read as a recognizable
demo. Values are approximate public snapshots, rounded, and meant to be
illustrative — not an authoritative data source:

- ``top_streamed_tracks.csv`` — most-streamed songs on Spotify of all time,
  cumulative streams in billions (public streaming trackers, ~2024). Good for a
  single-series bar chart with one bar highlighted.
- ``spotify_user_growth.csv`` — Spotify's year-end Monthly Active Users (MAU)
  and Premium Subscribers, in millions (Spotify quarterly earnings reports).
  Good for a two-series line chart with direct labels.

Only pandas + the standard library are used, matching the library's deps.
Run:  python data/spotify_stats.py
"""

from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent


# --- Bar: most-streamed songs of all time (cumulative streams, billions) -----
# Approximate all-time Spotify stream counts, rounded to 0.1B.
TOP_TRACKS = [
    ("Blinding Lights",  "The Weeknd",                 4.6),
    ("Shape of You",     "Ed Sheeran",                 4.0),
    ("Sunflower",        "Post Malone & Swae Lee",     3.6),
    ("Someone You Loved","Lewis Capaldi",              3.4),
    ("As It Was",        "Harry Styles",               3.3),
    ("Starboy",          "The Weeknd",                 3.3),
    ("Sweater Weather",  "The Neighbourhood",          3.2),
    ("Dance Monkey",     "Tones and I",                3.1),
]


# --- Line: Spotify user growth, year-end, millions -----------------------------
# Year-end Monthly Active Users (MAU) and Premium Subscribers, in millions.
USER_GROWTH = [
    # year,  MAU,  Premium
    (2015,    91,   28),
    (2016,   123,   48),
    (2017,   160,   71),
    (2018,   207,   96),
    (2019,   271,  124),
    (2020,   345,  155),
    (2021,   406,  180),
    (2022,   489,  205),
    (2023,   602,  236),
    (2024,   675,  263),
]


def main():
    tracks = pd.DataFrame(TOP_TRACKS, columns=["track", "artist", "streams_billions"])
    tracks.to_csv(HERE / "top_streamed_tracks.csv", index=False)

    growth = pd.DataFrame(USER_GROWTH, columns=["year", "MAU", "Premium"])
    growth.to_csv(HERE / "spotify_user_growth.csv", index=False)

    print("wrote top_streamed_tracks.csv  ", tracks.shape)
    print("wrote spotify_user_growth.csv  ", growth.shape)


if __name__ == "__main__":
    main()
