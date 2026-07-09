# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agentic Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

I asked GitHub Copilot to help me complete the Music Recommender Simulation end to end. I wanted it to expand the dataset, implement the recommender logic, improve the README and model card, and help verify the behavior with tests and sample output.

**Prompts used:**

- "Build the Music Recommender Simulation with the required scoring logic, README, model card, and tests."
- "Use a weighted recipe that considers genre, mood, energy, valence, danceability, tempo, and acousticness."
- "Make the recommender return a score and clear reasons for each result."
- "Help document the bias where genre can outweigh mood for a conflicting profile."

**What did the agent generate or change?**

Copilot helped expand the song catalog, implement the recommendation scoring flow in [src/recommender.py](src/recommender.py), add and improve tests in [tests/test_recommender.py](tests/test_recommender.py), and support the documentation updates in [README.md](README.md) and [model_card.md](model_card.md). It also helped generate sample output and explain the scoring behavior.

**What did you verify or fix manually?**

I verified the recommender output by running the CLI and reviewing whether the top songs matched the intended profile. I also checked the test results and manually confirmed that the conflicting profile example showed a realistic limitation: genre and numeric style features could still outweigh mood.

---

## Design Pattern (SF10)

> Document how AI helped you choose or implement a design pattern.

**Which design pattern did you use?**

I used a lightweight wrapper pattern.

**How did AI help you brainstorm or implement it?**

Copilot helped me compare a more complex Strategy-based design with a simpler wrapper approach. The wrapper pattern was easier to explain and fit the starter project well because it let the core scoring functions stay simple while giving the project an object-oriented interface.

**How does the pattern appear in your final code?**

The functional scoring helpers in [src/recommender.py](src/recommender.py) handle the main logic, while the Recommender class provides a clean object-oriented wrapper for tests and reuse. That keeps the implementation modular without overcomplicating the project.

---

## Going Beyond: Collaborative Filtering + Quantified Bias Report

> After finishing the core assignment, CodePath said I had room to go further, so I asked Claude Code to help me close a gap I noticed: the whole project explains collaborative filtering vs. content-based filtering in Phase 1, but the actual code only ever implements content-based filtering.

**What task did I give the agent?**

I asked it to (1) add a real collaborative-filtering signal blended into the existing content-based score, using a simulated "other listeners" dataset since I don't have real user behavior data, and (2) replace my anecdotal bias claims in the model card with an actual measured diversity metric across many profiles, not just the four I hand-picked.

**What did the agent generate or change?**

- `scripts/generate_listening_history.py`: a seeded, reproducible generator that creates `data/listening_history.csv` (203 simulated like-events from 40 fake users, clustered loosely by genre/mood so the data has realistic structure).
- `load_listening_history`, `_find_similar_users`, and `collaborative_scores` in [src/recommender.py](src/recommender.py): find simulated users who share the active profile's favorite genre/mood, then boost songs those users liked.
- `use_collaborative` / `history` parameters threaded through `score_song` and `recommend_songs`, wired into both `src/main.py` (a new "Bonus mode: collaborative filtering" block) and `app.py` (a new checkbox).
- [src/evaluate.py](src/evaluate.py): generates 60 reproducible synthetic profiles, runs them through the recommender, and computes a Herfindahl-Hirschman genre-concentration score plus which songs land at #1 most often, for balanced / diversity-penalty / collaborative-filtering configurations.
- New tests in `tests/test_recommender.py` and a new `tests/test_evaluate.py`.

**What did I verify or fix manually?**

I ran `python -m src.main` and `python -m src.evaluate` myself and read the actual numbers before writing anything in the model card. The result actually surprised me: I expected collaborative filtering to reduce the filter-bubble problem, but the HHI concentration score went *up* (0.103 to 0.126) once CF was on, because only 40 simulated users meant a couple of songs got disproportionately popular. I made the agent keep that honest result in the model card instead of a more flattering made-up one, since it's a more interesting and true finding about small-scale collaborative filtering. I also spot-checked that the diversity penalty and CF settings don't change the core assignment's original 8 required tests.

---

## Going Beyond, Round 2: Feedback Loop, "Why Not?" Explanations, Exploration Mode, Evaluator Dashboard

> A different AI tool I was using for a second opinion suggested four more ideas after reviewing the project: a feedback loop, richer "why not" explanations, an evaluator dashboard tab in Streamlit, and a "surprise me" exploration mode. It also flagged that my README's pasted test output said "8 items" when the project actually had 14 tests by then, and that a Future Work bullet about scoring modes was already done. I asked Claude Code to implement all of it.

**What task did I give the agent?**

Implement all five suggestions: (1) fix the stale docs, (2) add missed-points detail to score reasons, (3) a feedback loop that nudges numeric targets from like/save/skip actions, (4) an exploration mode that reserves a discovery slot, and (5) a second Streamlit tab that visualizes the diversity/bias report I already had in `src/evaluate.py`.

