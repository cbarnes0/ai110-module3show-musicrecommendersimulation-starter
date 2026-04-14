"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from .recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv") 

    user_prefs = {
        "favorite_genre": "lofi",
        "favorite_mood": "chill",
        "target_energy": 0.40,
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    divider = "-" * 48
    print(f"\nTop {len(recommendations)} recommendations for: "
          f"{user_prefs['favorite_genre']} · {user_prefs['favorite_mood']} "
          f"· energy {user_prefs['target_energy']}\n")

    for rank, (song, score, reasons) in enumerate(recommendations, start=1):
        print(divider)
        print(f" #{rank}  {song['title']}  —  {song['artist']}")
        print(f"      {song['genre']} · {song['mood']} · energy {song['energy']}")
        print(f"      Score : {score:.2f} / 4.0")
        print(f"      Why   : {' | '.join(reasons)}")

    print(divider)


if __name__ == "__main__":
    main()
