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

The catalog has 713 songs in `data/songs.csv`, in two very different parts:

- **18 "codepath" songs**: the original fictional demo catalog I built and
  hand-labeled in Phases 2-3 (genre, mood, energy, tempo, valence,
  danceability, acousticness all set by hand). I relabeled all of their
  `genre` values to a single tag, `codepath`, so this original simulation
  catalog reads as its own distinct category rather than mixing with real
  genre labels.
- **695 real, well-known songs from the 1940s-1980s**: imported from an
  external chart-hits dataset (title, artist, release year, BPM, energy,
  valence, danceability, acousticness, popularity). I repurposed the `genre`
  field to mean *decade* for these songs (`40's`, `50's`, `60's`, `70's`,
  `80's`) instead of a musical style, matching the decade labels the source
  data was already organized by. The decades are very unevenly sized: only 4
  songs from the `40's`, versus 371 from the `80's` — a real, unplanned class
  imbalance that turned out to matter a lot (see Limitations).

The source dataset has no `mood` column, but mood is worth 1.5 points in my
scoring recipe, so I derived one per song from its energy and valence (e.g.
high energy + high valence → `euphoric`; low + low → `sad`; mid-range →
`chill`/`relaxed`/`energetic`). That means every real song's mood is a
computed label, not something a person tagged — a limitation, not a
measurement.

I also generated `data/listening_history.csv`: 203 simulated "like" events from
40 fake users (via `scripts/generate_listening_history.py`, seeded for
reproducibility), used only by the optional collaborative filtering feature.
This only covers the 18 `codepath` songs (it predates the real-song import),
so collaborative filtering can only ever boost one of those 18, never a real
song. This is synthetic data either way, not real listener behavior, so any
pattern it produces reflects the generator's assumptions, not real music fans.

---

## 5. Strengths

The system works well when a user profile has consistent preferences and the
requested decade has enough songs to choose from. The "Codepath Originals"
profile (genre `codepath`, mood `happy`) correctly put `Sunrise City` first
because it matched genre, mood, energy, and danceability. The "80's Dance
Floor" profile (genre `80's`, mood `euphoric`) pulled real, era-appropriate
picks like *(I've Had) The Time of My Life* and *You Make My Dreams (Come
True)* — reasonable results for a large, well-covered decade. The "70's Deep
Rock" profile surfaced real high-energy 70's tracks (Queen, Bruce Springsteen,
Talking Heads) that plausibly fit an "intense rock" request. I also added a
mood-first scoring mode, a diversity penalty, an exploration mode, and a
feedback loop to make recommendations feel less repetitive and to show how
alternative ranking logic can change the output.

---

## 6. Limitations and Bias

