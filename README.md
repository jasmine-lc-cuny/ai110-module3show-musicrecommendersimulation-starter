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

3. Run the CLI:

```bash
python -m src.main
```

Or run the Streamlit app (adds interactive controls, a live feedback loop, a
"Bias Evaluator" tab with the diversity report and charts, and an "Analyze a
Song" tab where you can type in a real song's stats and score it with the
same algorithm):

```bash
python -m streamlit run app.py
```

### Running Tests
Run the starter tests with:

```bash
pytest
```
$ pytest
============================= test session starts =============================
platform win32 -- Python 3.14.5, pytest-9.1.0, pluggy-1.6.0
rootdir: D:\codex\ai110-module3show-musicrecommendersimulation-starter
configfile: pytest.ini
plugins: anyio-4.14.0
collected 14 items

tests/test_evaluate.py ...                                               [ 21%]
tests/test_recommender.py ...........                                    [100%]

============================== 14 passed in 0.02s ==============================

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
   Reasons: genre match (+2.00); different mood (+0.00, missed +1.50); energy closeness (+1.38); valence closeness (+0.92); danceability closeness (+0.97); tempo_bpm closeness (+0.70); acousticness closeness (+0.68)
3. Afterglow Arcade by Pixel Hearts [synthwave / happy] - Score: 6.28
   Reasons: different genre (+0.00, missed +2.00); mood match (+1.50); energy closeness (+1.41); valence closeness (+0.97); danceability closeness (+0.99); tempo_bpm closeness (+0.70); acousticness closeness (+0.71)
4. Rooftop Lights by Indigo Parade [indie pop / happy] - Score: 6.14
   Reasons: different genre (+0.00, missed +2.00); mood match (+1.50); energy closeness (+1.36); valence closeness (+0.96); danceability closeness (+0.97); tempo_bpm closeness (+0.75); acousticness closeness (+0.60)
5. Bassline Fever by DJ Circuit [edm / euphoric] - Score: 4.61
   Reasons: different genre (+0.00, missed +2.00); different mood (+0.00, missed +1.50); energy closeness (+1.33); valence closeness (+0.97); danceability closeness (+0.91); tempo_bpm closeness (+0.72); acousticness closeness (+0.67)

User profile: Chill Lofi
------------------------
1. Library Rain by Paper Lanterns [lofi / chill] - Score: 8.38
   Reasons: genre match (+2.00); mood match (+1.50); energy closeness (+1.50); valence closeness (+0.95); danceability closeness (+0.97); tempo_bpm closeness (+0.71); acousticness closeness (+0.74)
2. Midnight Coding by LoRoom [lofi / chill] - Score: 8.21
   Reasons: genre match (+2.00); mood match (+1.50); energy closeness (+1.40); valence closeness (+0.99); danceability closeness (+0.93); tempo_bpm closeness (+0.75); acousticness closeness (+0.65)
3. Focus Flow by LoRoom [lofi / focused] - Score: 6.77
   Reasons: genre match (+2.00); different mood (+0.00, missed +1.50); energy closeness (+1.42); valence closeness (+0.96); danceability closeness (+0.95); tempo_bpm closeness (+0.74); acousticness closeness (+0.70)
4. Spacewalk Thoughts by Orbit Bloom [ambient / chill] - Score: 5.99
   Reasons: different genre (+0.00, missed +2.00); mood match (+1.50); energy closeness (+1.40); valence closeness (+0.90); danceability closeness (+0.86); tempo_bpm closeness (+0.64); acousticness closeness (+0.70)
5. Coffee Shop Stories by Slow Stereo [jazz / relaxed] - Score: 4.70
   Reasons: different genre (+0.00, missed +2.00); different mood (+0.00, missed +1.50); energy closeness (+1.47); valence closeness (+0.84); danceability closeness (+0.99); tempo_bpm closeness (+0.68); acousticness closeness (+0.72)

User profile: Deep Intense Rock
-------------------------------
1. Storm Runner by Voltline [rock / intense] - Score: 8.32
   Reasons: genre match (+2.00); mood match (+1.50); energy closeness (+1.44); valence closeness (+0.97); danceability closeness (+0.94); tempo_bpm closeness (+0.74); acousticness closeness (+0.73)
2. Iron Skyline by North Static [metal / intense] - Score: 6.17
   Reasons: different genre (+0.00, missed +2.00); mood match (+1.50); energy closeness (+1.46); valence closeness (+0.91); danceability closeness (+0.90); tempo_bpm closeness (+0.69); acousticness closeness (+0.71)
3. Gym Hero by Max Pulse [pop / intense] - Score: 5.74
   Reasons: different genre (+0.00, missed +2.00); mood match (+1.50); energy closeness (+1.47); valence closeness (+0.68); danceability closeness (+0.72); tempo_bpm closeness (+0.64); acousticness closeness (+0.73)
