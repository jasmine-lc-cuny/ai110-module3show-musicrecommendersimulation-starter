import csv

import pandas as pd
import streamlit as st

from src.evaluate import run_diversity_report
from src.recommender import (
    apply_feedback,
    load_listening_history,
    load_songs,
    recommend_songs,
    score_song,
)


def load_reference_songs(csv_path):
    """Load the curated list of real, well-known songs used by the Analyze tab."""
    with open(csv_path, newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        return [
            {
                "genre": row["genre"],
                "title": row["title"],
                "artist": row["artist"],
                "mood": row["mood"],
                "energy": int(row["energy"]),
                "valence": int(row["valence"]),
                "danceability": int(row["danceability"]),
                "acousticness": int(row["acousticness"]),
                "tempo_bpm": int(row["tempo_bpm"]),
            }
            for row in reader
        ]


def draw_gauge(label, percent_value):
    """Render a small Tunebat-style circular gauge for a 0-100 value."""
    value = max(0, min(100, round(percent_value)))
    st.markdown(
        f"""
        <div style="text-align:center; display:inline-block; margin:10px; min-width:88px;">
            <div style="width:80px; height:80px; border-radius:50%;
                        background:conic-gradient(#4664ff {value}%, #e5e8ef 0);
                        display:flex; align-items:center; justify-content:center; margin:0 auto;">
                <div style="width:64px; height:64px; background:white; border-radius:50%;
                            display:flex; align-items:center; justify-content:center;
                            font-weight:700; font-size:15px; color:#162033;">
                    {value}
                </div>
            </div>
            <p style="margin-top:6px; font-size:12px; color:#5b6472;">{label}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.set_page_config(page_title="Music Recommender Simulation", page_icon="🎵")
st.title("Music Recommender Simulation")
st.write("Explore how a simple content-based recommender ranks songs from a CSV catalog.")

songs = load_songs("data/songs.csv")
history = load_listening_history("data/listening_history.csv")
reference_songs = load_reference_songs("data/reference_songs.csv")
genres = sorted({song["genre"] for song in songs})
moods = sorted({song["mood"] for song in songs})
reference_genres = sorted({song["genre"] for song in reference_songs})

if "feedback" not in st.session_state:
    st.session_state.feedback = {}

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
    use_collaborative = st.checkbox(
        "Use collaborative filtering (simulated listeners)",
        help="Boosts songs that simulated users with similar taste liked, even if their genre doesn't match yours.",
    )
    exploration = st.checkbox(
        "Reserve a 'surprise me' discovery slot",
        help="Swaps the last recommendation for a plausible pick outside your favorite genre.",
    )
    if st.button("Clear feedback"):
        st.session_state.feedback = {}

base_prefs = {
    "genre": genre,
    "mood": mood,
    "energy": energy,
    "valence": valence,
    "danceability": danceability,
    "tempo_bpm": tempo,
    "acousticness": acousticness,
}

prefs = (
    apply_feedback(base_prefs, songs, st.session_state.feedback)
    if st.session_state.feedback
    else base_prefs
)

tab_recommend, tab_evaluate, tab_analyze = st.tabs(["Recommender", "Bias Evaluator", "Analyze a Song"])

with tab_recommend:
    if st.session_state.feedback:
        songs_by_id = {song["id"]: song["title"] for song in songs}
        feedback_display = ", ".join(
            f"{songs_by_id.get(song_id, song_id)}: {action}"
            for song_id, action in st.session_state.feedback.items()
        )
        st.caption(f"Feedback applied (nudges your targets each rerun): {feedback_display}")

    results = recommend_songs(
        prefs,
        songs,
        k=k,
        scoring_mode=scoring_mode,
        diversity_penalty=diversity_penalty,
        history=history,
        use_collaborative=use_collaborative,
        exploration=exploration,
    )

    st.subheader("Top Recommendations")
    for index, (song, score, explanation) in enumerate(results, start=1):
        st.write(f"{index}. {song['title']} by {song['artist']} [{song['genre']} / {song['mood']}]")
        st.write(f"Score: {score:.2f}")
        st.write(f"Reasons: {explanation}")

        like_col, skip_col, save_col = st.columns(3)
        if like_col.button("👍 Like", key=f"like_{song['id']}"):
            st.session_state.feedback[song["id"]] = "like"
            st.rerun()
        if skip_col.button("⏭ Skip", key=f"skip_{song['id']}"):
            st.session_state.feedback[song["id"]] = "skip"
            st.rerun()
        if save_col.button("⭐ Save", key=f"save_{song['id']}"):
            st.session_state.feedback[song["id"]] = "save"
            st.rerun()
        st.write("")

with tab_evaluate:
    st.subheader("Quantified Diversity / Bias Report")
    st.write(
        "Runs many randomly generated user profiles through the recommender and "
        "measures how concentrated the results are around a few genres, using a "
        "Herfindahl-Hirschman Index (HHI): 0 = perfectly diverse, 1 = every result "
        "is the same genre."
    )
    num_profiles = st.slider("Number of synthetic profiles", 20, 150, 60, 10)

    if st.button("Run diversity report"):
        configs = {
            "Balanced": {},
            "Balanced + Diversity Penalty": {"diversity_penalty": True},
            "Balanced + Collaborative Filtering": {"history": history, "use_collaborative": True},
        }
        for name, kwargs in configs.items():
            report = run_diversity_report(songs, k=5, num_profiles=num_profiles, **kwargs)
            st.markdown(f"### {name}")
            st.metric("Genre concentration (HHI)", f"{report['hhi']:.3f}")

            genre_df = pd.DataFrame(
                sorted(report["genre_counts"].items(), key=lambda item: item[1], reverse=True),
                columns=["genre", "count"],
            ).set_index("genre")
            st.bar_chart(genre_df)

            top1_rows = report["top1_counts"].most_common(5)
            if top1_rows:
                st.table(pd.DataFrame(top1_rows, columns=["Most frequent #1 song", "Times"]))

with tab_analyze:
    st.subheader("Analyze a Real Song")
    st.write(
        "Pick a genre, then a real, well-known song in that genre — its stats "
        "auto-fill below (a small curated list, not a live lookup). Edit any "
        "value, or search a site like Tunebat/GetSongBPM yourself and type in a "
        "different song's numbers. Either way, it scores against your current "
        "sidebar preferences using the exact same algorithm as the Recommender tab. "
        "No API calls, no external data fetched live."
    )

    analyzed_genre = st.selectbox("Genre", reference_genres, key="analyze_genre_choice")
    matching_songs = [song for song in reference_songs if song["genre"] == analyzed_genre]
    song_choice_key = f"analyze_song_choice_{analyzed_genre}"
    custom_option = "Custom (type your own)"
    song_options = [custom_option] + [f"{song['title']} — {song['artist']}" for song in matching_songs]

    def _apply_reference_song(matching_songs=matching_songs, song_choice_key=song_choice_key, custom_option=custom_option):
        choice = st.session_state[song_choice_key]
        if choice == custom_option:
            return
        selected = next(
            song for song in matching_songs if f"{song['title']} — {song['artist']}" == choice
        )
        st.session_state.analyze_title = selected["title"]
        st.session_state.analyze_artist = selected["artist"]
        st.session_state.analyze_mood = selected["mood"]
        st.session_state.analyze_energy = selected["energy"]
        st.session_state.analyze_happiness = selected["valence"]
        st.session_state.analyze_danceability = selected["danceability"]
        st.session_state.analyze_acousticness = selected["acousticness"]
        st.session_state.analyze_tempo = selected["tempo_bpm"]

    st.selectbox(
        "Pick a real song in this genre",
        song_options,
        key=song_choice_key,
        on_change=_apply_reference_song,
    )

    name_col, artist_col = st.columns(2)
    song_title = name_col.text_input("Song title", value="Hotel California", key="analyze_title")
    song_artist = artist_col.text_input("Artist", value="Eagles", key="analyze_artist")
    analyzed_mood = st.text_input("Mood", value="chill", key="analyze_mood")

    st.caption("Values are 0-100, the same scale Tunebat/GetSongBPM display on-screen.")
    gauge_cols = st.columns(4)
    analyzed_energy = gauge_cols[0].number_input("Energy", 0, 100, 51, key="analyze_energy")
    analyzed_happiness = gauge_cols[1].number_input("Happiness (valence)", 0, 100, 25, key="analyze_happiness")
    analyzed_danceability = gauge_cols[2].number_input("Danceability", 0, 100, 58, key="analyze_danceability")
    analyzed_acousticness = gauge_cols[3].number_input("Acousticness", 0, 100, 1, key="analyze_acousticness")
    analyzed_tempo = st.number_input("Tempo (BPM)", 40, 220, 75, key="analyze_tempo")

    if st.button("Score this song"):
        st.markdown("**Audio profile**")
        gauge_display_cols = st.columns(4)
        with gauge_display_cols[0]:
            draw_gauge("Energy", analyzed_energy)
        with gauge_display_cols[1]:
            draw_gauge("Happiness", analyzed_happiness)
        with gauge_display_cols[2]:
            draw_gauge("Danceability", analyzed_danceability)
        with gauge_display_cols[3]:
            draw_gauge("Acousticness", analyzed_acousticness)

        analyzed_song = {
            "id": -1,
            "title": song_title,
            "artist": song_artist,
            "genre": analyzed_genre,
            "mood": analyzed_mood,
            "energy": analyzed_energy / 100,
            "valence": analyzed_happiness / 100,
            "danceability": analyzed_danceability / 100,
            "acousticness": analyzed_acousticness / 100,
            "tempo_bpm": float(analyzed_tempo),
        }

        analyzed_score, analyzed_reasons = score_song(prefs, analyzed_song, scoring_mode=scoring_mode)

        st.markdown("**Score against your current sidebar profile**")
        st.metric(f"{song_title} by {song_artist}", f"{analyzed_score:.2f}")
        for reason in analyzed_reasons:
            st.write(f"- {reason}")
