"""
Command line runner for the Music Recommender Simulation.

Runs a set of stress-test profiles (three standard, three adversarial)
through the recommender and prints the top five songs for each.
"""

import shutil
import textwrap

from src.recommender import load_songs, recommend_songs

# Each profile pairs its preferences with a note on what it is testing.
PROFILES = {
    "High-Energy Pop": {
        "tests": "Baseline: preferences that line up with a song in the catalog.",
        "prefs": {
            "favorite_genre": "pop",
            "favorite_mood": "happy",
            "target_energy": 0.85,
            "target_tempo_bpm": 125,
        },
    },
    "Chill Lofi": {
        "tests": "Baseline: low-energy taste, and whether the similar-mood "
                 "partial credit (chill/relaxed/focused) shows up.",
        "prefs": {
            "favorite_genre": "lofi",
            "favorite_mood": "chill",
            "target_energy": 0.35,
            "target_tempo_bpm": 75,
        },
    },
    "Deep Intense Rock": {
        "tests": "Baseline: extreme targets (energy 0.95, 150 BPM) at the edge "
                 "of the catalog's range.",
        "prefs": {
            "favorite_genre": "rock",
            "favorite_mood": "intense",
            "target_energy": 0.95,
            "target_tempo_bpm": 150,
        },
    },
    "Adversarial: Energetic but Sad": {
        "tests": "Conflicting preferences: very high energy and fast tempo with "
                 "a 'sad' mood. No song is sad, so mood can never score, and "
                 "the ranking is decided by genre, energy and tempo alone.",
        "prefs": {
            "favorite_genre": "pop",
            "favorite_mood": "sad",
            "target_energy": 0.95,
            "target_tempo_bpm": 160,
        },
    },
    "Adversarial: Genre and Mood Not in CSV": {
        "tests": "Missing categories: 'classical' and 'melancholy' appear in no "
                 "song, so only energy and tempo can differentiate. Shows how "
                 "the recommender degrades when categorical signals are dead.",
        "prefs": {
            "favorite_genre": "classical",
            "favorite_mood": "melancholy",
            "target_energy": 0.30,
            "target_tempo_bpm": 60,
        },
    },
    "Adversarial: Chill but Frantic": {
        "tests": "Conflict between categories and numbers: lofi/chill taste "
                 "paired with maximum energy and tempo. Checks whether the "
                 "40+20 category points override the numeric targets.",
        "prefs": {
            "favorite_genre": "lofi",
            "favorite_mood": "chill",
            "target_energy": 1.0,
            "target_tempo_bpm": 180,
        },
    },
    "Advanced: Study Session": {
        "tests": "Same core taste as Chill Lofi, plus all five advanced preferences. "
                 "Checks whether tags, themes and instrumentalness can reorder "
                 "songs the core score nearly ties.",
        "prefs": {
            "favorite_genre": "lofi",
            "favorite_mood": "chill",
            "target_energy": 0.35,
            "target_tempo_bpm": 75,
            "target_popularity": 50,
            "target_release_decade": 2020,
            "preferred_mood_tags": ["calm", "focused"],
            "target_instrumentalness": 0.9,
            "preferred_lyrical_themes": ["study"],
        },
    },
    "Advanced: Chart-Topping Workout": {
        "tests": "Pop and intense taste with a very popular, recent, vocal track in "
                 "mind. Checks that popularity and decade can lift a song.",
        "prefs": {
            "favorite_genre": "pop",
            "favorite_mood": "intense",
            "target_energy": 0.9,
            "target_tempo_bpm": 130,
            "target_popularity": 90,
            "target_release_decade": 2020,
            "preferred_mood_tags": ["energetic", "motivating"],
            "target_instrumentalness": 0.05,
            "preferred_lyrical_themes": ["workout"],
        },
    },
    "Advanced: Retro Night Drive": {
        "tests": "Only some advanced preferences (no popularity, no instrumentalness "
                 "target). Checks that unused components stay switched off.",
        "prefs": {
            "favorite_genre": "synthwave",
            "favorite_mood": "moody",
            "target_energy": 0.75,
            "target_tempo_bpm": 110,
            "target_release_decade": 2010,
            "preferred_mood_tags": ["nocturnal", "brooding"],
            "preferred_lyrical_themes": ["night"],
        },
    },
}


CORE_PREFERENCES = (
    "favorite_genre", "favorite_mood", "target_energy", "target_tempo_bpm",
)

RANK_WIDTH = 4
TITLE_WIDTH = 20
SCORE_WIDTH = 9


def format_table(recommendations: list) -> str:
    """Build a text table of (song, score, explanation) results, wrapped to the terminal."""
    total_width = max(80, min(shutil.get_terminal_size((100, 24)).columns, 110))
    # Four columns plus borders and padding take 13 characters.
    reasons_width = total_width - (RANK_WIDTH + TITLE_WIDTH + SCORE_WIDTH) - 13
    widths = (RANK_WIDTH, TITLE_WIDTH, SCORE_WIDTH, reasons_width)
    border = "+" + "+".join("-" * (w + 2) for w in widths) + "+"

    def row(cells: list) -> list:
        # Each cell is a list of lines; pad them so the row lines up.
        height = max(len(cell) for cell in cells)
        lines = []
        for i in range(height):
            parts = [
                (cell[i] if i < len(cell) else "").ljust(width)
                for cell, width in zip(cells, widths)
            ]
            lines.append("| " + " | ".join(parts) + " |")
        return lines

    lines = [border]
    lines += row([["Rank"], ["Song"], ["Score/100"], ["Reasons"]])
    lines.append(border)
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        reasons = []
        for reason in explanation.split("; "):
            reasons += textwrap.wrap(
                reason, reasons_width, initial_indent="- ", subsequent_indent="  "
            )
        # Scores keep full precision for ranking and are rounded only here.
        lines += row([
            [str(rank)],
            textwrap.wrap(song["title"], TITLE_WIDTH),
            [f"{score:.2f}"],
            reasons,
        ])
        lines.append(border)
    return "\n".join(lines)


def print_profile(name: str, profile: dict, songs: list) -> None:
    prefs = profile["prefs"]
    print("\n" + "#" * 70)
    print(f"PROFILE: {name}")
    print("#" * 70)
    print(textwrap.fill(
        f"What it tests: {profile['tests']}", 100, subsequent_indent="  "
    ))
    print(
        f"Preferences: genre={prefs['favorite_genre']}, "
        f"mood={prefs['favorite_mood']}, "
        f"energy={prefs['target_energy']}, "
        f"tempo={prefs['target_tempo_bpm']} BPM"
    )
    advanced = {
        key: value for key, value in prefs.items() if key not in CORE_PREFERENCES
    }
    if advanced:
        print(textwrap.fill(
            "Advanced preferences: "
            + ", ".join(f"{key}={value}" for key, value in advanced.items()),
            100, subsequent_indent="  ",
        ))

    recommendations = recommend_songs(prefs, songs, k=5)
    print(f"\nTop {len(recommendations)} recommendations:")
    print(format_table(recommendations))


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    for name, profile in PROFILES.items():
        print_profile(name, profile, songs)


if __name__ == "__main__":
    main()
