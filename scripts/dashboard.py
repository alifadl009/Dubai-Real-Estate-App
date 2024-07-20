import streamlit as st

@st.cache_data
def group_date(column1, column2, df):
    date_summary = df.groupby(column1).agg(
        {column2: ['mean', 'median', 'count', 'sum']}).reset_index()
    if type(column1) is list:
        date_summary.columns = ['Date', column1[1].title().replace('_', ' '), 'Average', 'Median', 'Count', 'Total']
    else:
        date_summary.columns = ['Date', 'Average', 'Median', 'Count', 'Total']
    return date_summary


