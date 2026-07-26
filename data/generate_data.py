"""Generate small, reproducible music-streaming-flavored datasets for the examples.

Uses only pandas and the Python standard library (``random``), matching the
project's pandas + matplotlib dependency constraint (no numpy import).

Writes three CSVs into ``data/``:

* ``genre_streams.csv``    — streams by genre           (bar)
* ``monthly_listeners.csv``— monthly listeners per artist (line, multi-series)
* ``tracks.csv``           — audio features per track    (scatter)

Run directly:  python data/generate_data.py
"""

import random
from pathlib import Path

import pandas as pd

HERE = Path(__file__).parent


def genre_streams(seed=1):
    rng = random.Random(seed)
    genres = ["Pop", "Hip-Hop", "Rock", "Latin", "EDM", "R&B", "Indie", "Jazz"]
    base = {"Pop": 9.2, "Hip-Hop": 8.1, "Rock": 5.6, "Latin": 6.8,
            "EDM": 4.3, "R&B": 3.9, "Indie": 2.7, "Jazz": 1.4}
    rows = [{"genre": g,
             "streams": round(base[g] * 1e9 * rng.uniform(0.9, 1.1))}
            for g in genres]
    return pd.DataFrame(rows)


def monthly_listeners(seed=2):
    rng = random.Random(seed)
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    artists = {"Aurora Skye": 18.0, "The Night Owls": 12.5,
               "DJ Marisol": 9.0, "Kite String": 6.5}
    data = {"month": months}
    for artist, start in artists.items():
        val = start
        series = []
        for _ in months:
            val = max(1.0, val * rng.uniform(0.97, 1.12))
            series.append(round(val, 2))
        data[artist] = series  # millions of monthly listeners
    return pd.DataFrame(data)


def tracks(seed=3):
    rng = random.Random(seed)
    rows = []
    for i in range(80):
        energy = rng.uniform(0.2, 0.98)
        # danceability loosely correlated with energy
        dance = min(0.99, max(0.1, 0.35 + 0.5 * energy + rng.uniform(-0.2, 0.2)))
        popularity = int(max(1, min(100, 30 + 60 * energy + rng.gauss(0, 12))))
        rows.append({
            "track": f"Track {i + 1:02d}",
            "energy": round(energy, 3),
            "danceability": round(dance, 3),
            "popularity": popularity,
        })
    return pd.DataFrame(rows)


def main():
    genre_streams().to_csv(HERE / "genre_streams.csv", index=False)
    monthly_listeners().to_csv(HERE / "monthly_listeners.csv", index=False)
    tracks().to_csv(HERE / "tracks.csv", index=False)
    print("Wrote genre_streams.csv, monthly_listeners.csv, tracks.csv")


if __name__ == "__main__":
    main()
