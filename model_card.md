# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**VibeMatch 1.0**

---

## 2. Intended Use

This recommender suggests songs from a small catalog based on a user's stated preferences. It is built for classroom exploration, not for real users. It assumes the user knows their favorite genre, mood, and roughly how energetic they want the music to feel. It does not learn from listening history.

---

## 3. How the Model Works

Every song in the catalog gets a score from 0 to 4. The score is built from three signals:

- If the song's genre matches what the user wants, it earns points.
- If the song's mood matches, it earns fewer points but still a meaningful boost.
- The closer the song's energy level is to the user's target, the more points it earns.

Genre is worth the most because it's the broadest signal — getting the genre wrong usually means the whole vibe is off. Mood is a secondary filter. Energy is always scored, even if nothing else matches. Songs are then ranked from highest to lowest score and the top results are returned.

---

## 4. Data

The catalog has 20 songs stored in a CSV file. The original 10 songs were provided as a starter. Ten more were added to expand coverage. The catalog now includes 17 genres — lofi, pop, rock, jazz, ambient, synthwave, indie pop, hip-hop, r&b, classical, metal, folk, electronic, soul, country, reggae, and trap. Moods covered include chill, happy, intense, focused, moody, relaxed, empowered, romantic, melancholic, angry, nostalgic, euphoric, sad, hopeful, peaceful, and dark. Most genres and moods have only one or two songs, so the catalog is thin and will miss many real user tastes.

---

## 5. Strengths

The system works best when a user's preferences line up cleanly with what's in the catalog. For example, a "Chill Lofi" user gets Midnight Coding and Library Rain as the top two results — both are exactly the right genre, mood, and energy. The scoring is fully transparent: every recommendation comes with a plain-language reason. There are no black-box patterns, and the results are easy to trace back to specific weights. Users with strong, consistent preferences (high-energy pop, chill lofi, intense rock) tend to get results that feel correct.

---

## 6. Limitations and Bias

The most significant weakness discovered through experimentation is that categorical signals (genre + mood) can combine to a floor of +3.0 out of 4.0, which continuous energy similarity can never overcome on its own. In the "Euphoric + Low Energy" adversarial test, the scorer recommended Neon Overflow (energy 0.95) to a user who explicitly wanted energy 0.20 — a nearly opposite sonic experience — purely because genre and mood matched. The user's most audible preference (how loud and intense the song feels) was overruled by label-matching.

A second issue is that the system silently fails for users whose favorite genre is absent from the catalog. A user asking for "bluegrass" receives no warning and no fallback — the genre weight simply never fires, capping their maximum score at 2.0 and making mood and energy do all the work. In a real product this would be a confusing, trust-breaking experience.

The experiment of halving genre weight and doubling energy weight (GENRE=1.0, ENERGY=2.0) partially fixed the adversarial cases but introduced a new problem: for the "High-Energy Pop" profile, Storm Runner (rock/intense) jumped ahead of Sunrise City (pop/happy) at #2, meaning the system promoted an off-genre song over an on-genre one because their energy scores were so similar. There is no single weighting that works well for both well-aligned and conflicting profiles on a 20-song catalog.

Finally, the system has no diversity mechanism. When a genre has only one representative (rock, metal, classical, etc.) that song always appears at the top of any matching profile, and the next four results are drawn from completely different genres with no connection to the user's stated taste.

---

## 7. Evaluation

Six user profiles were tested: three standard and three adversarial.

The standard profiles were High-Energy Pop, Chill Lofi, and Deep Intense Rock. All three returned results that felt right. Gym Hero topped the pop list, Midnight Coding and Library Rain led the lofi list, and Storm Runner dominated rock. Those matched intuition.

The adversarial profiles were more revealing. The biggest surprise was the "High Energy + Sad" test. Sunday Crying — a slow, melancholic soul track — ranked first for a user who wanted energy 0.92. It won because genre and mood matched, and the +3.0 from those two signals easily beat any song with better energy but no label match. The system confidently recommended a song that would feel completely wrong in practice.

The "Ghost Genre" test (bluegrass) showed something subtler: the system doesn't tell you when it can't find your genre. It just quietly falls back to mood and energy. That kind of silent failure is hard to spot without testing.

A weight shift experiment (halving genre, doubling energy) was also run. It reduced the gap in adversarial cases but pushed an off-genre rock song above a matching pop song for the High-Energy Pop profile. The experiment confirmed there is no single weight combination that works well across all profiles.

---

## 8. Future Work

- Add partial credit for related genres. Lofi and ambient are closer to each other than lofi and metal, but the scorer treats them identically.
- Add a warning when the user's genre isn't in the catalog instead of silently ignoring it.
- Cap how many results can come from the same genre to add diversity to the top-k list.
- Let users set a minimum acceptable energy range instead of just a single target value.
- Try adding valence (musical positivity) as a fourth scoring signal since it is already in the data.

---

## 9. Personal Reflection

**Biggest learning moment:** Watching the "Euphoric + Low Energy" adversarial profile recommend the highest-energy song in the catalog made it click that a bug in a recommender isn't always a code error — it can be a wrong assumption baked silently into the weights.

**How AI tools helped, and when I double-checked:** AI was useful for generating the expanded song catalog and drafting boilerplate quickly, but I had to verify every numeric value and scoring formula myself because the model can produce plausible-looking numbers that don't actually add up.

**What surprised me about simple algorithms:** A three-signal formula with no learning, no history, and no real intelligence can still produce a ranked list that feels surprisingly reasonable for well-aligned profiles — which explains why users trust recommender systems even when the underlying logic is much simpler than they imagine.

**What I'd try next:** I'd add a minimum energy range instead of a single target value, so a user could say "between 0.7 and 1.0" and avoid the situation where a perfectly label-matched but sonically wrong song dominates the results.
