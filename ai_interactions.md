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
