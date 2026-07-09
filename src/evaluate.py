"""Quantify recommendation diversity and filter-bubble bias across many synthetic profiles."""

import random
from collections import Counter
from typing import Dict, List

from .recommender import recommend_songs

GENRES = ["codepath", "40's", "50's", "60's", "70's", "80's"]
MOODS = ["happy", "chill", "intense", "relaxed", "moody", "focused", "euphoric", "sad", "calm", "energetic"]


def generate_synthetic_profiles(num_profiles: int = 60, seed: int = 7) -> List[Dict]:
    """Create random-but-plausible user preference dicts for bias testing."""
    rng = random.Random(seed)
    profiles = []
    for _ in range(num_profiles):
        profiles.append({
            "genre": rng.choice(GENRES),
            "mood": rng.choice(MOODS),
            "energy": round(rng.uniform(0.2, 0.95), 2),
            "valence": round(rng.uniform(0.2, 0.95), 2),
            "danceability": round(rng.uniform(0.3, 0.95), 2),
            "tempo_bpm": rng.randint(70, 170),
            "acousticness": round(rng.uniform(0.05, 0.9), 2),
        })
    return profiles


def genre_concentration(genre_counts: Counter) -> float:
    """Herfindahl-Hirschman Index of genre concentration (0=diverse, 1=one genre)."""
    total = sum(genre_counts.values())
    if total == 0:
        return 0.0
    return sum((count / total) ** 2 for count in genre_counts.values())


def run_diversity_report(songs: List[Dict], k: int = 5, num_profiles: int = 60, **recommend_kwargs) -> Dict:
    """Run many synthetic profiles and measure how concentrated the top-k results are."""
    profiles = generate_synthetic_profiles(num_profiles)
    genre_counts = Counter()
    top1_counts = Counter()

    for profile in profiles:
        results = recommend_songs(profile, songs, k=k, **recommend_kwargs)
        for song, _score, _explanation in results:
            genre_counts[song["genre"]] += 1
        if results:
            top1_counts[results[0][0]["title"]] += 1

    return {
        "num_profiles": num_profiles,
        "genre_counts": genre_counts,
        "hhi": genre_concentration(genre_counts),
        "top1_counts": top1_counts,
    }


def print_report(title: str, report: Dict) -> None:
    """Print a readable diversity report with an ASCII bar chart."""
    print(f"\n{title}")
    print("-" * len(title))
    print(f"Profiles tested: {report['num_profiles']}")
    print(f"Genre concentration (HHI, 0=diverse .. 1=one genre): {report['hhi']:.3f}")

    total = sum(report["genre_counts"].values())
    print("\nGenre share of all top-k slots:")
    for genre, count in report["genre_counts"].most_common():
        share = count / total
        bar = "#" * round(share * 40)
        print(f"  {genre:<12} {share * 100:5.1f}% {bar}")

    print("\nMost frequent #1 recommendation across profiles:")
    for song_title, count in report["top1_counts"].most_common(3):
        share = count / report["num_profiles"] * 100
        print(f"  {song_title}: {count}/{report['num_profiles']} profiles ({share:.1f}%)")


def main() -> None:
    """Compare genre concentration across scoring configurations."""
    from .recommender import load_songs, load_listening_history

    songs = load_songs("data/songs.csv")
    history = load_listening_history("data/listening_history.csv")

    baseline = run_diversity_report(songs)
    print_report("Balanced scoring (no diversity penalty)", baseline)

    with_penalty = run_diversity_report(songs, diversity_penalty=True)
    print_report("Balanced scoring + diversity penalty", with_penalty)

    with_cf = run_diversity_report(songs, history=history, use_collaborative=True)
    print_report("Balanced scoring + collaborative filtering", with_cf)


if __name__ == "__main__":
    main()
