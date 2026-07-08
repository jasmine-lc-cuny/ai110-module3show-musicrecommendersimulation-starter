"""
Command line runner for the Music Recommender Simulation.
"""

from .recommender import apply_feedback, load_songs, load_listening_history, recommend_songs


PROFILES = {
    "High-Energy Pop": {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.85,
        "valence": 0.85,
        "danceability": 0.85,
        "tempo_bpm": 124,
        "acousticness": 0.15,
    },
    "Chill Lofi": {
        "genre": "lofi",
        "mood": "chill",
        "energy": 0.35,
        "valence": 0.55,
        "danceability": 0.55,
        "tempo_bpm": 78,
        "acousticness": 0.85,
    },
    "Deep Intense Rock": {
        "genre": "rock",
        "mood": "intense",
        "energy": 0.95,
        "valence": 0.45,
        "danceability": 0.60,
        "tempo_bpm": 150,
        "acousticness": 0.08,
    },
    "Conflicted Sad Workout": {
        "genre": "pop",
        "mood": "sad",
        "energy": 0.90,
        "valence": 0.25,
        "danceability": 0.80,
        "tempo_bpm": 130,
        "acousticness": 0.25,
    },
}


def print_recommendations(profile_name, user_prefs, songs, k=5, scoring_mode="balanced", **recommend_kwargs):
    """Print a formatted recommendation list for one profile."""
    print(f"\nUser profile: {profile_name}")
    print("-" * (14 + len(profile_name)))

    recommendations = recommend_songs(user_prefs, songs, k=k, scoring_mode=scoring_mode, **recommend_kwargs)
    for index, (song, score, explanation) in enumerate(recommendations, start=1):
        print(
            f"{index}. {song['title']} by {song['artist']} "
            f"[{song['genre']} / {song['mood']}] - Score: {score:.2f}"
        )
        print(f"   Reasons: {explanation}")


def main() -> None:
    """Load songs and print recommendations for several taste profiles."""
    songs = load_songs("data/songs.csv")
    history = load_listening_history("data/listening_history.csv")
    print(f"Loaded songs: {len(songs)}")

    for profile_name, user_prefs in PROFILES.items():
        print_recommendations(profile_name, user_prefs, songs, k=5, scoring_mode="balanced")

    print("\nBonus mode: mood-first")
    print_recommendations("High-Energy Pop (Mood-First)", PROFILES["High-Energy Pop"], songs, k=5, scoring_mode="mood-first")

    print("\nBonus mode: collaborative filtering (simulated listeners)")
    print_recommendations(
        "High-Energy Pop (Collaborative)",
        PROFILES["High-Energy Pop"],
        songs,
        k=5,
        scoring_mode="balanced",
        history=history,
        use_collaborative=True,
    )

    print("\nBonus mode: exploration slot (reserves one discovery pick)")
    print_recommendations(
        "High-Energy Pop (Exploration)",
        PROFILES["High-Energy Pop"],
        songs,
        k=5,
        scoring_mode="balanced",
        exploration=True,
    )

    print("\nBonus mode: feedback loop (skip Library Rain, save Midnight Coding)")
    print_recommendations(
        "Chill Lofi (Before Feedback)",
        PROFILES["Chill Lofi"],
        songs,
        k=3,
        scoring_mode="balanced",
    )
    feedback = {4: "skip", 2: "save"}  # 4 = Library Rain, 2 = Midnight Coding
    adjusted_prefs = apply_feedback(PROFILES["Chill Lofi"], songs, feedback)
    print_recommendations(
        "Chill Lofi (After Feedback)",
        adjusted_prefs,
        songs,
        k=3,
        scoring_mode="balanced",
    )


if __name__ == "__main__":
    main()
