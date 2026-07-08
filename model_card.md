# Model Card: VibeFinder 1.0

## 1. Model Name

**VibeFinder 1.0**

---

## 2. Intended Use

VibeFinder 1.0 is designed for classroom exploration of music recommendation
logic. It recommends songs from a small CSV catalog based on a user's preferred
genre, mood, and numerical vibe targets. It assumes the user can describe their
current taste with simple labels and values. It should not be used as a real
commercial recommender or as proof of what a person will actually enjoy.

---

## 3. How the Model Works

The model scores each song one at a time. It gives points for matching genre and
mood, then gives smaller similarity points when numerical features are close to
the user's targets. The numerical features are energy, valence, danceability,
tempo, and acousticness. After every song receives a score, the recommender sorts
the songs from highest to lowest and returns the top results with explanation
reasons.

As an optional extra, the model can also blend in a simple collaborative
signal: it looks at a simulated group of 40 "other listeners" and boosts songs
that listeners who share the user's favorite genre or mood also liked, even if
that song's own genre doesn't match. This is content-based filtering and
collaborative filtering working together instead of content-based alone.

Three more optional extras address specific weaknesses I found during testing:
an exploration mode reserves one recommendation slot for a plausible pick
outside the user's favorite genre, as a small counter to filter bubbles; a
feedback loop lets a user mark a past result as liked, saved, or skipped, which
nudges the numeric targets used for the *next* call; and every reason string
now says how many points a mismatch cost (e.g. `different genre (+0.00,
missed +2.00)`) instead of just showing the zero, so it explains not just why a
song scored well, but why it didn't score better.

---

## 4. Data

The catalog has 18 songs in `data/songs.csv`. The dataset includes pop, lofi,
rock, ambient, jazz, synthwave, folk, EDM, R&B, metal, soul, and hip hop. Each
song has a title, artist, genre, mood, energy, tempo, valence, danceability, and
acousticness. I added 8 songs beyond the starter catalog to make the simulation
less narrow. The data is still tiny and manually labeled, so it does not capture
lyrics, real listener behavior, subgenres, culture, language, or artist history.

I also generated `data/listening_history.csv`: 203 simulated "like" events from
40 fake users (via `scripts/generate_listening_history.py`, seeded for
reproducibility), used only by the optional collaborative filtering feature.
This is synthetic data, not real listener behavior, so any pattern it produces
reflects the generator's assumptions, not real music fans.

---

## 5. Strengths

The system works well when a user profile has consistent preferences. The
High-Energy Pop profile recommended `Sunrise City` first because it matched pop,
happy mood, high energy, and danceability. The Chill Lofi profile recommended
`Library Rain` and `Midnight Coding`, which feels reasonable for a quiet focus
playlist. The Deep Intense Rock profile correctly put `Storm Runner` first and
then moved toward intense metal/pop tracks because those shared energy and mood.
I also added a mood-first scoring mode and a simple diversity penalty to make
recommendations feel less repetitive and to show how alternative ranking logic
can change the output.

---

## 6. Limitations and Bias

The biggest limitation is that genre and mood labels are simple and powerful.
This can create a filter bubble where songs outside the user's favorite genre
have trouble ranking highly. In the Conflicted Sad Workout profile, pop songs
ranked above `Blue Hour Ballad` even though that song matched the requested sad
mood. That happened because genre, energy, danceability, and tempo outweighed
mood.

I added a small feedback loop (`apply_feedback()`) so the system isn't
completely static, but it's a limited fix: it only nudges the numeric targets
(energy, valence, danceability, tempo, acousticness), not the genre/mood match
bonus. Testing it on the Chill Lofi profile, skipping `Library Rain` and
saving `Midnight Coding` was enough to flip their order — but only because
they started just 0.17 points apart. A feedback loop can't override a strong
genre/mood match with a handful of clicks; it can only re-sort songs that were
already close. That's a useful, honest limit to know about a "learns from
feedback" feature: it learns, but not enough to fix the genre/mood bias above.

