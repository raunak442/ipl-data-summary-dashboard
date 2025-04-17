# -*- coding: utf-8 -*-
"""
Created on Wed Apr 16 17:28:47 2025

@author: Raunak
"""

import streamlit as st
import pandas as pd

df_matches = pd.read_csv("ipl_matches_summary.csv")
df_deliveries = pd.read_csv("ipl_deliveries.csv")

st.sidebar.title("🏏 Filters")
seasons = sorted(df_matches['season'].dropna().unique())
selected_season = st.sidebar.selectbox("Select Season", seasons)

filtered_matches = df_matches[df_matches['season']== selected_season]
match_ids = filtered_matches['match_id'].tolist()
 
filtered_deliveries = df_deliveries[df_deliveries['match_id'].isin(match_ids)]


st.title("IPL Data Dashboard")
st.write(f"Showing Stats for {selected_season}")


st.subheader("📊 Season Summary")
st.metric("Total Matches", len(filtered_matches))
st.write("Top Winning Teams")
st.dataframe(filtered_matches['winner'].value_counts())


st.subheader("🏏 Top Run Scorers")
top_batters = (
    filtered_deliveries.groupby("batter")["runs_batter"]
    .sum()
    .sort_values(ascending= False)
    .head(10)
    .reset_index()
)
st.bar_chart(top_batters.set_index("batter"))