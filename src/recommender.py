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

# Advanced scoring: the core score (mood, genre, energy, tempo) counts for 70
# of the weight. Each advanced preference adds its own weight, but only when
# the user supplies it.
CORE_WEIGHT = 70
ADVANCED_WEIGHTS = {
    "popularity": 5,
    "release_decade": 5,
    "mood_tags": 10,
    "instrumentalness": 5,
    "lyrical_themes": 5,
}

def _split_tags(value) -> List[str]:
    """Turn 'a; B ;c' (or a list) into a clean lowercase list of tags."""
    if value is None:
        return []
    if isinstance(value, str):
        value = value.split(";")
    return [tag.strip().lower() for tag in value if tag and tag.strip()]

def load_songs(csv_path: str) -> List[Dict]:
    """Read songs from a CSV file into dictionaries with numbers and tag lists converted."""
    print(f"Loading songs from {csv_path}...")
    songs = []
    with open(csv_path, "r", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            row["id"] = int(row["id"])
            row["tempo_bpm"] = int(row["tempo_bpm"])
            for field in ("energy", "valence", "danceability", "acousticness"):
                row[field] = float(row[field])
            # A missing advanced value becomes None (or an empty list)
            # instead of raising an error.
            for field in ("popularity", "release_decade"):
                row[field] = int(row[field]) if row.get(field) else None
            row["instrumentalness"] = (
                float(row["instrumentalness"]) if row.get("instrumentalness") else None
            )
            for field in ("detailed_mood_tags", "lyrical_themes"):
                row[field] = _split_tags(row.get(field))
            songs.append(row)
    return songs

def _core_score(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song out of 100 on mood, genre, energy and tempo, with reasons."""
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

def _tag_match(wanted: List[str], song_tags: List[str]) -> float:
    """Fraction of the wanted tags that the song has."""
    return sum(tag in song_tags for tag in wanted) / len(wanted)

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song out of 100, adding advanced preferences only when supplied."""
    core, reasons = _core_score(user_prefs, song)

    # Each active component is (name, match between 0 and 1, reason).
    active = []

    target = user_prefs.get("target_popularity")
    if target is not None:
        value = song.get("popularity")
        match = 0.0 if value is None else max(0.0, 1 - abs(value - target) / 100)
        active.append(("popularity", match, f"popularity {value} vs target {target}"))

    target = user_prefs.get("target_release_decade")
    if target is not None:
        value = song.get("release_decade")
        match = 1.0 if value == target else 0.0
        active.append(("release_decade", match, f"release decade {value} vs target {target}"))

    wanted = _split_tags(user_prefs.get("preferred_mood_tags"))
    if wanted:
        have = song.get("detailed_mood_tags") or []
        found = [tag for tag in wanted if tag in have]
        active.append((
            "mood_tags", _tag_match(wanted, have),
            f"mood tags {len(found)} of {len(wanted)} wanted found ({', '.join(found) or 'none'})",
        ))

    target = user_prefs.get("target_instrumentalness")
    if target is not None:
        value = song.get("instrumentalness")
        match = 0.0 if value is None else max(0.0, 1 - abs(value - target))
        active.append(("instrumentalness", match, f"instrumentalness {value} vs target {target}"))

    wanted = _split_tags(user_prefs.get("preferred_lyrical_themes"))
    if wanted:
        have = song.get("lyrical_themes") or []
        found = [tag for tag in wanted if tag in have]
        active.append((
            "lyrical_themes", _tag_match(wanted, have),
            f"lyrical themes {len(found)} of {len(wanted)} wanted found ({', '.join(found) or 'none'})",
        ))

    # Without advanced preferences the original score is returned untouched.
    if not active:
        return core, reasons

    weighted_total = CORE_WEIGHT * (core / 100)
    active_weight_total = CORE_WEIGHT
    reasons.append(f"core score {core:.2f}/100 counts for weight {CORE_WEIGHT}")
    for name, match, text in active:
        weight = ADVANCED_WEIGHTS[name]
        weighted_total += weight * match
        active_weight_total += weight
        reasons.append(f"{text}: match {match:.2f} x weight {weight}")
    score = 100 * weighted_total / active_weight_total
    reasons.append(
        f"final = 100 x {weighted_total:.2f} / {active_weight_total} = {score:.2f}"
    )
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
