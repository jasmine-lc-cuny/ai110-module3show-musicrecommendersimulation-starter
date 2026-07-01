# Music Recommender Simulation

## Project Summary

**VibeFinder 1.0** is a small content-based music recommender. It compares a
user's preferred genre, mood, energy, valence, danceability, tempo, and
acousticness to every song in a CSV catalog, then ranks the songs with a
weighted score and explains why each recommendation was chosen. The project
also includes bonus functionality for a mood-first scoring mode and a diversity
penalty that helps avoid repeating the same artist too often in the top results.

---

## How The System Works

Real recommendation systems use many signals. Collaborative filtering looks for
patterns in user behavior, such as likes, skips, playlists, and what similar
listeners replay. Content-based filtering looks at the item itself, such as a
song's genre, mood, tempo, energy, or acousticness. This project uses the
content-based approach: it does not know what other listeners like, so it
matches song attributes to a single user's taste profile.

Each song uses these features: `genre`, `mood`, `energy`, `tempo_bpm`,
`valence`, `danceability`, and `acousticness`. A user profile stores matching
targets for those features, such as favorite genre, favorite mood, target
energy, target valence, target danceability, target tempo, and whether the user
likes acoustic music.

Algorithm recipe:

- `+2.0` for an exact genre match.
- `+1.5` for an exact mood match.
- Up to `+1.5` for energy closeness.
- Up to `+1.0` for valence closeness.
- Up to `+1.0` for danceability closeness.
- Up to `+0.75` for tempo closeness.
- Up to `+0.75` for acousticness closeness.
- Score every song, sort from highest to lowest, and return the top `k`.

```text
User Preferences -> score each song in songs.csv -> sort scores -> top recommendations with reasons
```

Expected bias: because genre and mood receive strong weights, the system can
over-prioritize familiar categories and miss songs with a similar vibe but a
different label.

---

## Getting Started

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the recommender:

```bash
python -m src.main
```

Run tests:

```bash
python -m pytest
```

---

## Sample Recommendation Output

