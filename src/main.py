"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    # Taste profile: target values for the features used in scoring
    user_prefs = {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.8,
        "target_tempo_bpm": 120,
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print(
        f"\nTop {len(recommendations)} recommendations for: "
        f"genre={user_prefs['favorite_genre']}, "
        f"mood={user_prefs['favorite_mood']}, "
        f"energy={user_prefs['target_energy']}, "
        f"tempo={user_prefs['target_tempo_bpm']} BPM"
    )
    print("=" * 60)
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        # Scores keep full precision for ranking and are rounded only here.
        print(f"\n{rank}. {song['title']} by {song['artist']}")
        print(f"   Score: {score:.2f} / 100")
        print("   Reasons:")
        for reason in explanation.split("; "):
            print(f"     - {reason}")


if __name__ == "__main__":
    main()
