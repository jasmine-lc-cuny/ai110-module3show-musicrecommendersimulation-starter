# 🎵 Music Recommender Simulation

## Project Summary
In this project I built and explained a small music recommender system. The goal is to represent songs and a user taste profile as data, design a scoring rule that turns that data into recommendations, and reflect on what the system does well and where it is limited. My version uses a content-based approach that compares a user's preferred genre, mood, and musical characteristics to songs in a catalog and ranks the best matches.

---

## How The System Works
This project uses a content-based recommender. Each Song contains features such as genre, mood, energy, tempo, valence, danceability, and acousticness, which describe the musical qualities of that song. The UserProfile stores the user’s preferred genre, preferred mood, and target values for the numeric features such as energy, valence, danceability, tempo, and acousticness. In other words, it captures the kind of music the user is trying to find.

The Recommender computes a score for each song by giving points for a genre match and a mood match, then adding extra points based on how closely the song’s numeric features match the user’s target values. Songs that are closer to the user’s taste receive higher scores. To choose which songs to recommend, the system ranks all songs by score and returns the top 𝑘 results. It can also apply a diversity penalty to reduce repeated artists in the final recommendation list.

Finalized Algorithm Recipe:

- `+2.0` for an exact genre match.
- `+1.5` for an exact mood match.
- Up to `+1.5` for energy closeness.
- Up to `+1.0` for valence closeness.
- Up to `+1.0` for danceability closeness.
- Up to `+0.75` for tempo closeness.
- Up to `+0.75` for acousticness closeness.
- Score every song, sort from highest to lowest, and return the top `k`.

A simple workflow looks like this:

- Load songs from data/songs.csv
- Build a user profile with preferred music features
- Score each song against that profile
- Sort the results and return the top recommendations

---

## Getting Started

### Setup

1. Create a virtual environment (I did):

```bash
python -m venv .venv
source .venv/bin/activate      # Mac or Linux
.venv\Scripts\activate         # Windows
```

2. Install dependencies: (I did)

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests
Run the starter tests with:

```bash
pytest
```
starter (main) $ pytest
========================= test session starts ============================
platform linux -- Python 3.12.1, pytest-9.1.1, pluggy-1.6.0
rootdir: /workspaces/ai110-module3show-musicrecommendersimulation-starter
configfile: pytest.ini
plugins: cov-7.1.0, anyio-4.14.1
collected 8 items                                                                  

tests/test_recommender.py ........                                           [100%]

============================ 8 passed in 0.03s ============================


You can add more tests in tests/test_recommender.py.

---

## Sample Recommendation Output
Here is an example of the recommender's output:

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

**Screenshot or video** *(optional)*:

![Music Recommender Screenshot](images/recommender-screenshot.png)
---

## Experiments You Tried
Some experiments I tried with the recommender include:

- Testing different user profiles such as high-energy pop, chill lofi, and deep intense rock
- Comparing the default balanced scoring mode with a mood-first mode
- Trying a diversity penalty to reduce repeated artists in the final recommendations

**Weight-shift experiment:** I temporarily halved the genre weight (`+2.0` to
`+1.0`) and doubled the energy weight (`+1.5` to `+3.0`), then reran the
`Conflicted Sad Workout` profile (`genre=pop`, `mood=sad`, `energy=0.90`) to see
if the change helped or hurt.

Before (original weights):

```text
User profile: Conflicted Sad Workout
------------------------------------
1. Gym Hero by Max Pulse [pop / intense] - Score: 6.19
2. Sunrise City by Neon Echo [pop / happy] - Score: 6.15
3. Blue Hour Ballad by Marina Vale [r&b / sad] - Score: 4.74
```

After (genre halved, energy doubled):

```text
User profile: Conflicted Sad Workout
------------------------------------
1. Gym Hero by Max Pulse [pop / intense] - Score: 6.65
2. Sunrise City by Neon Echo [pop / happy] - Score: 6.53
3. Storm Runner by Voltline [rock / intense] - Score: 5.85
```

The math stayed valid (scores and ordering still computed correctly), but the
change made recommendations *worse*, not more accurate. Lowering the genre
weight didn't let the sad-mood song (`Blue Hour Ballad`) rise into the top 3 —
instead, doubling energy pulled in another high-energy, non-sad track (`Storm
Runner`) and pushed the sad song down further. This shows the mood mismatch
problem isn't caused by genre being "too strong" relative to mood; it's that no
single numeric feature (energy, danceability, tempo) reliably stands in for
mood, so amplifying any of them just reinforces the same energy-driven bias
instead of fixing it. I reverted the weights back to the original recipe after
this test.

---

## Limitations and Risks
Some limitations of this recommender are:

- It only works on a small catalog of songs
- It does not use listening history, lyrics, or artist relationships
- It can over-prioritize one genre or mood when the weights are strong
- It may produce narrow or repetitive recommendations for some users

You will go deeper on this in the model card.

---

## Reflection
I learned that recommenders turn raw data into predictions by translating preferences into a scoring rule. This project also showed that even a simple system can seem personalized while still reflecting hidden assumptions about which features matter most. Bias can show up when the data or weights favor a narrow set of genres, moods, or artist patterns, so explainability and careful evaluation are important.

Read and complete the model card here:

[**Model Card**](model_card.md)
