# AI Interactions Log

## Agentic Workflow

**What task did you give the agent?**

I asked Codex to help me complete the Music Recommender Simulation from the
CodePath project instructions. I wanted it to fork the starter repo, expand the
dataset, implement the recommender, run CLI/tests, and finish the README and
model card. I also asked it to keep the commit history meaningful so the project
shows planning, implementation, and documentation work.

**Prompts used:**

- "Build the Music Recommender Simulation project with the required scoring logic, README, model card, tests, and commits."
- "Use a weighted scoring recipe with genre, mood, energy, valence, danceability, tempo, and acousticness."
- "Make sure the recommender returns a score and readable reasons."
- "Document the bias where genre can overpower mood for a conflicting profile."

**What did the agent generate or change?**

Codex forked and cloned the starter repo, expanded `data/songs.csv` from 10 to
18 songs, implemented `load_songs`, `score_song`, and `recommend_songs` in
`src/recommender.py`, and updated `src/main.py` to print recommendations for
four profiles. It also expanded `tests/test_recommender.py`, ran
`python -m src.main`, ran `python -m pytest`, completed `README.md`, completed
`model_card.md`, and filled this AI interactions log.

**What did you verify or fix manually?**

I reviewed the recommendation output to see if the top songs made musical sense.
The main manual judgment was keeping the genre/mood weights simple instead of
adding too many extra rules. I also checked the Conflicted Sad Workout profile
because it exposed a useful limitation: pop songs ranked above the sad R&B song
because genre and workout-style numerical features carried more total weight.

---

## Design Pattern

**Which design pattern did you use?**

I used a lightweight wrapper pattern. The core scoring logic is functional
(`load_songs`, `score_song`, `recommend_songs`), and the `Recommender` class
wraps that logic for the starter tests and OOP interface.

**How did AI help you brainstorm or implement it?**

AI helped compare a full Strategy pattern against a simpler design. A Strategy
pattern would make sense for multiple scoring modes, but it was more complexity
than the base assignment needed. The wrapper design kept the system modular
without making the code hard to explain.

**How does the pattern appear in your final code?**

`src/recommender.py` contains both dataclasses (`Song`, `UserProfile`) and the
`Recommender` class, but the class delegates scoring to the same functional
helpers used by `src/main.py`. This keeps the CLI simulation, tests, and OOP
interface consistent.
