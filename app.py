import streamlit as st
import pandas as pd
from recommender import get_recommendations
import os
import datetime
import matplotlib.pyplot as plt
import subprocess
import sys

st.set_page_config(page_title="Mood Music App", layout="centered")

# ---------------- FILE CHECK ----------------
files = {
    "users.csv": ["username", "password"],
    "history.csv": ["username", "query", "language", "decade", "timestamp"]
}

for file, cols in files.items():
    if not os.path.exists(file):
        pd.DataFrame(columns=cols).to_csv(file, index=False)

# ---------------- FUNCTIONS ----------------
def load_users():
    return pd.read_csv("users.csv")

def login(username, password):
    users = load_users()
    username = username.strip().lower()
    password = password.strip()

    users["username"] = users["username"].str.strip().str.lower()
    users["password"] = users["password"].astype(str).str.strip()

    return not users[(users["username"] == username) & (users["password"] == password)].empty

def signup(username, password):
    users = load_users()
    username = username.strip().lower()

    if username in users["username"].values:
        return "exists"

    new_user = pd.DataFrame([[username, password]], columns=["username", "password"])
    pd.concat([users, new_user], ignore_index=True).to_csv("users.csv", index=False)
    return "success"

def save_history(username, query, language, decade):
    df = pd.read_csv("history.csv")

    new = pd.DataFrame([{
        "username": username,
        "query": query,
        "language": language,
        "decade": decade,
        "timestamp": datetime.datetime.now()
    }])

    pd.concat([df, new], ignore_index=True).to_csv("history.csv", index=False)

# ---------------- QUERY ----------------
def build_query(mood, language, decade, search_query, trending):
    if search_query:
        return search_query

    query = f"{mood} {language}"

    if decade != "None":
        query += f" {decade}"

    if trending:
        query += " trending"

    return query

# ---------------- SESSION ----------------
for key, val in {
    "logged_in": False,
    "page": "login",
    "username": "",
    "detected_mood": None
}.items():
    if key not in st.session_state:
        st.session_state[key] = val

# ---------------- LOGIN ----------------
if not st.session_state.logged_in:

    if st.session_state.page == "login":
        st.title("🔐 Login")

        u = st.text_input("Username")
        p = st.text_input("Password", type="password")

        if st.button("Login"):
            if login(u, p):
                st.session_state.logged_in = True
                st.session_state.username = u
                st.rerun()
            else:
                st.error("Invalid credentials")

        if st.button("Go to Signup"):
            st.session_state.page = "signup"
            st.rerun()

    else:
        st.title("📝 Signup")

        u = st.text_input("Create Username")
        p = st.text_input("Create Password", type="password")

        if st.button("Create Account"):
            res = signup(u, p)
            if res == "success":
                st.success("Account created!")
                st.session_state.page = "login"
                st.rerun()
            else:
                st.error("Username exists")

        if st.button("Back"):
            st.session_state.page = "login"
            st.rerun()

# ---------------- MAIN APP ----------------
else:
    st.title("🎧 Mood-Based Music App")

    if st.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.rerun()

    is_admin = st.session_state.username == "admin"

    mode = "User View"
    if is_admin:
        mode = st.radio("🔧 Mode", ["User View", "Admin Dashboard"])

    users = pd.read_csv("users.csv")
    history = pd.read_csv("history.csv")

    # ---------------- ADMIN ----------------
    if is_admin and mode == "Admin Dashboard":
        st.subheader("👑 Admin Dashboard")

        st.write("👥 Users:", len(users))
        st.write("📊 Searches:", len(history))

        if not history.empty:

            if st.button("🌍 Language Insights"):
                fig, ax = plt.subplots()
                history["language"].value_counts().plot(kind="bar", ax=ax)
                st.pyplot(fig)

            if st.button("🔥 Query Insights"):
                fig, ax = plt.subplots()
                history["query"].value_counts().head(5).plot(kind="bar", ax=ax)
                st.pyplot(fig)

            if st.button("📅 Decade Insights"):
                fig, ax = plt.subplots()
                history["decade"].value_counts().plot(kind="pie", ax=ax, autopct='%1.1f%%')
                st.pyplot(fig)

        st.dataframe(history)
        st.stop()

    # ---------------- USER ----------------
    st.subheader("🎧 Music Recommendation")

    search_query = st.text_input("🔍 Search")
    trending = st.checkbox("🔥 Trending Mode")

    mood = st.selectbox("Mood", [
        "Happy","Sad","Stressed","Relaxed","Focused",
        "Study","Workout","Yoga","Sleep","Kids","Travel",
        "Energetic","Slow-Lofi","Party","Romantic",
        "Calm","Trending","Chill","Anger (Cool Down)"
    ])

    language = st.selectbox("Language", [
        "English","Hindi","Marathi","Tamil",
        "German","Russian","Korean","Italian","Spanish"
    ])

    decade = st.selectbox("Decade", [
        "None","1970s","1980s","1990s",
        "2000s","2010s","2020-present"
    ])

    # Emotion via subprocess
    import subprocess

    if st.button("🎥 Detect Emotion"):
        st.warning("⚠️ Emotion detection works only on local system")
        st.info("Using selected mood instead")
        st.session_state.detected_mood = mood
        try:
            emotion_python = "emotion_env\\Scripts\\python.exe"

            result = subprocess.check_output(
                [emotion_python, "emotion.py"],
                stderr=subprocess.STDOUT,
                text=True
            )

            st.write("DEBUG:", result)  # optional, can remove later

            detected = result.split("Final Emotion:")[-1].strip()

            st.session_state.detected_mood = detected
            st.success(f"Detected: {detected}")

        except subprocess.CalledProcessError as e:
            st.error("Emotion detection failed")
            st.text(e.output)

    if st.session_state.detected_mood:
        mood = st.session_state.detected_mood

    if st.button("🎵 Get Recommendations"):
        query = build_query(mood, language, decade, search_query, trending)

        save_history(st.session_state.username, query, language, decade)

        songs, playlists = get_recommendations(query)

        st.subheader("🎵 Songs")
        for s in songs:
            st.write(f"{s['name']} - {s['artist']}")
            st.markdown(f"[🌐 Open Song]({s['url']})")

        st.subheader("📻 Playlists")
        for p in playlists:
            st.write(p['name'])
            st.markdown(f"[🎧 Open Playlist]({p['url']})")

    if st.button("🔄 Refresh"):
        st.rerun()