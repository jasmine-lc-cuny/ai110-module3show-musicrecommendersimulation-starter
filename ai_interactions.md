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