```text
$ python -m src.main
Loaded songs: 18

User profile: High-Energy Pop
-----------------------------
1. Sunrise City by Neon Echo [pop / happy] - Score: 8.32
   Reasons: genre match (+2.00); mood match (+1.50); energy closeness (+1.46); valence closeness (+0.99); danceability closeness (+0.94); tempo_bpm closeness (+0.71); acousticness closeness (+0.73)
2. Gym Hero by Max Pulse [pop / intense] - Score: 6.64
   Reasons: genre match (+2.00); different mood (+0.00); energy closeness (+1.38); valence closeness (+0.92); danceability closeness (+0.97); tempo_bpm closeness (+0.70); acousticness closeness (+0.68)
3. Afterglow Arcade by Pixel Hearts [synthwave / happy] - Score: 6.28
   Reasons: different genre (+0.00); mood match (+1.50); energy closeness (+1.41); valence closeness (+0.97); danceability closeness (+0.99); tempo_bpm closeness (+0.70); acousticness closeness (+0.71)
4. Rooftop Lights by Indigo Parade [indie pop / happy] - Score: 6.14
   Reasons: different genre (+0.00); mood match (+1.50); energy closeness (+1.36); valence closeness (+0.96); danceability closeness (+0.97); tempo_bpm closeness (+0.75); acousticness closeness (+0.60)
5. Bassline Fever by DJ Circuit [edm / euphoric] - Score: 4.61
   Reasons: different genre (+0.00); different mood (+0.00); energy closeness (+1.33); valence closeness (+0.97); danceability closeness (+0.91); tempo_bpm closeness (+0.72); acousticness closeness (+0.67)

User profile: Chill Lofi
------------------------
1. Library Rain by Paper Lanterns [lofi / chill] - Score: 8.38
   Reasons: genre match (+2.00); mood match (+1.50); energy closeness (+1.50); valence closeness (+0.95); danceability closeness (+0.97); tempo_bpm closeness (+0.71); acousticness closeness (+0.74)
2. Midnight Coding by LoRoom [lofi / chill] - Score: 8.21
   Reasons: genre match (+2.00); mood match (+1.50); energy closeness (+1.40); valence closeness (+0.99); danceability closeness (+0.93); tempo_bpm closeness (+0.75); acousticness closeness (+0.65)
3. Focus Flow by LoRoom [lofi / focused] - Score: 6.77
   Reasons: genre match (+2.00); different mood (+0.00); energy closeness (+1.42); valence closeness (+0.96); danceability closeness (+0.95); tempo_bpm closeness (+0.74); acousticness closeness (+0.70)
4. Spacewalk Thoughts by Orbit Bloom [ambient / chill] - Score: 5.99
   Reasons: different genre (+0.00); mood match (+1.50); energy closeness (+1.40); valence closeness (+0.90); danceability closeness (+0.86); tempo_bpm closeness (+0.64); acousticness closeness (+0.70)
5. Coffee Shop Stories by Slow Stereo [jazz / relaxed] - Score: 4.70
   Reasons: different genre (+0.00); different mood (+0.00); energy closeness (+1.47); valence closeness (+0.84); danceability closeness (+0.99); tempo_bpm closeness (+0.68); acousticness closeness (+0.72)

User profile: Deep Intense Rock
-------------------------------
1. Storm Runner by Voltline [rock / intense] - Score: 8.32
   Reasons: genre match (+2.00); mood match (+1.50); energy closeness (+1.44); valence closeness (+0.97); danceability closeness (+0.94); tempo_bpm closeness (+0.74); acousticness closeness (+0.73)
2. Iron Skyline by North Static [metal / intense] - Score: 6.17
   Reasons: different genre (+0.00); mood match (+1.50); energy closeness (+1.46); valence closeness (+0.91); danceability closeness (+0.90); tempo_bpm closeness (+0.69); acousticness closeness (+0.71)
3. Gym Hero by Max Pulse [pop / intense] - Score: 5.74
   Reasons: different genre (+0.00); mood match (+1.50); energy closeness (+1.47); valence closeness (+0.68); danceability closeness (+0.72); tempo_bpm closeness (+0.64); acousticness closeness (+0.73)
4. Night Drive Loop by Neon Echo [synthwave / moody] - Score: 4.17
   Reasons: different genre (+0.00); different mood (+0.00); energy closeness (+1.20); valence closeness (+0.96); danceability closeness (+0.87); tempo_bpm closeness (+0.50); acousticness closeness (+0.65)
5. Bassline Fever by DJ Circuit [edm / euphoric] - Score: 4.05
   Reasons: different genre (+0.00); different mood (+0.00); energy closeness (+1.48); valence closeness (+0.57); danceability closeness (+0.66); tempo_bpm closeness (+0.61); acousticness closeness (+0.72)

User profile: Conflicted Sad Workout
------------------------------------
1. Gym Hero by Max Pulse [pop / intense] - Score: 6.19
   Reasons: genre match (+2.00); different mood (+0.00); energy closeness (+1.46); valence closeness (+0.48); danceability closeness (+0.92); tempo_bpm closeness (+0.74); acousticness closeness (+0.60)
2. Sunrise City by Neon Echo [pop / happy] - Score: 6.15
   Reasons: genre match (+2.00); different mood (+0.00); energy closeness (+1.38); valence closeness (+0.41); danceability closeness (+0.99); tempo_bpm closeness (+0.68); acousticness closeness (+0.70)
3. Blue Hour Ballad by Marina Vale [r&b / sad] - Score: 4.74
   Reasons: different genre (+0.00); mood match (+1.50); energy closeness (+0.72); valence closeness (+0.93); danceability closeness (+0.72); tempo_bpm closeness (+0.40); acousticness closeness (+0.47)
4. Storm Runner by Voltline [rock / intense] - Score: 4.37
   Reasons: different genre (+0.00); different mood (+0.00); energy closeness (+1.48); valence closeness (+0.77); danceability closeness (+0.86); tempo_bpm closeness (+0.61); acousticness closeness (+0.64)
5. Night Drive Loop by Neon Echo [synthwave / moody] - Score: 4.32
   Reasons: different genre (+0.00); different mood (+0.00); energy closeness (+1.27); valence closeness (+0.76); danceability closeness (+0.93); tempo_bpm closeness (+0.62); acousticness closeness (+0.73)

Bonus mode: mood-first

User profile: High-Energy Pop (Mood-First)
------------------------------------------
1. Sunrise City by Neon Echo [pop / happy] - Score: 9.07
   Reasons: genre match (+2.00); mood match (+1.50); energy closeness (+1.46); valence closeness (+0.99); danceability closeness (+0.94); tempo_bpm closeness (+0.71); acousticness closeness (+0.73)
2. Afterglow Arcade by Pixel Hearts [synthwave / happy] - Score: 7.03
   Reasons: different genre (+0.00); mood match (+1.50); energy closeness (+1.41); valence closeness (+0.97); danceability closeness (+0.99); tempo_bpm closeness (+0.70); acousticness closeness (+0.71)
3. Rooftop Lights by Indigo Parade [indie pop / happy] - Score: 6.89
   Reasons: different genre (+0.00); mood match (+1.50); energy closeness (+1.36); valence closeness (+0.96); danceability closeness (+0.97); tempo_bpm closeness (+0.75); acousticness closeness (+0.60)
4. Gym Hero by Max Pulse [pop / intense] - Score: 6.64
   Reasons: genre match (+2.00); different mood (+0.00); energy closeness (+1.38); valence closeness (+0.92); danceability closeness (+0.97); tempo_bpm closeness (+0.70); acousticness closeness (+0.68)
5. Bassline Fever by DJ Circuit [edm / euphoric] - Score: 4.61
   Reasons: different genre (+0.00); different mood (+0.00); energy closeness (+1.33); valence closeness (+0.97); danceability closeness (+0.91); tempo_bpm closeness (+0.72); acousticness closeness (+0.67)
```

