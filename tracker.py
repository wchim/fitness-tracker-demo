import streamlit as st
#from google.oauth2 import service_account
from gsheetsdb import connect
import numpy as np
import pandas as pd
import plotly.express as px
from datetime import datetime

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

days = []
weights = [] 

# Print results.
for row in rows:
    st.write(f'User {row.UserID} lifted {row.Weight} for {row.Reps} reps!')
    days.append(row.Date)
    weights.append(row.ORM)

user_ls = ['Wayne', 'Ian']

st.title('Trkkr')
st.subheader('Welcome back, User')

# Form
with st.form(key='my_form'):
    uid = st.text_input(label='User ID:')
    lift = st.radio('Lift', ['Bench Press', 'Deadlift'])
    weight_input = st.number_input(label='Weight (lbs):')
    rep_input = st.number_input(label='Reps:')
    ingestion = st.radio('Ingestion', ['Real-time', 'Historical'])
    submit_button = st.form_submit_button(label='Submit')

if submit_button:
    timestamp = datetime.now()
    st.write(f'{user_ls[int(uid)]} lifted {int(weight_input)} pounds {int(rep_input)} times for {lift} on {timestamp}.')

    table = pd.DataFrame(columns={'% of ORM', 'Weight (lbs)', 'Reps'})
    table = table[['% of ORM', 'Weight (lbs)', 'Reps']]

    if rep_input == 1:
        orm = weight_input
    else:
        orm = weight_input*(1+(0.0333*rep_input))

    st.caption(f'Your 1-rep max is: {orm} pounds!')

    # Building graph to update new 
    days.append(timestamp)
    weights.append(orm)

    fig = px.line(x=days, y=weights, title='User Performance Summary')
    st.plotly_chart(fig, use_container_width=True)

    # New entry to write to Google Sheet
    write = pd.DataFrame(columns={'Date', 'UserID', 'Lift', 'Weight', 'Reps', 'ORM', 'IngestionType'})
    write = write[['Date', 'UserID', 'Lift', 'Weight', 'Reps', 'ORM', 'IngestionType']]

    write = write.append({'Date': timestamp,
                  'UserID': uid,
                  'Lift': lift,
                  'Weight': weight_input,
                  'Reps': rep_input,
                  'ORM': orm,
                  'IngestionType': ingestion
    }, ignore_index=True)

    st.table(write)

    # 1-rep max distribution table
    pct = []
    wt = []
    rp = [1, 2, 4, 6, 8, 10, 12, 16, 20, 24, 30]
    for i in range(100, 45, -5):
        pct.append(str(i) + '%')
        wt.append(i/100*orm)

    table['% of ORM'] = pct
    table['Weight (lbs)'] = wt
    table['Reps'] = rp
    st.table(table)