I measured this instead of just describing it. `src/evaluate.py` runs 60
random synthetic profiles through the recommender and computes a genre
concentration score (HHI, 0 = diverse, 1 = one genre). The balanced scorer
alone measured 0.103. Turning on the diversity penalty barely changed that
(0.098), because that penalty only removes duplicate artists within one
profile's own top 5 — it does nothing about which genres dominate across many
different profiles. Turning on collaborative filtering made concentration
*worse* (0.126): with only 40 simulated listeners, two songs (`Sunrise City`,
`Library Rain`) got liked disproportionately often, so the CF signal
amplified their popularity across unrelated profiles instead of adding
variety. That's a small-scale version of the "rich-get-richer" popularity bias
real collaborative-filtering systems are criticized for — it shows that adding
"what other users liked" as a signal isn't automatically a fix for a filter
bubble; with a small enough user base, it can create its own bubble around
whichever songs got an early lead in popularity.

---

## 7. Evaluation

I tested four profiles: High-Energy Pop, Chill Lofi, Deep Intense Rock, and
Conflicted Sad Workout. High-Energy Pop favored pop/happy/high-danceability
songs, while Chill Lofi shifted toward acoustic low-energy tracks. Deep Intense
Rock shifted toward rock and metal, which made sense because those songs had
high energy and intense mood labels. The surprising result was Conflicted Sad
Workout: the sad R&B song appeared third because pop genre and workout-style
energy had more influence than mood. I also ran pytest to verify CSV loading,
scoring explanations, sorted top-k output, and expected edge-case behavior.

I also ran a weight-shift experiment on Conflicted Sad Workout: halving the
genre weight and doubling the energy weight. The sad song did not move up —
instead another high-energy, non-sad track outranked it, and the sad song fell
further down. That told me the mood-mismatch problem isn't really "genre is too
strong"; it's that no numeric feature substitutes for mood, so boosting any of
them just reinforces the same energy-driven bias. See the README's
"Experiments You Tried" section for the full before/after output.

Beyond individual profiles, I ran a batch evaluation (`python -m src.evaluate`)
across 60 randomly generated profiles to see how the system behaves in
aggregate, not just on the four hand-picked examples. That's what produced the
HHI concentration numbers above and confirmed that collaborative filtering
needs a much bigger simulated user base before it would actually reduce bias
instead of amplifying it.

I also specifically tested the two newest features. For exploration mode, I
compared `k=2` results for High-Energy Pop with and without it: normally both
slots are pop songs (`Sunrise City`, `Gym Hero`); with exploration on, the
second slot swaps to `Afterglow Arcade` (synthwave) — confirming it actually
trades score for genre variety instead of silently doing nothing. For the
feedback loop, see the Limitations section above: it reordered two close-
scoring lofi songs but, as expected, couldn't dislodge a strong genre/mood
match in the High-Energy Pop profile with the same size nudge.

---

## 8. Future Work

- Replace the simulated listening history with real (or a much larger simulated) user base so collaborative filtering adds diversity instead of amplifying a couple of popular songs.
- Let the feedback loop also shift genre/mood preference over time (e.g., after enough likes for a different genre, treat it as a second favorite genre), not just the numeric targets, so it can eventually overcome a strong initial genre/mood match.
- Track replay count and use it as its own signal, not just like/save/skip.
- Expand the diversity penalty so it also considers cross-profile genre concentration, not just per-profile artist repeats.
- Add more songs and richer labels such as decade, language, popularity, and lyrical theme.
- Add more scoring modes beyond Balanced and Mood-First, such as Genre-First or Energy-Focused.
- Improve explanations so they are shorter and easier to read.

---

## 9. Personal Reflection

My biggest learning moment was seeing how quickly simple weights create a
recommendation "personality." The model felt smart when it picked lofi songs for
a chill profile, but the conflicting profile showed that it was only following
the rules I gave it. AI helped me brainstorm the scoring recipe and structure
the code, but I had to double-check whether the outputs actually made musical
sense. If I extended this project, I would try a diversity penalty and multiple
scoring modes so users could escape the filter bubble created by one fixed
recipe.
