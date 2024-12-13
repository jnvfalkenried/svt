# src/streamlit_app.py

import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

import pandas as pd
import plotly.express as px
import streamlit as st
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker

from src.postgresql_old.alchemy.models import Author, Challenge, Music, TikTokVideo

load_dotenv()

DATABASE_URL = (
    f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
    f"@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
)
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


def get_authors():
    with Session() as session:
        result = session.execute(select(Author))
        authors = result.scalars().all()
        return [
            {
                "id": author.id,
                "nickname": author.nickname,
                "followers": (
                    author.stats.get("followerCount", 0) if author.stats else 0
                ),
                "hearts": author.stats.get("heartCount", 0) if author.stats else 0,
            }
            for author in authors
        ]


def get_videos():
    with Session() as session:
        result = session.execute(select(TikTokVideo))
        videos = result.scalars().all()
        return [
            {
                "id": video.id,
                "desc": video.desc,
                "play_count": video.stats.get("playCount", 0) if video.stats else 0,
                "digg_count": video.stats.get("diggCount", 0) if video.stats else 0,
            }
            for video in videos
        ]


st.title("TikTok Stats Dashboard")

st.header("Author Statistics")
authors_data = get_authors()
authors_df = pd.DataFrame(authors_data)

if not authors_df.empty:
    fig_authors = px.bar(
        authors_df,
        x="nickname",
        y=["followers", "hearts"],
        title="Author Followers and Hearts",
    )
    st.plotly_chart(fig_authors)
else:
    st.write("No author data available.")

st.header("Video Statistics")
videos_data = get_videos()
videos_df = pd.DataFrame(videos_data)

if not videos_df.empty:
    fig_videos = px.scatter(
        videos_df,
        x="play_count",
        y="digg_count",
        hover_data=["desc"],
        title="Video Play Count vs Digg Count",
    )
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
