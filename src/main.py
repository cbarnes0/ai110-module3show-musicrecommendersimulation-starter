"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from .recommender import load_songs, recommend_songs

# ── User profiles ────────────────────────────────────────────────────────────
# Each dict must include: favorite_genre, favorite_mood, target_energy.
# "label" is display-only and ignored by the scorer.

PROFILES = [
    # Standard profiles — well-aligned preferences with clear catalog matches
    {
        "label": "High-Energy Pop",
        "favorite_genre": "pop",
        "favorite_mood":  "intense",
        "target_energy":  0.90,
    },
    {
        "label": "Chill Lofi",
        "favorite_genre": "lofi",
        "favorite_mood":  "chill",
        "target_energy":  0.40,
    },
    {
        "label": "Deep Intense Rock",
        "favorite_genre": "rock",
        "favorite_mood":  "intense",
        "target_energy":  0.88,
    },

    # Adversarial / edge-case profiles — designed to expose scoring weaknesses
    {
        # Genre and mood match only one song (Neon Overflow, energy=0.95) but
        # target_energy is 0.20. Tests whether 3.0 pts of categorical signal
        # overrides a large energy penalty (+0.25 energy score → total ~3.25).
        "label": "EDGE: Euphoric Mood + Low Energy (conflicting)",
        "favorite_genre": "electronic",
        "favorite_mood":  "euphoric",
        "target_energy":  0.20,
    },
    {
        # 'bluegrass' is not in the catalog. Genre match never fires.
        # Max achievable score is 2.0. Reveals what happens when the user's
        # primary preference has zero representation.
        "label": "EDGE: Ghost Genre (bluegrass not in catalog)",
        "favorite_genre": "bluegrass",
        "favorite_mood":  "chill",
        "target_energy":  0.38,
    },
    {
        # Only one sad song exists (Sunday Crying, energy=0.44) but target
        # energy is 0.92. Soul/sad match earns +3.0 but energy similarity
        # is only 0.52 → total 3.52. Does genre+mood dominance paper over
        # a song that "feels" totally wrong for this request?
        "label": "EDGE: High Energy + Sad (conflicting signals)",
        "favorite_genre": "soul",
        "favorite_mood":  "sad",
        "target_energy":  0.92,
    },
]
# ─────────────────────────────────────────────────────────────────────────────


def print_results(label: str, user_prefs: dict, recommendations: list) -> None:
    """Print a formatted results block for one profile run."""
    divider = "-" * 52
    header = "=" * 52
    print(f"\n{header}")
    print(f"  {label}")
    print(f"  {user_prefs['favorite_genre']} · {user_prefs['favorite_mood']} · energy {user_prefs['target_energy']}")
    print(header)
    for rank, (song, score, reasons) in enumerate(recommendations, start=1):
        print(divider)
        print(f"  #{rank}  {song['title']}  —  {song['artist']}")
        print(f"       {song['genre']} · {song['mood']} · energy {song['energy']}")
        print(f"       Score : {score:.2f} / 4.0")
        print(f"       Why   : {' | '.join(reasons)}")
    print(divider)


def main() -> None:
    songs = load_songs("data/songs.csv")

    for profile in PROFILES:
        user_prefs = {k: v for k, v in profile.items() if k != "label"}
        recommendations = recommend_songs(user_prefs, songs, k=3)
        print_results(profile["label"], user_prefs, recommendations)


if __name__ == "__main__":
    main()
