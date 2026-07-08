from src.recommender import (
    Recommender,
    Song,
    UserProfile,
    collaborative_scores,
    load_listening_history,
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


def test_score_song_supports_mood_first_mode():
    song = {
        "id": 1,
        "title": "Sunrise City",
        "artist": "Neon Echo",
        "genre": "rock",
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

    balanced_score, _ = score_song(prefs, song)
    mood_first_score, _ = score_song(prefs, song, scoring_mode="mood-first")

    assert mood_first_score > balanced_score


def test_recommend_songs_can_penalize_same_artist_duplicates():
    songs = [
        {
            "id": 1,
            "title": "First Hit",
            "artist": "Artist A",
            "genre": "pop",
            "mood": "happy",
            "energy": 0.80,
            "tempo_bpm": 120.0,
            "valence": 0.80,
            "danceability": 0.80,
            "acousticness": 0.20,
        },
        {
            "id": 2,
            "title": "Second Hit",
            "artist": "Artist A",
            "genre": "pop",
            "mood": "happy",
            "energy": 0.80,
            "tempo_bpm": 120.0,
            "valence": 0.80,
            "danceability": 0.80,
            "acousticness": 0.20,
        },
        {
            "id": 3,
            "title": "Different Artist Song",
            "artist": "Artist B",
            "genre": "pop",
            "mood": "happy",
            "energy": 0.70,
            "tempo_bpm": 118.0,
            "valence": 0.75,
            "danceability": 0.77,
            "acousticness": 0.25,
        },
    ]
    prefs = {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.80,
        "tempo_bpm": 120.0,
        "valence": 0.80,
        "danceability": 0.80,
        "acousticness": 0.20,
    }

    results = recommend_songs(prefs, songs, k=2, diversity_penalty=True)

    assert results[0][0]["artist"] == "Artist A"
    assert results[1][0]["artist"] == "Artist B"


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


def test_load_listening_history_groups_song_ids_by_user():
    history = load_listening_history("data/listening_history.csv")

    assert len(history) == 40
    assert all(isinstance(song_ids, list) for song_ids in history.values())
    assert all(isinstance(song_id, int) for song_ids in history.values() for song_id in song_ids)


def test_collaborative_scores_boost_songs_liked_by_similar_users():
    songs = [
        {"id": 1, "genre": "pop", "mood": "happy"},
        {"id": 2, "genre": "rock", "mood": "intense"},
    ]
    history = {
        1: [1, 2],  # a "pop/happy" fan who also liked the rock song
        2: [1],     # another pop/happy fan
        3: [2],     # a fan outside the pop/happy cluster
    }

    scores = collaborative_scores(history, songs, favorite_genre="pop", favorite_mood="happy")

    assert scores[1] > 0
    assert scores.get(2, 0) > 0
    assert scores[1] >= scores[2]


def test_recommend_songs_can_blend_collaborative_signal():
    songs = load_songs("data/songs.csv")
    history = load_listening_history("data/listening_history.csv")
    prefs = {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.85,
        "tempo_bpm": 124.0,
        "valence": 0.85,
        "danceability": 0.85,
        "acousticness": 0.15,
    }

    without_cf = recommend_songs(prefs, songs, k=5)
    with_cf = recommend_songs(prefs, songs, k=5, history=history, use_collaborative=True)

    without_cf_score = {song["id"]: score for song, score, _ in without_cf}
    with_cf_score = {song["id"]: score for song, score, _ in with_cf}

    shared_ids = set(without_cf_score) & set(with_cf_score)
    assert any(with_cf_score[song_id] >= without_cf_score[song_id] for song_id in shared_ids)