**A tiny "genre" gets starved out, even when explicitly requested.** The
`40's` decade only has 4 songs, all with low energy (0.17-0.42) and calm
moods. I tested a "Starved 40's Workout" profile — explicitly requesting
genre `40's` but with high-energy, intense-mood targets (a workout playlist
from the 1940s, essentially a contradiction the dataset can't satisfy). Not
one actual `40's` song made the top 5. Every result came from `80's` or
`codepath` instead, because their sheer numbers (371 and 18 candidates with a
wide range of energy levels) meant *something* would out-score a low-energy,
niche-mood match every time. This is a direct, measured example of a real
recommender problem: catalog imbalance can make a whole category functionally
invisible, no matter what the user explicitly asks for, once a strong numeric
mismatch is added to the mix.

I added a small feedback loop (`apply_feedback()`) so the system isn't
completely static, but it's a limited fix: it only nudges the numeric targets
(energy, valence, danceability, tempo, acousticness), not the genre/mood match
bonus. Testing it on a codepath chill profile, skipping `Library Rain` and
saving `Midnight Coding` was enough to flip their order — but only because
they started just 0.17 points apart. A feedback loop can't override a strong
genre/mood match with a handful of clicks; it can only re-sort songs that were
already close. That's a useful, honest limit to know about a "learns from
feedback" feature: it learns, but not enough to fix the catalog-imbalance bias
above.

I measured concentration instead of just describing it. `src/evaluate.py` runs
60 random synthetic profiles through the recommender and computes a genre
concentration score (HHI, 0 = diverse, 1 = one genre) — genre here means the
new vocabulary (`codepath` plus the five decades). The balanced scorer alone
measured 0.186. Turning on the diversity penalty barely changed that (0.187),
because that penalty only removes duplicate artists within one profile's own
top 5 — it does nothing about which genres dominate across many different
profiles. Turning on collaborative filtering made concentration *worse*
(0.214): the `codepath` share of all recommended slots jumped from 22% to 34%,
because CF can only ever boost one of the 18 `codepath` songs (the simulated
listening history predates the real-song import), so it systematically pulls
weight toward that one small pool regardless of what decade the profile asked
for. Across every configuration, `40's` stayed the smallest share of results
(6.7-7.7%) despite being requestable like any other genre — the same
starvation problem showing up in aggregate, not just in one hand-picked
profile. That's a small-scale version of the "rich-get-richer" popularity bias
real collaborative-filtering systems are criticized for, plus a reminder that
adding "what other users liked" as a signal isn't automatically a fix for a
filter bubble — with an unevenly sized catalog, it can make the imbalance
worse.

---

## 7. Evaluation

I tested four profiles: "Codepath Originals" (genre `codepath`), "80's Dance
Floor" (genre `80's`, mood `euphoric`), "70's Deep Rock" (genre `70's`, mood
`intense`), and "Starved 40's Workout" (genre `40's`, mood `intense`, but
40's-inappropriate high-energy targets). The first three behaved sensibly:
each pulled genre-and-mood-appropriate songs, real or codepath. The fourth was
the interesting one — see Limitations for why not a single `40's` song made
the cut.

I also re-ran the weight-shift experiment (halving the genre weight, doubling
the energy weight) on the Starved 40's Workout profile. Before: top 3 were
`How Will I Know` (80's), `Storm Runner` (codepath), `We Didn't Start the
Fire` (80's). After the shift: `How Will I Know` and `Storm Runner` still led,
but `We Didn't Start the Fire` dropped out of the top 3, replaced by another
codepath song, `Gym Hero`. Lowering the genre weight didn't help a single
`40's` song crack the list — it just changed which non-`40's` songs won. Same
conclusion as before: no numeric feature substitutes for what's actually
missing (enough `40's` candidates that also fit the energy target), so
reweighting just reshuffles which other genre dominates.

Beyond individual profiles, I ran a batch evaluation (`python -m src.evaluate`)
across 60 randomly generated profiles (now drawn from the `codepath` +
5-decade vocabulary) to see how the system behaves in aggregate, not just on
the four hand-picked examples. That's what produced the HHI concentration
numbers above and confirmed that collaborative filtering, scoped to only the
18 `codepath` songs, systematically favors that pool over every decade,
including the ones explicitly requested — and that `40's` stays the smallest
share of recommendations under every configuration.

I also specifically tested the two newest features against the new catalog.
For exploration mode, I compared `k=2` results for Codepath Originals with and
without it: normally both slots are codepath songs (`Sunrise City`, `Afterglow
Arcade`); with exploration on, the last slot force-swaps to a real decade
song — confirming it still trades score for genre variety instead of silently
doing nothing, even against a 713-song catalog. For the feedback loop, see the
Limitations section above: it reordered two close-scoring codepath songs but,
as expected, couldn't dislodge a strong genre/mood match with the same size
nudge.

---

## 8. Future Work

- Rebalance or resample the decade catalog (or add a small-genre boost) so `40's` and other under-represented decades aren't structurally invisible.
- Extend `data/listening_history.csv` to cover real songs, not just the 18 `codepath` songs, so collaborative filtering can actually surface real-song discoveries instead of only ever boosting the same small pool.
- Get real, human-labeled mood tags for the 695 imported songs instead of a derived energy/valence heuristic.
- Let the feedback loop also shift genre/mood preference over time (e.g., after enough likes for a different genre, treat it as a second favorite genre), not just the numeric targets, so it can eventually overcome a strong initial genre/mood match.
- Track replay count and use it as its own signal, not just like/save/skip.
- Expand the diversity penalty so it also considers cross-profile genre concentration, not just per-profile artist repeats.
- Add richer labels such as language, popularity, and lyrical theme to the real-song catalog.
- Add more scoring modes beyond Balanced and Mood-First, such as Genre-First or Energy-Focused.
- Improve explanations so they are shorter and easier to read.

---

## 9. Personal Reflection

My biggest learning moment was seeing how quickly simple weights create a
recommendation "personality." The model felt smart when it picked lofi-style
codepath songs for a chill profile, but the conflicting profiles showed it was
only following the rules I gave it. Importing 695 real songs and relabeling
genre as decade was the biggest surprise of the whole project: I expected more
data to make the system feel richer, but instead it exposed a sharper bias
than anything in the original 18-song catalog — a tiny decade like the `40's`
can be requested by name and still get completely crowded out, just because
there are only 4 of them next to 371 `80's` songs. AI helped me brainstorm the
scoring recipe, structure the code, and design the data import, but I had to
double-check every claim against real output — especially the mood labels,
since those are a heuristic I invented, not something anyone actually tagged.
If I extended this project, I would fix the catalog imbalance itself before
adding more ranking logic, since no amount of clever scoring can recommend
songs that are barely represented in the data to begin with.
