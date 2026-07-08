"""Generate a simulated listening-history dataset for the collaborative-filtering demo.

Each simulated user mostly "likes" songs that match one genre/mood cluster
(their taste), plus a couple of noisy likes outside that cluster, so the
resulting co-occurrence data has realistic structure: users who share a
favorite genre or mood also cluster around a few cross-genre songs.

Run with: python scripts/generate_listening_history.py
"""

import csv
import random
from pathlib import Path

from src.recommender import load_songs

SEED = 42
NUM_USERS = 40
MIN_LIKES = 3
MAX_LIKES = 6
NOISE_LIKES = 2


def main() -> None:
    random.seed(SEED)
    songs = load_songs("data/songs.csv")
    song_ids = [song["id"] for song in songs]

    clusters = sorted({(song["genre"], song["mood"]) for song in songs})

    rows = []
    for user_id in range(1, NUM_USERS + 1):
        genre, mood = random.choice(clusters)
        cluster_song_ids = [
            song["id"]
            for song in songs
            if song["genre"] == genre or song["mood"] == mood
        ]

        num_likes = random.randint(MIN_LIKES, MAX_LIKES)
        liked = set(random.sample(cluster_song_ids, min(num_likes, len(cluster_song_ids))))

        noisy_pool = [sid for sid in song_ids if sid not in liked]
        liked.update(random.sample(noisy_pool, min(NOISE_LIKES, len(noisy_pool))))

        for song_id in sorted(liked):
            rows.append({"user_id": user_id, "song_id": song_id})

    path = Path("data/listening_history.csv")
    with path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["user_id", "song_id"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} like events for {NUM_USERS} simulated users to {path}")


if __name__ == "__main__":
    main()
