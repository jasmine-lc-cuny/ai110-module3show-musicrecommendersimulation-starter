from src.recommender import (
    Recommender,
    Song,
    UserProfile,
    load_songs,
    recommend_songs,
    score_song,
)

def make_small_recommender() -> Recommender:
    songs = [
        Song(
            id=1,
            title="Test Pop Track",
            artist="Test Artist",
            genre="pop",
            mood="happy",
            energy=0.8,
            tempo_bpm=120,
            valence=0.9,
            danceability=0.8,
            acousticness=0.2,
        ),
        Song(
            id=2,
            title="Chill Lofi Loop",
            artist="Test Artist",
            genre="lofi",
            mood="chill",
            energy=0.4,
            tempo_bpm=80,
            valence=0.6,
            danceability=0.5,
            acousticness=0.9,
        ),
    ]
    return Recommender(songs)


def test_recommend_returns_songs_sorted_by_score():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    results = rec.recommend(user, k=2)

    assert len(results) == 2
    # Starter expectation: the pop, happy, high energy song should score higher
    assert results[0].genre == "pop"
    assert results[0].mood == "happy"


def test_explain_recommendation_returns_non_empty_string():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    song = rec.songs[0]

    explanation = rec.explain_recommendation(user, song)
    assert isinstance(explanation, str)
    assert explanation.strip() != ""


def test_load_songs_converts_numeric_fields():
    songs = load_songs("data/songs.csv")

    assert len(songs) == 18
    assert isinstance(songs[0]["id"], int)
    assert isinstance(songs[0]["energy"], float)
    assert isinstance(songs[0]["tempo_bpm"], float)


def test_score_song_returns_score_and_reasons():
    song = {
        "id": 1,
        "title": "Sunrise City",
        "artist": "Neon Echo",
        "genre": "pop",
        "mood": "happy",
        "energy": 0.82,
        "tempo_bpm": 118.0,
        "valence": 0.84,
        "danceability": 0.79,
        "acousticness": 0.18,
    }
    prefs = {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.80,
        "tempo_bpm": 120.0,
        "valence": 0.80,
        "danceability": 0.80,
        "acousticness": 0.20,
    }

    score, reasons = score_song(prefs, song)

    assert score > 7
    assert "genre match (+2.00)" in reasons
    assert "mood match (+1.50)" in reasons


def test_recommend_songs_returns_top_k_sorted():
    songs = load_songs("data/songs.csv")
    prefs = {
        "genre": "lofi",
        "mood": "chill",
        "energy": 0.35,
        "tempo_bpm": 78.0,
        "valence": 0.55,
        "danceability": 0.55,
        "acousticness": 0.85,
    }

    results = recommend_songs(prefs, songs, k=3)
    scores = [score for _, score, _ in results]

    assert len(results) == 3
    assert scores == sorted(scores, reverse=True)
    assert results[0][0]["genre"] == "lofi"
    assert results[0][0]["mood"] == "chill"


def test_conflicting_profile_can_prioritize_genre_over_mood():
    songs = load_songs("data/songs.csv")
    prefs = {
        "genre": "pop",
        "mood": "sad",
        "energy": 0.90,
        "tempo_bpm": 130.0,
        "valence": 0.25,
        "danceability": 0.80,
        "acousticness": 0.25,
    }

    results = recommend_songs(prefs, songs, k=1)

    assert results[0][0]["genre"] == "pop"