**What did the agent generate or change?**

- Docs: fixed the stale "collected 8 items" pytest snippet in `README.md` and reworded the model card's Future Work bullet that claimed scoring modes weren't done yet.
- `score_song()`: mismatched genre/mood reasons now say `missed +2.00` / `missed +1.50`; numeric closeness reasons below 30% of their max points get a `- far from target` note.
- `apply_feedback()`: nudges the profile's numeric targets toward liked/saved songs and away from skipped ones (exponential-moving-average style update).
- `_apply_diversity_penalty()` / `_reserve_exploration_slot()`: refactored the old inline diversity-penalty logic into a helper, then added an exploration mode that swaps the last slot for a different-genre pick.
- `app.py`: added `st.tabs` with a "Bias Evaluator" tab (runs `src.evaluate.run_diversity_report` for balanced / diversity-penalty / collaborative-filtering configs and shows HHI + bar charts + top-#1 tables via pandas), plus 👍/⏭/⭐ feedback buttons under each recommendation using `st.session_state`, plus an exploration checkbox.
- `src/main.py`: new "Bonus mode: exploration slot" and "Bonus mode: feedback loop" demo blocks.
- 6 new tests in `tests/test_recommender.py`.

**What did I verify or fix manually?**

I deliberately picked demo scenarios that show a real effect instead of a no-op. For exploration mode, the default High-Energy Pop top-5 already contains a non-pop song in slot 5, so nothing visibly changes there — I tested with `k=2` instead, where it visibly swaps `Gym Hero` for `Afterglow Arcade`. For the feedback loop, my first test profile (High-Energy Pop, skip/like) didn't reorder anything because the gap between songs was too large for a numeric nudge to close — so I picked a profile where two songs were only 0.17 points apart (Chill Lofi) and confirmed the skip/save feedback actually flipped their rank. I also ran `python app.py` directly (bare Streamlit mode) and re-ran the dashboard's pandas/report logic standalone to confirm there were no runtime errors before trusting the "boots cleanly" claim, and ran the full pytest suite (18 tests) after each change.

**Bug found through actual use, not just testing:** after using the Streamlit app with its default sidebar values (not the CLI's hand-picked profile), the exploration checkbox and the collaborative filtering checkbox produced the exact same 5 songs in the exact same order. I asked Claude Code to explain why. Root cause: `_reserve_exploration_slot` searched the *entire* ranked list for the first different-genre song not already in the top `k-1` — and the natural k-th song (`Bassline Fever`, edm) already qualified, so "exploration" was a silent no-op that just relabeled the song that would have been there anyway. Fixed by making the search start strictly *past* the natural top-`k` cutoff (`ranked[k:]`), so exploration always pulls in a song that wouldn't already be on the list. Added `test_exploration_still_swaps_when_natural_last_slot_is_already_diverse` to guard against this regression, using the exact prefs that exposed the bug.

---

## Going Beyond, Round 3: Tunebat-Style "Analyze a Song" Tab (and Two Rejected Ideas)

> I wanted a Tunebat-style visual (circular gauges for energy/happiness/danceability/acousticness) in the app. I tried two data-source ideas with Claude Code before landing on a safe one.

**Idea 1 — live Spotify API.** Another AI gave me a full script that called `sp.audio_features()` and `sp.recommendations()` with a hardcoded `CLIENT_SECRET` string in `app.py`. Claude Code flagged two problems before I did anything: (1) a hardcoded secret in a file destined for a public GitHub repo gets exposed the moment it's pushed, and (2) Spotify restricted the `audio-features`/`audio-analysis`/`recommendations` endpoints in November 2024 to apps with "Extended Quota Mode," which new individual-developer apps mostly don't get — so those calls would likely 403 regardless of how the secret was stored. I dropped this entirely rather than debug an API restriction that has nothing to do with my code.

**Idea 2 — GetSongBPM API.** Free, no deprecation issues, generous rate limit, but its song-level response schema only has `tempo`, `key_of`, `danceability`, and `acousticness` — no `energy`, no `valence`, no `genre`, no `mood`. Those missing four are exactly the heaviest-weighted parts of my Phase 3 recipe (genre +2.0, mood +1.5, energy up to +1.5, valence up to +1.0). Wiring up an API to fill in ~28% of my own scoring weights, plus dealing with a mandatory backlink requirement and another API key to keep out of git, wasn't worth it.

**What I actually built:** a third Streamlit tab, "Analyze a Song," where I type in a real song's stats myself (looked up on Tunebat/GetSongBPM's website, not their API) — genre, mood, energy, happiness, danceability, acousticness, tempo — and the app draws the same circular gauges and scores it with the exact same `score_song()` function used everywhere else in the project. Zero API calls, zero secrets, and it covers all 7 of my scoring weights instead of 3.

**What I verified manually:** ran the exact "Hotel California" numbers from the Tunebat screenshot (energy 51, happiness 25, danceability 58, acousticness 1, tempo 75) through `score_song()` directly in a Python shell before trusting the UI, confirmed a sensible score and reasons breakdown, then booted the full Streamlit app on a scratch port and confirmed no traceback in the rendered page.

**Follow-up: cascading genre → song dropdowns.** I wanted the Genre field to be a real dropdown, and picking a genre to show a list of real songs I could just select instead of typing everything by hand. I asked whether GetSongBPM has an official downloadable "Top 100 by genre" list to power this — Claude Code said it doesn't have confirmed knowledge of one, and that scraping their genre pages instead of using their registered API would be a terms-of-service problem, so it recommended against building that. Instead, we hand-curated `data/reference_songs.csv`: 2 real, well-known songs per genre (26 total, covering all 13 genres already in `data/songs.csv`) with manually estimated Tunebat-scale stats. Picking a genre now filters a "pick a real song" dropdown to that genre; picking a song auto-fills the title/artist/mood/energy/happiness/danceability/acousticness/tempo fields via `st.session_state`, still editable afterward. I checked the lookup logic for all 26 songs across all 13 genres in a standalone script (no `KeyError`/`StopIteration`) since I can't click a live dropdown from the terminal, then re-ran the full test suite and booted the app to confirm no runtime errors.

---

## Major Data Import: Renaming the Original Catalog to "codepath" and Adding 695 Real Songs

> I pasted a real chart-hits dataset (`50's^60's^70's^80's.csv`, ~700 real songs from the 1940s-1980s with title/artist/year/BPM/energy/danceability/acousticness/valence/popularity) and asked Claude Code to (1) relabel all 18 original demo songs' `genre` to a single tag, `codepath`, and (2) add every song from the file, with `genre` set to its decade.

**What did I verify before letting it touch the real data?**

Before writing anything to `data/songs.csv`, I had it write the raw pasted content to a scratch file and run analysis first: total row count (695, after the first partial paste turned out to be missing the 40's/50's/60's rows and had to be re-sent complete), a duplicate check (none — 695 unique title/artist pairs), and an encoding check (2 titles from the *Grease* soundtrack had mangled multi-generation mojibake characters, which got cleaned to proper `"Grease"` quotes). Only after those checks passed did it write the transformation into the real file.

**What did the agent generate or change?**

- `data/songs.csv` grew from 18 to 713 rows. The original 18 all got `genre="codepath"`. The 695 real songs got `genre` = their decade (`40's`/`50's`/`60's`/`70's`/`80's`), with energy/valence/danceability/acousticness converted from the source's 0-100 scale to this project's 0-1 scale.
- The source data has no `mood` column, so Claude Code derived one from each song's energy+valence using a small rule (high+high → euphoric, low+low → sad, mid-range → chill/relaxed/energetic) and told me this was a heuristic, not a real label, before I could mistake it for measured data.
- Fixed 4 tests in `tests/test_recommender.py` that hardcoded the old `pop`/`lofi` genre values or the old row count of 18 — one of them (an exploration-mode regression test) got rewritten to use a small synthetic fixture instead of the real catalog, since with 713 songs it got much harder to naturally reproduce the exact edge case it was checking for.
- Rewrote `src/main.py`'s demo profiles (Codepath Originals, 80's Dance Floor, 70's Deep Rock, Starved 40's Workout) to actually exercise the new genre vocabulary, since the old pop/rock/lofi profiles no longer matched anything.
- Fixed `src/evaluate.py`'s hardcoded `GENRES`/`MOODS` constants (used to generate synthetic bias-testing profiles), which still referenced the old musical-genre vocabulary and would have silently made every synthetic profile's genre-match a guaranteed miss.
- Updated `README.md` and `model_card.md`: refreshed every sample output with real, freshly-run numbers instead of hand-edited old text, and replaced the old "Conflicted Sad Workout" bias story with a stronger, real one: requesting the tiny `40's` genre (only 4 songs) with a high-energy target surfaces *zero* `40's` songs — confirmed both as a single hand-picked example and in aggregate across the 60-profile bias report, where `40's` is consistently the smallest genre share (6.7-7.7%) no matter the scoring configuration.

**What surprised me:** collaborative filtering's bias got *more* dramatic after the import, not less. `data/listening_history.csv` was generated before the real songs existed, so it only ever simulates likes for the 18 `codepath` songs. That means CF can never surface a real decade song — it can only pull `codepath` songs up, regardless of which decade a profile actually asks for. In the 60-profile aggregate report, turning on CF pushed the `codepath` share of all recommendations from 22% to 34%. I made sure this stayed in the docs as an explicit, named limitation rather than something to gloss over, since it's a direct consequence of a data pipeline step (the listening-history generator) running before another one (the real-song import) — a very realistic kind of bug/limitation in real ML systems.