4. Night Drive Loop by Neon Echo [synthwave / moody] - Score: 4.17
   Reasons: different genre (+0.00, missed +2.00); different mood (+0.00, missed +1.50); energy closeness (+1.20); valence closeness (+0.96); danceability closeness (+0.87); tempo_bpm closeness (+0.50); acousticness closeness (+0.65)
5. Bassline Fever by DJ Circuit [edm / euphoric] - Score: 4.05
   Reasons: different genre (+0.00, missed +2.00); different mood (+0.00, missed +1.50); energy closeness (+1.48); valence closeness (+0.57); danceability closeness (+0.66); tempo_bpm closeness (+0.61); acousticness closeness (+0.72)

User profile: Conflicted Sad Workout
------------------------------------
1. Gym Hero by Max Pulse [pop / intense] - Score: 6.19
   Reasons: genre match (+2.00); different mood (+0.00, missed +1.50); energy closeness (+1.46); valence closeness (+0.48); danceability closeness (+0.92); tempo_bpm closeness (+0.74); acousticness closeness (+0.60)
2. Sunrise City by Neon Echo [pop / happy] - Score: 6.15
   Reasons: genre match (+2.00); different mood (+0.00, missed +1.50); energy closeness (+1.38); valence closeness (+0.41); danceability closeness (+0.99); tempo_bpm closeness (+0.68); acousticness closeness (+0.70)
3. Blue Hour Ballad by Marina Vale [r&b / sad] - Score: 4.74
   Reasons: different genre (+0.00, missed +2.00); mood match (+1.50); energy closeness (+0.72); valence closeness (+0.93); danceability closeness (+0.72); tempo_bpm closeness (+0.40); acousticness closeness (+0.47)
4. Storm Runner by Voltline [rock / intense] - Score: 4.37
   Reasons: different genre (+0.00, missed +2.00); different mood (+0.00, missed +1.50); energy closeness (+1.48); valence closeness (+0.77); danceability closeness (+0.86); tempo_bpm closeness (+0.61); acousticness closeness (+0.64)
5. Night Drive Loop by Neon Echo [synthwave / moody] - Score: 4.32
   Reasons: different genre (+0.00, missed +2.00); different mood (+0.00, missed +1.50); energy closeness (+1.27); valence closeness (+0.76); danceability closeness (+0.93); tempo_bpm closeness (+0.62); acousticness closeness (+0.73)

Bonus mode: mood-first

User profile: High-Energy Pop (Mood-First)
------------------------------------------
1. Sunrise City by Neon Echo [pop / happy] - Score: 9.07
   Reasons: genre match (+2.00); mood match (+1.50); energy closeness (+1.46); valence closeness (+0.99); danceability closeness (+0.94); tempo_bpm closeness (+0.71); acousticness closeness (+0.73)
2. Afterglow Arcade by Pixel Hearts [synthwave / happy] - Score: 7.03
   Reasons: different genre (+0.00, missed +2.00); mood match (+1.50); energy closeness (+1.41); valence closeness (+0.97); danceability closeness (+0.99); tempo_bpm closeness (+0.70); acousticness closeness (+0.71)
3. Rooftop Lights by Indigo Parade [indie pop / happy] - Score: 6.89
   Reasons: different genre (+0.00, missed +2.00); mood match (+1.50); energy closeness (+1.36); valence closeness (+0.96); danceability closeness (+0.97); tempo_bpm closeness (+0.75); acousticness closeness (+0.60)
4. Gym Hero by Max Pulse [pop / intense] - Score: 6.64
   Reasons: genre match (+2.00); different mood (+0.00, missed +1.50); energy closeness (+1.38); valence closeness (+0.92); danceability closeness (+0.97); tempo_bpm closeness (+0.70); acousticness closeness (+0.68)
5. Bassline Fever by DJ Circuit [edm / euphoric] - Score: 4.61
   Reasons: different genre (+0.00, missed +2.00); different mood (+0.00, missed +1.50); energy closeness (+1.33); valence closeness (+0.97); danceability closeness (+0.91); tempo_bpm closeness (+0.72); acousticness closeness (+0.67)

**Screenshot or video** *(optional)*:

![Music Recommender Screenshot](images/recommender-screenshot.png)
---

## Extra Enhancement: Collaborative Filtering

Phase 1 explains the difference between content-based filtering (matching a
song's own attributes to a taste profile) and collaborative filtering (matching
based on what *other* users liked). The core recommender above only does the
first one. To close that gap, I added a simulated "other listeners" dataset
(`data/listening_history.csv`, generated by `scripts/generate_listening_history.py`)
representing 40 fake users and which songs each one "liked."

