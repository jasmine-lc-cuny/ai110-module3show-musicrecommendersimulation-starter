import streamlit as st

from src.recommender import load_songs, recommend_songs

st.set_page_config(page_title="Music Recommender Simulation", page_icon="🎵")
st.title("Music Recommender Simulation")
st.write("Explore how a simple content-based recommender ranks songs from a CSV catalog.")

songs = load_songs("data/songs.csv")
genres = sorted({song["genre"] for song in songs})
moods = sorted({song["mood"] for song in songs})

with st.sidebar:
    st.header("User Profile")
    genre = st.selectbox("Favorite genre", genres, index=genres.index("pop") if "pop" in genres else 0)
    mood = st.selectbox("Favorite mood", moods, index=moods.index("happy") if "happy" in moods else 0)
    energy = st.slider("Target energy", 0.0, 1.0, 0.8, 0.01)
    valence = st.slider("Target valence", 0.0, 1.0, 0.8, 0.01)
    danceability = st.slider("Target danceability", 0.0, 1.0, 0.8, 0.01)
    tempo = st.slider("Target tempo", 50, 200, 120, 1)
    acousticness = st.slider("Target acousticness", 0.0, 1.0, 0.2, 0.01)
    k = st.slider("Number of recommendations", 3, 10, 5, 1)
    scoring_mode = st.selectbox("Scoring mode", ["balanced", "mood-first"])
    diversity_penalty = st.checkbox("Use diversity penalty")

prefs = {
    "genre": genre,
    "mood": mood,
    "energy": energy,
    "valence": valence,
    "danceability": danceability,
    "tempo_bpm": tempo,
    "acousticness": acousticness,
}

results = recommend_songs(
    prefs,
    songs,
    k=k,
    scoring_mode=scoring_mode,
    diversity_penalty=diversity_penalty,
)

st.subheader("Top Recommendations")
for index, (song, score, explanation) in enumerate(results, start=1):
    st.write(f"{index}. {song['title']} by {song['artist']} [{song['genre']} / {song['mood']}]")
    st.write(f"Score: {score:.2f}")
    st.write(f"Reasons: {explanation}")
    st.write("")
