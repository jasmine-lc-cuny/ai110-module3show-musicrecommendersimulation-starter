# 🎵 Music Recommender Simulation

## Project Summary
In this project I built and explained a small music recommender system. The goal is to represent songs and a user taste profile as data, design a scoring rule that turns that data into recommendations, and reflect on what the system does well and where it is limited. My version uses a content-based approach that compares a user's preferred genre, mood, and musical characteristics to songs in a catalog and ranks the best matches.

The catalog now has 713 songs: the 18 original hand-built demo songs (relabeled
genre `codepath` so they read as their own category) plus 695 real, well-known
songs from the 1940s-1980s, imported from an external chart-hits dataset. For
the real songs, `genre` is repurposed to mean *decade* (`40's`/`50's`/`60's`/
`70's`/`80's`) rather than a musical style, since that's how the source data
was organized.

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

**Note on genre:** `genre` in this catalog now has two different meanings
depending on the song. For the 18 original demo songs, it's a fixed tag,
`codepath`. For the 695 real songs, it's the decade the song charted in
(`40's`, `50's`, `60's`, `70's`, `80's`). The scoring math doesn't care which
kind of value it is — it's still just an exact-match check — but it's worth
knowing when reading the sample output below.

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
Song" tab where you pick a genre and a real, well-known song from a small
curated list — its stats auto-fill — or type in your own, then score it with
the same algorithm):

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
collected 19 items

tests/test_evaluate.py ...                                               [ 15%]
tests/test_recommender.py ................                               [100%]

============================== 19 passed in 0.07s ==============================

---

## Sample Recommendation Output
Here is an example of the recommender's output:

 $ python -m src.main
Loaded songs: 713

User profile: Codepath Originals
--------------------------------
1. Sunrise City by Neon Echo [codepath / happy] - Score: 8.32
   Reasons: genre match (+2.00); mood match (+1.50); energy closeness (+1.46); valence closeness (+0.99); danceability closeness (+0.94); tempo_bpm closeness (+0.71); acousticness closeness (+0.73)
2. Afterglow Arcade by Pixel Hearts [codepath / happy] - Score: 8.28
   Reasons: genre match (+2.00); mood match (+1.50); energy closeness (+1.41); valence closeness (+0.97); danceability closeness (+0.99); tempo_bpm closeness (+0.70); acousticness closeness (+0.71)
3. Rooftop Lights by Indigo Parade [codepath / happy] - Score: 8.14
   Reasons: genre match (+2.00); mood match (+1.50); energy closeness (+1.36); valence closeness (+0.96); danceability closeness (+0.97); tempo_bpm closeness (+0.75); acousticness closeness (+0.60)
4. Gym Hero by Max Pulse [codepath / intense] - Score: 6.64
   Reasons: genre match (+2.00); different mood (+0.00, missed +1.50); energy closeness (+1.38); valence closeness (+0.92); danceability closeness (+0.97); tempo_bpm closeness (+0.70); acousticness closeness (+0.68)
5. Bassline Fever by DJ Circuit [codepath / euphoric] - Score: 6.61
   Reasons: genre match (+2.00); different mood (+0.00, missed +1.50); energy closeness (+1.33); valence closeness (+0.97); danceability closeness (+0.91); tempo_bpm closeness (+0.72); acousticness closeness (+0.67)

User profile: 80's Dance Floor
------------------------------
1. (I've Had) The Time of My Life - From  Dirty Dancing  Soundtrack by Bill Medley, Jennifer Warnes [80's / euphoric] - Score: 8.34
   Reasons: genre match (+2.00); mood match (+1.50); energy closeness (+1.44); valence closeness (+0.97); danceability closeness (+0.99); tempo_bpm closeness (+0.74); acousticness closeness (+0.70)
