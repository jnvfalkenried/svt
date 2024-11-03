# main_page.py
import streamlit as st
import pandas as pd
import plotly.express as px
import os
import sys
import asyncio

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from classes.database import Database

st.sidebar.header("Trends")

db = Database()

async def get_data():
    authors_data = await db.get_authors()
    videos_data = await db.get_videos()
    return authors_data, videos_data

authors_data, videos_data = asyncio.run(get_data())
st.title("TikTok Stats Dashboard")

st.header("Author Statistics")
authors_df = pd.DataFrame(authors_data)

if not authors_df.empty:
    fig_authors = px.bar(authors_df, x="nickname", y=["followers", "hearts"], title="Author Followers and Hearts")
    st.plotly_chart(fig_authors)
else:
    st.write("No author data available.")

st.header("Video Statistics")
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

