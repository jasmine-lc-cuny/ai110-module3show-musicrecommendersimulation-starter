from collections import Counter

from src.evaluate import (
    generate_synthetic_profiles,
    genre_concentration,
    run_diversity_report,
)
from src.recommender import load_songs


def test_generate_synthetic_profiles_are_reproducible():
    profiles_a = generate_synthetic_profiles(num_profiles=10, seed=1)
    profiles_b = generate_synthetic_profiles(num_profiles=10, seed=1)

    assert profiles_a == profiles_b
    assert len(profiles_a) == 10
    assert all("genre" in profile and "mood" in profile for profile in profiles_a)


def test_genre_concentration_is_higher_for_one_genre():
    concentrated = Counter({"pop": 10})
    diverse = Counter({"pop": 5, "rock": 5})

    assert genre_concentration(concentrated) == 1.0
    assert genre_concentration(diverse) < genre_concentration(concentrated)


def test_run_diversity_report_returns_expected_keys():
    songs = load_songs("data/songs.csv")

    report = run_diversity_report(songs, k=5, num_profiles=10)

    assert report["num_profiles"] == 10
    assert 0.0 <= report["hhi"] <= 1.0
    assert sum(report["genre_counts"].values()) == 50