---

## Experiments You Tried

- **Diverse profiles:** High-Energy Pop recommended upbeat pop first, Chill Lofi
  recommended low-energy acoustic lofi first, and Deep Intense Rock recommended
  high-energy rock/metal first.
- **Adversarial profile:** Conflicted Sad Workout asked for `genre=pop` and
  `mood=sad`. Pop songs still ranked above the sad R&B song, showing that genre
  and numerical energy/danceability can overpower mood.
- **Weight sensitivity:** I considered doubling energy and lowering genre, but
  kept the original weights because the current recipe is easier to explain and
  shows a useful bias for the model card.

---

## Limitations and Risks

- The catalog only has 18 songs, so the recommendations are very sensitive to
  which songs happen to be present.
- The system does not use listening behavior, skips, playlists, lyrics, language,
  release year, or artist similarity.
- Genre and mood labels are simplified, which can create filter bubbles.
- A user with mixed preferences may get songs that match genre and energy while
  missing the emotional mood they asked for.

---

## Test Results

```text
============================= test session starts =============================
platform win32 -- Python 3.14.5, pytest-9.1.0, pluggy-1.6.0
rootdir: D:\codex\ai110-module3show-musicrecommendersimulation-starter
plugins: anyio-4.14.0
collected 6 items

tests\test_recommender.py ......                                         [100%]

============================== 6 passed in 0.02s ==============================
```

---

## Reflection

This project helped me understand that recommendations are not magic; they are
data transformations. A simple scoring rule can already feel personalized if it
connects user preferences to song features and explains the match. I also saw
how bias appears quickly: if the weights overvalue genre, the system can keep a
listener inside a narrow category even when another song matches their mood.

AI helped me plan the scoring recipe, implement the CSV loader and recommender,
and think through edge cases. I still had to review the math and outputs myself,
especially for the conflicting sad workout profile. That profile showed me why
model cards matter: a recommender can produce reasonable-looking results while
still reflecting hidden assumptions in the weights and dataset.

[Model Card](model_card.md)
