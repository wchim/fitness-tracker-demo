import streamlit as st
#from google.oauth2 import service_account
from gsheetsdb import connect
import numpy as np
import pandas as pd
import altair as alt
import time

# Create a connection object.
conn = connect()

# Perform SQL query on the Google Sheet.
# Uses st.cache to only rerun when the query changes or after 10 min.
@st.cache(ttl=600)
def run_query(query):
    rows = conn.execute(query, headers=1)
    return rows

sheet_url = st.secrets["public_gsheets_url"]
rows = run_query(f'SELECT * FROM "{sheet_url}"')

st.title('My Fitness Tracker')
st.subheader('Welcome back, User')

# Print results.
for row in rows:
    st.write(f"on {row.Day} {row.Fname} lifted {row.Normalize}")

@st.cache
def normalize(weight, rep):
    pass

addPoints = st.button('Click for Gains')

chart_data = pd.DataFrame({
    'Day': ['1', '2', '3', '4', '5'],
    'Normalized': [151.9, 245.5, 267.3, 270, 272.6]
})

#st.line_chart(chart_data)

basic_chart = alt.Chart(chart_data).mark_line().encode(
    x='Day',
    y='Normalized',
).configure_line(
    opacity=1.0,
    color='yellow'
).properties(
    width=700,
    height=500
)

st.altair_chart(basic_chart)

