# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

My version, **VibeFinder 1.0**, is a small content-based recommender. It compares
a user's preferred genre, mood, energy, valence, danceability, tempo, and
acousticness to every song in a CSV catalog, then ranks the songs with a
weighted score and explains why each recommendation was chosen.

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

Data flow:

```text
User Preferences -> score each song in songs.csv -> sort scores -> top recommendations with reasons
```

Expected bias: because genre and mood receive strong weights, the system can
over-prioritize familiar categories and miss songs with a similar vibe but a
different label.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

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

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
# e.g.:
# User profile: genre=indie, mood=chill, energy=low
# Recommendations:
#   1. ...
#   2. ...
#   3. ...
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



