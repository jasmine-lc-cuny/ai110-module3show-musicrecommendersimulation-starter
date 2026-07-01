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

---

## 4. Data

The catalog has 18 songs in `data/songs.csv`. The dataset includes pop, lofi,
rock, ambient, jazz, synthwave, folk, EDM, R&B, metal, soul, and hip hop. Each
song has a title, artist, genre, mood, energy, tempo, valence, danceability, and
acousticness. I added 8 songs beyond the starter catalog to make the simulation
less narrow. The data is still tiny and manually labeled, so it does not capture
lyrics, real listener behavior, subgenres, culture, language, or artist history.

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
mood. The system also cannot learn from user feedback, so it has no way to know
if a surprising recommendation was actually good.

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

---

## 8. Future Work

- Add user feedback such as likes, skips, saves, and replay count.
- Expand the diversity penalty so the top results do not cluster around one genre or artist.
- Add more songs and richer labels such as decade, language, popularity, and lyrical theme.
- Let users choose scoring modes such as Genre-First, Mood-First, or Energy-Focused.
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
