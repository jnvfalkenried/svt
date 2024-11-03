# src/streamlit_app.py

import os
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker
from postgresql.database_models import Authors, Posts, Music, PostsChallenges
from dotenv import load_dotenv
from pyngrok import ngrok

load_dotenv()

DATABASE_URL = (
    f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
    f"@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
)
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

# Start Ngrok tunnel on Streamlit's port (8501)
NGROK_AUTH_TOKEN = os.getenv("NGROK_AUTH_TOKEN")
ngrok.set_auth_token(NGROK_AUTH_TOKEN)
public_url = ngrok.connect(8501)
st.write(f"App is publicly available at: {public_url}")

# Authentication function
def check_credentials(username, password):
    # Define your credentials here
    return username == "admin" and password == "password"

# Create login form
if "authenticated" not in st.session_state or not st.session_state.authenticated:
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if check_credentials(username, password):
            st.session_state.authenticated = True
            st.success("Logged in successfully!")
        else:
            st.error("Invalid username or password.")
else:
    # Main app code goes here after successful login
    st.title("TikTok Stats Dashboard")

    def get_authors():
        with Session() as session:
            result = session.execute(select(Authors))
            authors = result.scalars().all()
            return [{
                "id": author.id,
                "nickname": author.nickname,
                "followers": author.stats.get("followerCount", 0) if author.stats else 0,
                "hearts": author.stats.get("heartCount", 0) if author.stats else 0
            } for author in authors]

    def get_videos():
        with Session() as session:
            result = session.execute(select(Posts))
            videos = result.scalars().all()
            return [{
                "id": video.id,
                "desc": video.desc,
                "play_count": video.stats.get("playCount", 0) if video.stats else 0,
                "digg_count": video.stats.get("diggCount", 0) if video.stats else 0
            } for video in videos]

    st.header("Author Statistics")
    authors_data = get_authors()
    authors_df = pd.DataFrame(authors_data)

    if not authors_df.empty:
        fig_authors = px.bar(authors_df, x="nickname", y=["followers", "hearts"], title="Author Followers and Hearts")
        st.plotly_chart(fig_authors)
    else:
        st.write("No author data available.")

    st.header("Video Statistics")
    videos_data = get_videos()
    videos_df = pd.DataFrame(videos_data)

    if not videos_df.empty:
        fig_videos = px.scatter(videos_df, x="play_count", y="digg_count", hover_data=["desc"], title="Video Play Count vs Digg Count")
        st.plotly_chart(fig_videos)
    else:
        st.write("No video data available.")

    st.header("Top Authors")
    if not authors_df.empty:
        top_authors = authors_df.nlargest(10, "followers")
        st.table(top_authors[["nickname", "followers", "hearts"]])
    else:
        st.write("No author data available for the top authors table.")

    st.header("Recent Videos")
    if not videos_df.empty:
        st.table(videos_df.head(10))
    else:
        st.write("No video data available for the recent videos table.")