2. The Way It Is by Bruce Hornsby and the Range [80's / euphoric] - Score: 8.33
   Reasons: genre match (+2.00); mood match (+1.50); energy closeness (+1.50); valence closeness (+0.95); danceability closeness (+0.94); tempo_bpm closeness (+0.71); acousticness closeness (+0.73)
3. When the Going Gets Tough, The Tough Get Going by Billy Ocean [80's / euphoric] - Score: 8.32
   Reasons: genre match (+2.00); mood match (+1.50); energy closeness (+1.47); valence closeness (+0.89); danceability closeness (+0.97); tempo_bpm closeness (+0.74); acousticness closeness (+0.75)
4. Situation by Yaz [80's / euphoric] - Score: 8.32
   Reasons: genre match (+2.00); mood match (+1.50); energy closeness (+1.47); valence closeness (+0.97); danceability closeness (+0.98); tempo_bpm closeness (+0.68); acousticness closeness (+0.72)
5. You Make My Dreams (Come True) by Daryl Hall & John Oates [80's / euphoric] - Score: 8.29
   Reasons: genre match (+2.00); mood match (+1.50); energy closeness (+1.47); valence closeness (+0.96); danceability closeness (+0.95); tempo_bpm closeness (+0.66); acousticness closeness (+0.74)

User profile: 70's Deep Rock
----------------------------
1. Rubber Bullets by 10cc [70's / energetic] - Score: 6.84
   Reasons: genre match (+2.00); different mood (+0.00, missed +1.50); energy closeness (+1.40); valence closeness (+0.98); danceability closeness (+1.00); tempo_bpm closeness (+0.72); acousticness closeness (+0.74)
2. Crazy Little Thing Called Love - Remastered 2011 by Queen [70's / energetic] - Score: 6.68
   Reasons: genre match (+2.00); different mood (+0.00, missed +1.50); energy closeness (+1.36); valence closeness (+0.95); danceability closeness (+0.91); tempo_bpm closeness (+0.74); acousticness closeness (+0.71)
3. Psycho Killer - 2005 Remaster by Talking Heads [70's / energetic] - Score: 6.65
   Reasons: genre match (+2.00); different mood (+0.00, missed +1.50); energy closeness (+1.38); valence closeness (+0.85); danceability closeness (+0.99); tempo_bpm closeness (+0.68); acousticness closeness (+0.75)
4. Go Your Own Way - 2004 Remaster by Fleetwood Mac [70's / euphoric] - Score: 6.54
   Reasons: genre match (+2.00); different mood (+0.00, missed +1.50); energy closeness (+1.50); valence closeness (+0.65); danceability closeness (+0.97); tempo_bpm closeness (+0.69); acousticness closeness (+0.73)
5. Born to Run by Bruce Springsteen [70's / energetic] - Score: 6.51
   Reasons: genre match (+2.00); different mood (+0.00, missed +1.50); energy closeness (+1.48); valence closeness (+0.84); danceability closeness (+0.72); tempo_bpm closeness (+0.74); acousticness closeness (+0.72)

User profile: Starved 40's Workout
----------------------------------
1. How Will I Know by Whitney Houston [80's / intense] - Score: 6.04
   Reasons: different genre (+0.00, missed +2.00); mood match (+1.50); energy closeness (+1.48); valence closeness (+0.96); danceability closeness (+0.70); tempo_bpm closeness (+0.72); acousticness closeness (+0.68)
2. Storm Runner by Voltline [codepath / intense] - Score: 6.03
   Reasons: different genre (+0.00, missed +2.00); mood match (+1.50); energy closeness (+1.48); valence closeness (+0.82); danceability closeness (+0.86); tempo_bpm closeness (+0.61); acousticness closeness (+0.75)
3. We Didn't Start the Fire by Billy Joel [80's / intense] - Score: 5.89
   Reasons: different genre (+0.00, missed +2.00); mood match (+1.50); energy closeness (+1.06); valence closeness (+0.96); danceability closeness (+0.88); tempo_bpm closeness (+0.74); acousticness closeness (+0.74)
4. You Might Think by The Cars [80's / intense] - Score: 5.88
   Reasons: different genre (+0.00, missed +2.00); mood match (+1.50); energy closeness (+1.32); valence closeness (+0.99); danceability closeness (+0.76); tempo_bpm closeness (+0.56); acousticness closeness (+0.75)
5. Gym Hero by Max Pulse [codepath / intense] - Score: 5.86
   Reasons: different genre (+0.00, missed +2.00); mood match (+1.50); energy closeness (+1.46); valence closeness (+0.53); danceability closeness (+0.92); tempo_bpm closeness (+0.74); acousticness closeness (+0.71)

This is the profile "Starved 40's Workout": it explicitly requests genre
`40's`, but not one of the only 4 `40's` songs makes the top 5 — every one of
them is low-energy, and the pool is too small to have anything that fits a
high-energy intense target. See the Limitations section for what this means.

Bonus mode: mood-first

User profile: Codepath Originals (Mood-First)
---------------------------------------------
1. Sunrise City by Neon Echo [codepath / happy] - Score: 9.07
   Reasons: genre match (+2.00); mood match (+1.50); energy closeness (+1.46); valence closeness (+0.99); danceability closeness (+0.94); tempo_bpm closeness (+0.71); acousticness closeness (+0.73)
2. Afterglow Arcade by Pixel Hearts [codepath / happy] - Score: 9.03
   Reasons: genre match (+2.00); mood match (+1.50); energy closeness (+1.41); valence closeness (+0.97); danceability closeness (+0.99); tempo_bpm closeness (+0.70); acousticness closeness (+0.71)
3. Rooftop Lights by Indigo Parade [codepath / happy] - Score: 8.89
   Reasons: genre match (+2.00); mood match (+1.50); energy closeness (+1.36); valence closeness (+0.96); danceability closeness (+0.97); tempo_bpm closeness (+0.75); acousticness closeness (+0.60)
4. Sweet Sixteen by Billy Idol [80's / happy] - Score: 6.71
   Reasons: different genre (+0.00, missed +2.00); mood match (+1.50); energy closeness (+1.05); valence closeness (+0.96); danceability closeness (+1.00); tempo_bpm closeness (+0.70); acousticness closeness (+0.75)
5. I'm on My Way by The Proclaimers [80's / happy] - Score: 6.68
   Reasons: different genre (+0.00, missed +2.00); mood match (+1.50); energy closeness (+1.11); valence closeness (+0.97); danceability closeness (+0.87); tempo_bpm closeness (+0.74); acousticness closeness (+0.73)

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

**Important caveat after the real-song import:** `data/listening_history.csv`
was generated before the 695 real songs were added, so it only contains
simulated "likes" for the 18 `codepath` songs. That means collaborative
filtering can only ever boost one of those 18 — it can never surface a real
decade song, no matter what profile you use. That's a real limitation, not
just a demo quirk (see the Future Work in `model_card.md`).

```text
Bonus mode: collaborative filtering (simulated listeners)
Requests a tiny genre (40's, only 4 songs) with a mood ('euphoric') none of them have.

User profile: 40's Euphoric (Collaborative)
-------------------------------------------
1. Bassline Fever by DJ Circuit [codepath / euphoric] - Score: 7.58
   Reasons: different genre (+0.00, missed +2.00); mood match (+1.50); energy closeness (+1.26); valence closeness (+0.92); danceability closeness (+0.91); tempo_bpm closeness (+0.75); acousticness closeness (+0.74); liked by similar listeners (+1.50)
2. You Make My Dreams (Come True) by Daryl Hall & John Oates [80's / euphoric] - Score: 6.38
   Reasons: different genre (+0.00, missed +2.00); mood match (+1.50); energy closeness (+1.46); valence closeness (+0.99); danceability closeness (+1.00); tempo_bpm closeness (+0.71); acousticness closeness (+0.72)
3. Coming Up - Remastered 2011 by Paul McCartney [80's / euphoric] - Score: 6.30
   Reasons: different genre (+0.00, missed +2.00); mood match (+1.50); energy closeness (+1.47); valence closeness (+0.98); danceability closeness (+0.94); tempo_bpm closeness (+0.68); acousticness closeness (+0.73)
4. The Reflex - Single Version; 2010 Remaster by Duran Duran [80's / euphoric] - Score: 6.28
   Reasons: different genre (+0.00, missed +2.00); mood match (+1.50); energy closeness (+1.48); valence closeness (+0.98); danceability closeness (+0.86); tempo_bpm closeness (+0.73); acousticness closeness (+0.73)
5. She Blinded Me With Science - 2009 Remastered Version by Thomas Dolby [80's / euphoric] - Score: 6.28
   Reasons: different genre (+0.00, missed +2.00); mood match (+1.50); energy closeness (+1.50); valence closeness (+0.85); danceability closeness (+1.00); tempo_bpm closeness (+0.68); acousticness closeness (+0.75)
```

Without CF, `Bassline Fever` isn't even close to the top 5 for this profile
(the real 80's songs win on pure content match). With CF on, it jumps to #1 —
simulated listeners who share this profile's euphoric mood happened to like
it, and that one boost (+1.50) was enough to leapfrog a strong field of real
songs. That's the one thing collaborative filtering can do that pure
content-based scoring cannot: surface a song with none of the "right"
attributes on paper. It also incidentally shows the CF blind spot from the
caveat above — it rescues a `codepath` song here, but could never do the same
for an actual `40's` song, since none of those are in the simulated history.

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
Balanced (no exploration), slot 5: Bassline Fever by DJ Circuit [codepath / euphoric] - Score: 6.61

Bonus mode: exploration slot (reserves one discovery pick)

User profile: Codepath Originals (Exploration)
----------------------------------------------
1. Sunrise City by Neon Echo [codepath / happy] - Score: 8.32
2. Afterglow Arcade by Pixel Hearts [codepath / happy] - Score: 8.28
3. Rooftop Lights by Indigo Parade [codepath / happy] - Score: 8.14
4. Gym Hero by Max Pulse [codepath / intense] - Score: 6.64
5. Sweet Sixteen by Billy Idol [80's / happy] - Score: 5.96
   Reasons: ...; exploration pick: different genre, reserved discovery slot
```

Early on, this had a bug: it searched for *any* different-genre song not
already in the first `k-1` slots, and the natural 5th-place pick already
qualified — so the "exploration" slot ended up showing the exact same song the
balanced scorer would have picked anyway, making the toggle look like it did
nothing. Collaborative filtering had a similar "no visible change" problem for
this exact profile, since it boosts codepath scores fairly uniformly. Fixed by
making exploration search strictly *past* the natural top-`k` cutoff, so it
always swaps in a song (here, `Sweet Sixteen`, 80's) that would not already be
on the list — a real trade of a lower score for genre variety, even against a
713-song catalog.

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

User profile: Codepath Chill (Before Feedback)
----------------------------------------------
1. Library Rain by Paper Lanterns [codepath / chill] - Score: 8.38
2. Midnight Coding by LoRoom [codepath / chill] - Score: 8.21
3. Spacewalk Thoughts by Orbit Bloom [codepath / chill] - Score: 7.99

User profile: Codepath Chill (After Feedback)
---------------------------------------------
1. Midnight Coding by LoRoom [codepath / chill] - Score: 8.32
2. Library Rain by Paper Lanterns [codepath / chill] - Score: 8.30
3. Spacewalk Thoughts by Orbit Bloom [codepath / chill] - Score: 7.86
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
Genre concentration (HHI, 0=diverse .. 1=one genre): 0.186

Genre share of all top-k slots:
  70's          24.7%
  codepath      22.0%
  50's          16.7%
  60's          16.3%
  80's          12.7%
  40's           7.7%

Most frequent #1 recommendation across profiles:
  I Saw The Light: 5/60 profiles (8.3%)
  (We're Gonna) Rock Around The Clock: 3/60 profiles (5.0%)
  Lovesick Blues - Show 9: 3/60 profiles (5.0%)

Balanced scoring + diversity penalty
------------------------------------
Genre concentration (HHI): 0.187
(barely moves — the diversity penalty only dedupes artists within one
profile's own top 5, it doesn't change which genres win across profiles)

Balanced scoring + collaborative filtering
------------------------------------------
Genre concentration (HHI): 0.214
Genre share of all top-k slots:
  codepath      34.0%
  70's          21.0%
  50's          15.0%
  60's          12.7%
  80's          10.7%
  40's           6.7%
```

Two things stand out. First, `40's` is the smallest share in *every*
configuration (6.7-7.7%) — the same starvation problem from the "Starved 40's
Workout" example shows up in aggregate across 60 random profiles, not just
that one hand-picked case. Second, collaborative filtering made concentration
*worse*, not better: the `codepath` share jumped from 22.0% to 34.0%, because
CF can only ever boost one of the 18 `codepath` songs (the simulated listening
history predates the real-song import), so it systematically pulls weight
toward that one small pool regardless of what decade the profile actually
asked for — a small-scale example of the "rich-get-richer" popularity bias
real collaborative-filtering systems are criticized for. See `model_card.md`
for the full write-up.

---

## Experiments You Tried
Some experiments I tried with the recommender include:

- Testing different user profiles across the new genre vocabulary: Codepath Originals, 80's Dance Floor, 70's Deep Rock, and Starved 40's Workout
- Comparing the default balanced scoring mode with a mood-first mode
- Trying a diversity penalty to reduce repeated artists in the final recommendations

**Weight-shift experiment:** I temporarily halved the genre weight (`+2.0` to
`+1.0`) and doubled the energy weight (`+1.5` to `+3.0`), then reran the
`Starved 40's Workout` profile (`genre=40's`, `mood=intense`, `energy=0.90`) to
see if the change would let a `40's` song finally crack the top 3.

Before (original weights):

```text
User profile: Starved 40's Workout
----------------------------------
1. How Will I Know by Whitney Houston [80's / intense] - Score: 6.04
2. Storm Runner by Voltline [codepath / intense] - Score: 6.03
3. We Didn't Start the Fire by Billy Joel [80's / intense] - Score: 5.89
```

After (genre halved, energy doubled):

```text
User profile: Starved 40's Workout
----------------------------------
1. How Will I Know by Whitney Houston [80's / intense] - Score: 7.53
2. Storm Runner by Voltline [codepath / intense] - Score: 7.51
3. Gym Hero by Max Pulse [codepath / intense] - Score: 7.31
```

The math stayed valid (scores and ordering still computed correctly), but the
change didn't help — it just reshuffled which *other* genres won. `We Didn't
Start the Fire` (80's) dropped out of the top 3, replaced by another
`codepath` song, but still zero `40's` songs anywhere in sight. Halving the
genre weight didn't matter because the real problem isn't that genre is "too
strong" — it's that there are only 4 `40's` songs and all of them are
low-energy, so no reweighting of genre vs. energy can conjure up a `40's` song
that actually fits a high-energy target. That's a data problem, not a weights
problem, and no amount of recipe-tuning fixes a data problem. I reverted the
weights back to the original recipe after this test.

---

## Limitations and Risks
Some limitations of this recommender are:

- The catalog's decade "genres" are wildly unbalanced (4 `40's` songs vs. 371 `80's` songs), and a small/niche genre can get completely crowded out even when a user explicitly asks for it (see "Starved 40's Workout")
- The optional collaborative filtering signal uses *simulated* listening history that only covers the 18 `codepath` songs, not any real song, and it does not use lyrics or artist relationships
- It can over-prioritize one genre or mood when the weights are strong
- It may produce narrow or repetitive recommendations for some users
- Collaborative filtering can amplify popularity bias instead of adding diversity — with this catalog, it systematically favors the small `codepath` pool over every decade (see the quantified report above)
- The feedback loop only nudges numeric targets (energy, valence, danceability, tempo, acousticness); it cannot override a strong genre/mood match with a few likes/skips, so its "learning" is limited
- Every real song's `mood` is a derived label (from energy/valence), not something a person actually tagged, so it reflects my heuristic's assumptions more than genuine emotional content

You will go deeper on this in the model card.

---

## Reflection
I learned that recommenders turn raw data into predictions by translating preferences into a scoring rule. This project also showed that even a simple system can seem personalized while still reflecting hidden assumptions about which features matter most. Bias can show up when the data or weights favor a narrow set of genres, moods, or artist patterns, so explainability and careful evaluation are important. Importing 695 real songs and repurposing `genre` as decade made this concrete in a way the original 18-song catalog never could: a real, measurable class imbalance (4 vs. 371) turned out to matter more than any of the scoring-recipe tuning I'd done up to that point — no amount of clever weighting fixes a catalog that barely has any songs in the category being asked for.

Read and complete the model card here:

[**Model Card**](model_card.md)
