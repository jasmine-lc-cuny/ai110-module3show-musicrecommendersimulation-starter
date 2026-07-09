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
            <p style="margin-top:6px; font-size:13px; font-weight:700; color:#ffffff;">{label}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def draw_bar(label, value, display_text, max_value=100):
    """Render a GetSongBPM-style horizontal bar for one audio feature."""
    percent = max(0, min(100, round((value / max_value) * 100)))
    st.markdown(
        f"""
        <div style="margin:6px 0;">
            <div style="display:flex; justify-content:space-between; font-size:13px;
                        font-weight:700; color:#ffffff; margin-bottom:2px;">
                <span>{label}</span>
                <span>{display_text}</span>
            </div>
            <div style="background:#e5e8ef; border-radius:8px; height:14px; width:100%;">
                <div style="background:#2ec4b6; width:{percent}%; height:14px; border-radius:8px;"></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_audio_profile(energy_pct, valence_pct, dance_pct, acoustic_pct, tempo_bpm):
    """Show an audio profile as circular gauges (Tunebat-style) plus bars (GetSongBPM-style)."""
    st.markdown("**Audio profile**")
    gauge_cols = st.columns(4)
    with gauge_cols[0]:
        draw_gauge("Energy", energy_pct)
    with gauge_cols[1]:
        draw_gauge("Happiness", valence_pct)
    with gauge_cols[2]:
        draw_gauge("Danceability", dance_pct)
    with gauge_cols[3]:
        draw_gauge("Acousticness", acoustic_pct)

    draw_bar("Tempo", tempo_bpm, f"{round(tempo_bpm)} BPM", max_value=220)
    draw_bar("Danceability", dance_pct, f"{round(dance_pct)}")
    draw_bar("Energy", energy_pct, f"{round(energy_pct)}")
    draw_bar("Acousticness", acoustic_pct, f"{round(acoustic_pct)}")


def render_feedback_caption(songs):
    """Show which past results feedback has been recorded for, if any."""
    if not st.session_state.feedback:
        return
    songs_by_id = {song["id"]: song["title"] for song in songs}
    feedback_display = ", ".join(
        f"{songs_by_id.get(song_id, song_id)}: {action}"
        for song_id, action in st.session_state.feedback.items()
    )
    st.caption(f"Feedback applied (nudges your targets each rerun): {feedback_display}")


def render_recommendation_list(results, key_prefix):
    """Render a ranked results list: gauges, score breakdown, and feedback buttons."""
    for index, (song, score, explanation) in enumerate(results, start=1):
        st.markdown(f"**{index}. {song['title']}** by {song['artist']} [{song['genre']} / {song['mood']}]")
        st.metric("Score", f"{score:.2f}")
        render_audio_profile(
            song["energy"] * 100,
            song["valence"] * 100,
            song["danceability"] * 100,
            song["acousticness"] * 100,
            song["tempo_bpm"],
        )
        with st.expander("Why this score?"):
            for reason in explanation.split("; "):
                st.write(f"- {reason}")

        like_col, skip_col, save_col = st.columns(3)
        if like_col.button("👍 Like", key=f"{key_prefix}_like_{song['id']}"):
            st.session_state.feedback[song["id"]] = "like"
            st.rerun()
        if skip_col.button("⏭ Skip", key=f"{key_prefix}_skip_{song['id']}"):
            st.session_state.feedback[song["id"]] = "skip"
            st.rerun()
        if save_col.button("⭐ Save", key=f"{key_prefix}_save_{song['id']}"):
            st.session_state.feedback[song["id"]] = "save"
            st.rerun()
        st.write("")

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

tab_recommend, tab_collab, tab_surprise, tab_evaluate, tab_analyze = st.tabs(
    ["Recommender", "Collaborative Filtering", "Surprise Me", "Bias Evaluator", "Analyze a Song"]
)

with tab_recommend:
    render_feedback_caption(songs)

    results = recommend_songs(
        prefs,
        songs,
        k=k,
        scoring_mode=scoring_mode,
        diversity_penalty=diversity_penalty,
    )

    st.subheader("Top Recommendations")
    render_recommendation_list(results, key_prefix="recommend")

with tab_collab:
    st.subheader("Collaborative Filtering")
    st.write(
        "Boosts songs that simulated 'similar' listeners liked, even if a song's own "
        "genre doesn't match your favorite genre — a content-based + collaborative blend "
        "instead of content-based alone."
    )
    render_feedback_caption(songs)

    collab_results = recommend_songs(
        prefs,
        songs,
        k=k,
        scoring_mode=scoring_mode,
        diversity_penalty=diversity_penalty,
        history=history,
        use_collaborative=True,
    )

    st.subheader("Top Recommendations (with Collaborative Filtering)")
    render_recommendation_list(collab_results, key_prefix="collab")

with tab_surprise:
    st.subheader("Surprise Me")
    st.write(
        "Reserves the last recommendation slot for a plausible pick outside your "
        "favorite genre — a small counter to filter-bubble bias instead of always "
        "filling every slot with your usual genre."
    )
    render_feedback_caption(songs)

    surprise_results = recommend_songs(
        prefs,
        songs,
        k=k,
        scoring_mode=scoring_mode,
        diversity_penalty=diversity_penalty,
        exploration=True,
    )

    st.subheader("Top Recommendations (with a Discovery Slot)")
    render_recommendation_list(surprise_results, key_prefix="surprise")

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
        "Pick a decade (40's-80's), then a real, well-known song from that decade — "
        "its stats auto-fill below (a small curated list, not a live lookup). Edit any "
        "value, or search a site like Tunebat/GetSongBPM yourself and type in a "
        "different song's numbers. Either way, it scores against your current "
        "sidebar preferences using the exact same algorithm as the Recommender tab. "
        "No API calls, no external data fetched live."
    )

    analyzed_genre = st.selectbox("Decade", reference_genres, key="analyze_genre_choice")
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
    song_title = name_col.text_input("Song title", value="Introduction", key="analyze_title")
    song_artist = artist_col.text_input("Artist", value="Hank Williams", key="analyze_artist")
    analyzed_mood = st.text_input("Mood", value="happy", key="analyze_mood")

    st.caption("Values are 0-100, the same scale Tunebat/GetSongBPM display on-screen.")
    gauge_cols = st.columns(4)
    analyzed_energy = gauge_cols[0].number_input("Energy", 0, 100, 17, key="analyze_energy")
    analyzed_happiness = gauge_cols[1].number_input("Happiness (valence)", 0, 100, 77, key="analyze_happiness")
    analyzed_danceability = gauge_cols[2].number_input("Danceability", 0, 100, 71, key="analyze_danceability")
    analyzed_acousticness = gauge_cols[3].number_input("Acousticness", 0, 100, 97, key="analyze_acousticness")
    analyzed_tempo = st.number_input("Tempo (BPM)", 40, 220, 61, key="analyze_tempo")

    if st.button("Score this song"):
        render_audio_profile(
            analyzed_energy, analyzed_happiness, analyzed_danceability, analyzed_acousticness, analyzed_tempo
        )

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