`collaborative_scores()` in `src/recommender.py` finds simulated users who
share the current profile's favorite genre or mood, then boosts songs that
those "similar" users liked — even if a song's own genre doesn't match. Enable
it with `use_collaborative=True` (CLI: see the "Bonus mode: collaborative
filtering" block below; Streamlit: check "Use collaborative filtering").

```text
Bonus mode: collaborative filtering (simulated listeners)

User profile: High-Energy Pop (Collaborative)
---------------------------------------------
1. Sunrise City by Neon Echo [pop / happy] - Score: 9.82
   Reasons: genre match (+2.00); mood match (+1.50); energy closeness (+1.46); valence closeness (+0.99); danceability closeness (+0.94); tempo_bpm closeness (+0.71); acousticness closeness (+0.73); liked by similar listeners (+1.50)
2. Gym Hero by Max Pulse [pop / intense] - Score: 7.70
   Reasons: genre match (+2.00); different mood (+0.00, missed +1.50); energy closeness (+1.38); valence closeness (+0.92); danceability closeness (+0.97); tempo_bpm closeness (+0.70); acousticness closeness (+0.68); liked by similar listeners (+1.05)
3. Afterglow Arcade by Pixel Hearts [synthwave / happy] - Score: 7.33
   Reasons: different genre (+0.00, missed +2.00); mood match (+1.50); energy closeness (+1.41); valence closeness (+0.97); danceability closeness (+0.99); tempo_bpm closeness (+0.70); acousticness closeness (+0.71); liked by similar listeners (+1.05)
4. Rooftop Lights by Indigo Parade [indie pop / happy] - Score: 6.97
   Reasons: different genre (+0.00, missed +2.00); mood match (+1.50); energy closeness (+1.36); valence closeness (+0.96); danceability closeness (+0.97); tempo_bpm closeness (+0.75); acousticness closeness (+0.60); liked by similar listeners (+0.82)
5. Storm Runner by Voltline [rock / intense] - Score: 4.96
   Reasons: different genre (+0.00, missed +2.00); different mood (+0.00, missed +1.50); energy closeness (+1.41); valence closeness (+0.63); danceability closeness (+0.81); tempo_bpm closeness (+0.57); acousticness closeness (+0.71); liked by similar listeners (+0.82)
```

Notice rank 5: `Storm Runner` is rock/intense — it never appears in the
balanced (content-only) top 5 for this profile. It only shows up because
simulated listeners who share this profile's pop/happy taste also happened to
like it. That's the one thing collaborative filtering can do that pure
content-based scoring cannot: surface a song with none of the "right"
attributes on paper.

## Extra Enhancement: "Why Not?" Explanations

Reasons used to just say `different genre (+0.00)`, which tells you a song
lost points but not how many. Reasons now say `different genre (+0.00,
missed +2.00)` / `different mood (+0.00, missed +1.50)`, and any numeric
feature that scored below 30% of its max points gets a `- far from target`
note. This makes it possible to answer "why didn't this song rank higher?"
directly from the reasons list instead of doing the subtraction yourself.

## Extra Enhancement: "Surprise Me" Exploration Mode

Enable with `exploration=True` (CLI: "Bonus mode: exploration slot" below;
Streamlit: check "Reserve a 'surprise me' discovery slot"). It reserves the
last recommendation slot for the highest-scoring song that is still outside
the user's favorite genre, as a small counter to the filter-bubble problem —
instead of filling every slot with the closest possible match, one slot is
deliberately used for discovery.

```text
Balanced (no exploration), slot 5: Bassline Fever by DJ Circuit [edm / euphoric] - Score: 4.61

Bonus mode: exploration slot (reserves one discovery pick)

User profile: High-Energy Pop (Exploration)
-------------------------------------------
1. Sunrise City by Neon Echo [pop / happy] - Score: 8.32
2. Gym Hero by Max Pulse [pop / intense] - Score: 6.64
3. Afterglow Arcade by Pixel Hearts [synthwave / happy] - Score: 6.28
4. Rooftop Lights by Indigo Parade [indie pop / happy] - Score: 6.14
5. Metro Daydream by Kai North [hip hop / focused] - Score: 4.33
   Reasons: ...; exploration pick: different genre, reserved discovery slot
```

Early on, this had a bug: it searched for *any* different-genre song not
already in the first `k-1` slots, and the natural 5th-place pick
(`Bassline Fever`, edm) already qualified — so the "exploration" slot ended up
showing the exact same song the balanced scorer would have picked anyway,
making the toggle look like it did nothing. Collaborative filtering had the
same "no visible change" problem for a different reason: for this dataset it
boosts scores roughly proportionally, so it rarely reorders the top 5. Fixed
by making exploration search strictly *past* the natural top-`k` cutoff, so
it always swaps in a song (here, `Metro Daydream`, hip hop) that would not
already be on the list — a real trade of a lower score for genre variety, and
now visibly different from both plain balanced and from collaborative
filtering.

## Extra Enhancement: Feedback Loop

The model card used to say the system "cannot learn from user feedback."
`apply_feedback()` in `src/recommender.py` is a small step toward fixing that:
mark a past recommendation as `like`, `save`, or `skip`, and it nudges the
profile's numeric targets (energy, valence, danceability, tempo, acousticness)
toward songs you liked/saved and away from songs you skipped, so the *next*
recommendation call reflects that feedback. In the CLI this runs automatically;
in Streamlit, click 👍/⏭/⭐ under any result and the list re-ranks live.

```text
Bonus mode: feedback loop (skip Library Rain, save Midnight Coding)

User profile: Chill Lofi (Before Feedback)
------------------------------------------
1. Library Rain by Paper Lanterns [lofi / chill] - Score: 8.38
2. Midnight Coding by LoRoom [lofi / chill] - Score: 8.21
3. Focus Flow by LoRoom [lofi / focused] - Score: 6.77

User profile: Chill Lofi (After Feedback)
-----------------------------------------
1. Midnight Coding by LoRoom [lofi / chill] - Score: 8.32
2. Library Rain by Paper Lanterns [lofi / chill] - Score: 8.30
3. Focus Flow by LoRoom [lofi / focused] - Score: 6.89
```

Skipping `Library Rain` and saving `Midnight Coding` was enough to flip their
order, because they started only 0.17 points apart. This also shows the
feedback loop's real limit: it only nudges numeric targets, not the genre/mood
match bonus, so it can reorder close-scoring songs but can't override a strong
genre/mood match with a handful of clicks — a small, honest example of how
much weight the genre/mood bonus really carries in this recipe.

## Extra Enhancement: Quantified Diversity / Bias Report

The model card's bias discussion used to be based on eyeballing a handful of
profiles. `src/evaluate.py` makes that measurable: it generates 60 random-but-plausible
synthetic profiles, runs each through the recommender, and reports a
[Herfindahl-Hirschman Index](https://en.wikipedia.org/wiki/Herfindahl%E2%80%93Hirschman_index)
(HHI) of genre concentration (0 = perfectly diverse, 1 = every result is the
same genre), plus which songs most often land at #1. Run it with
`python -m src.evaluate`.

```text
Balanced scoring (no diversity penalty)
---------------------------------------
Profiles tested: 60
Genre concentration (HHI, 0=diverse .. 1=one genre): 0.103

Most frequent #1 recommendation across profiles:
  Blue Hour Ballad: 9/60 profiles (15.0%)
  Sunrise City: 6/60 profiles (10.0%)
  Desert Bloom: 6/60 profiles (10.0%)

Balanced scoring + diversity penalty
------------------------------------
Genre concentration (HHI): 0.098
(barely moves — the diversity penalty only dedupes artists within one
profile's own top 5, it doesn't change which genres win across profiles)

Balanced scoring + collaborative filtering
------------------------------------------
Genre concentration (HHI): 0.126
Most frequent #1 recommendation across profiles:
  Sunrise City: 12/60 profiles (20.0%)
  Library Rain: 11/60 profiles (18.3%)
  Afterglow Arcade: 5/60 profiles (8.3%)
```

The surprising result: collaborative filtering made concentration *worse*, not
better. With only 40 simulated listeners, a couple of songs (`Sunrise City`,
`Library Rain`) got liked disproportionately often, so the CF signal amplified
their popularity across unrelated profiles — a small-scale example of the
"rich-get-richer" popularity bias real collaborative-filtering systems are
criticized for. See `model_card.md` for the full write-up.

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
- The optional collaborative filtering signal uses *simulated* listening history, not real behavior, and it does not use lyrics or artist relationships
- It can over-prioritize one genre or mood when the weights are strong
- It may produce narrow or repetitive recommendations for some users
- With a small simulated user base, collaborative filtering can amplify popularity bias instead of adding diversity (see the quantified report above)
- The feedback loop only nudges numeric targets (energy, valence, danceability, tempo, acousticness); it cannot override a strong genre/mood match with a few likes/skips, so its "learning" is limited

You will go deeper on this in the model card.

---

## Reflection
I learned that recommenders turn raw data into predictions by translating preferences into a scoring rule. This project also showed that even a simple system can seem personalized while still reflecting hidden assumptions about which features matter most. Bias can show up when the data or weights favor a narrow set of genres, moods, or artist patterns, so explainability and careful evaluation are important.

Read and complete the model card here:

[**Model Card**](model_card.md)
