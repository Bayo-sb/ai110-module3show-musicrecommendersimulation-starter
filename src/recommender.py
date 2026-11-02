import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
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

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

# Moods that earn partial credit when they differ from the requested mood.
SIMILAR_MOODS = {"chill", "relaxed", "focused"}

def load_songs(csv_path: str) -> List[Dict]:
    """Read songs from a CSV file into dictionaries with numeric fields converted."""
    print(f"Loading songs from {csv_path}...")
    songs = []
    with open(csv_path, "r", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            row["id"] = int(row["id"])
            row["tempo_bpm"] = int(row["tempo_bpm"])
            for field in ("energy", "valence", "danceability", "acousticness"):
                row[field] = float(row[field])
            songs.append(row)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song out of 100 against a taste profile and list the reasons."""
    reasons = []

    want_mood = user_prefs["favorite_mood"].strip().lower()
    song_mood = song["mood"].strip().lower()
    if song_mood == want_mood:
        mood_points = 40
        reasons.append(f"mood matches {want_mood} (+40)")
    elif song_mood in SIMILAR_MOODS and want_mood in SIMILAR_MOODS:
        mood_points = 20
        reasons.append(f"mood {song_mood} is similar to {want_mood} (+20)")
    else:
        mood_points = 0
        reasons.append(f"mood {song_mood} does not match {want_mood} (+0)")

    want_genre = user_prefs["favorite_genre"].strip().lower()
    song_genre = song["genre"].strip().lower()
    if song_genre == want_genre:
        genre_points = 20
        reasons.append(f"genre matches {want_genre} (+20)")
    else:
        genre_points = 0
        reasons.append(f"genre {song_genre} does not match {want_genre} (+0)")

    energy_points = 30 * (1 - abs(song["energy"] - user_prefs["target_energy"]))
    reasons.append(
        f"energy {song['energy']} vs target {user_prefs['target_energy']} (+{energy_points:.2f})"
    )

    tempo_gap = abs(song["tempo_bpm"] - user_prefs["target_tempo_bpm"])
    tempo_points = 10 * max(0, 1 - tempo_gap / 40)
    reasons.append(
        f"tempo {song['tempo_bpm']} BPM vs target {user_prefs['target_tempo_bpm']} (+{tempo_points:.2f})"
    )

    score = mood_points + genre_points + energy_points + tempo_points
    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Return the top k songs as (song, score, explanation), best score first."""
    # A negative k would otherwise slice off songs from the end instead of
    # returning nothing.
    if k <= 0:
        return []

    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored.append((song, score, "; ".join(reasons)))

    # sorted() builds a new list, so `songs` is left untouched. Negating the
    # score gives descending order, and the title breaks ties alphabetically.
    ranked = sorted(scored, key=lambda item: (-item[1], item[0]["title"].casefold()))
    return ranked[:k]
