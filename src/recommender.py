import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple


NUMERIC_FIELDS = {
    "id": int,
    "energy": float,
    "tempo_bpm": float,
    "valence": float,
    "danceability": float,
    "acousticness": float,
}


@dataclass
class Song:
    """Represent a song and the attributes used for recommendation."""

    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

    @classmethod
    def from_dict(cls, data: Dict) -> "Song":
        """Create a Song object from a CSV row dictionary."""
        return cls(
            id=int(data["id"]),
            title=data["title"],
            artist=data["artist"],
            genre=data["genre"],
            mood=data["mood"],
            energy=float(data["energy"]),
            tempo_bpm=float(data["tempo_bpm"]),
            valence=float(data["valence"]),
            danceability=float(data["danceability"]),
            acousticness=float(data["acousticness"]),
        )


@dataclass
class UserProfile:
    """Represent a user's simplified music taste profile."""

    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool
    target_valence: float = 0.75
    target_danceability: float = 0.75
    target_tempo_bpm: float = 120.0

    def to_preferences(self) -> Dict:
        """Convert the profile into the dictionary format used by functions."""
        return {
            "genre": self.favorite_genre,
            "mood": self.favorite_mood,
            "energy": self.target_energy,
            "valence": self.target_valence,
            "danceability": self.target_danceability,
            "tempo_bpm": self.target_tempo_bpm,
            "acousticness": 0.75 if self.likes_acoustic else 0.20,
        }


class Recommender:
    """OOP wrapper around the functional recommendation logic."""

    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top k songs for a user profile."""
        song_dicts = [song.__dict__ for song in self.songs]
        ranked = recommend_songs(user.to_preferences(), song_dicts, k)
        return [Song.from_dict(song) for song, _, _ in ranked]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Explain why a single song fits the user profile."""
        _, reasons = score_song(user.to_preferences(), song.__dict__)
        return "; ".join(reasons)


def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file and convert numeric fields."""
    path = Path(csv_path)
    songs = []

    with path.open(newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            converted = {}
            for key, value in row.items():
                converter = NUMERIC_FIELDS.get(key, str)
                converted[key] = converter(value)
            songs.append(converted)

    return songs


def load_listening_history(csv_path: str) -> Dict[int, List[int]]:
    """Load simulated listener like-events, grouped by user id."""
    path = Path(csv_path)
    history: Dict[int, List[int]] = {}

    with path.open(newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            user_id = int(row["user_id"])
            song_id = int(row["song_id"])
            history.setdefault(user_id, []).append(song_id)

    return history


def _find_similar_users(
    history: Dict[int, List[int]],
    favorite_genre: str,
    favorite_mood: str,
    songs_by_id: Dict[int, Dict],
) -> set:
    """Return ids of simulated users who liked the user's favorite genre or mood."""
    similar_users = set()

    for user_id, liked_song_ids in history.items():
        for song_id in liked_song_ids:
            song = songs_by_id.get(song_id)
            if song is None:
                continue
            if (
                song["genre"].lower() == favorite_genre.lower()
                or song["mood"].lower() == favorite_mood.lower()
            ):
                similar_users.add(user_id)
                break

    return similar_users


def collaborative_scores(
    history: Dict[int, List[int]],
    songs: List[Dict],
    favorite_genre: str,
    favorite_mood: str,
    max_points: float = 1.5,
) -> Dict[int, float]:
    """Score songs by how often simulated 'similar' listeners liked them.

    This approximates collaborative filtering: instead of looking at a song's
    own attributes, it looks at what other simulated users with a similar
    genre/mood taste liked, so a song can score well here even if its own
    genre does not match the user's favorite.
    """
    songs_by_id = {song["id"]: song for song in songs}
    similar_users = _find_similar_users(history, favorite_genre, favorite_mood, songs_by_id)

    like_counts: Dict[int, int] = {}
    for user_id in similar_users:
        for song_id in history.get(user_id, []):
            like_counts[song_id] = like_counts.get(song_id, 0) + 1

    if not like_counts:
        return {}

    max_count = max(like_counts.values())
    return {
        song_id: round((count / max_count) * max_points, 4)
        for song_id, count in like_counts.items()
    }


def _closeness_points(value: float, target: float, max_points: float, scale: float = 1.0):
    """Return points based on how close value is to target."""
    gap = abs(value - target) / scale
    return max(0.0, max_points * (1.0 - gap))


def score_song(
    user_prefs: Dict,
    song: Dict,
    scoring_mode: str = "balanced",
    collaborative_points: Dict[int, float] = None,
) -> Tuple[float, List[str]]:
    """Score a song against preferences and return reasons."""
    score = 0.0
    reasons = []

    if song["genre"].lower() == user_prefs.get("genre", "").lower():
        score += 2.0
        reasons.append("genre match (+2.00)")
    else:
        reasons.append("different genre (+0.00)")

    if song["mood"].lower() == user_prefs.get("mood", "").lower():
        score += 1.5
        reasons.append("mood match (+1.50)")
    else:
        reasons.append("different mood (+0.00)")

    if scoring_mode == "mood-first":
        score += 0.75 if song["mood"].lower() == user_prefs.get("mood", "").lower() else 0.0

    numeric_specs = [
        ("energy", 1.5, 1.0),
        ("valence", 1.0, 1.0),
        ("danceability", 1.0, 1.0),
        ("tempo_bpm", 0.75, 120.0),
        ("acousticness", 0.75, 1.0),
    ]

    for field, max_points, scale in numeric_specs:
        if field not in user_prefs:
            continue
        points = _closeness_points(float(song[field]), float(user_prefs[field]), max_points, scale)
        score += points
        reasons.append(f"{field} closeness (+{points:.2f})")

    if collaborative_points:
        points = collaborative_points.get(song["id"], 0.0)
        if points > 0:
            score += points
            reasons.append(f"liked by similar listeners (+{points:.2f})")

    return round(score, 4), reasons


def recommend_songs(
    user_prefs: Dict,
    songs: List[Dict],
    k: int = 5,
    scoring_mode: str = "balanced",
    diversity_penalty: bool = False,
    history: Dict[int, List[int]] = None,
    use_collaborative: bool = False,
) -> List[Tuple[Dict, float, str]]:
    """Score every song and return the top k ranked recommendations."""
    collaborative_points: Dict[int, float] = {}
    if use_collaborative and history:
        collaborative_points = collaborative_scores(
            history,
            songs,
            user_prefs.get("genre", ""),
            user_prefs.get("mood", ""),
        )

    scored = []

    for song in songs:
        score, reasons = score_song(
            user_prefs,
            song,
            scoring_mode=scoring_mode,
            collaborative_points=collaborative_points,
        )
        scored.append((song, score, "; ".join(reasons)))

    ranked = sorted(scored, key=lambda item: item[1], reverse=True)
    if not diversity_penalty:
        return ranked[:k]

    final_results = []
    seen_artists = set()
    for song, score, explanation in ranked:
        adjusted_score = score
        if song["artist"] in seen_artists:
            adjusted_score -= 0.5
        if adjusted_score < 0:
            adjusted_score = 0.0
        final_results.append((song, adjusted_score, explanation))
        seen_artists.add(song["artist"])

    return sorted(final_results, key=lambda item: item[1], reverse=True)[:k]
