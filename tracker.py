import streamlit as st
#from google.oauth2 import service_account
#from gsheetsdb import connect
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
import time

st.title('My Fitness Tracker')
st.subheader('Welcome back, User')

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

