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


def _closeness_points(value: float, target: float, max_points: float, scale: float = 1.0):
    """Return points based on how close value is to target."""
    gap = abs(value - target) / scale
    return max(0.0, max_points * (1.0 - gap))


def score_song(
    user_prefs: Dict,
    song: Dict,
    scoring_mode: str = "balanced",
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

    return round(score, 4), reasons


def recommend_songs(
    user_prefs: Dict,
    songs: List[Dict],
    k: int = 5,
    scoring_mode: str = "balanced",
    diversity_penalty: bool = False,
) -> List[Tuple[Dict, float, str]]:
    """Score every song and return the top k ranked recommendations."""
    scored = []

    for song in songs:
        score, reasons = score_song(user_prefs, song, scoring_mode=scoring_mode)
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
