import streamlit as st
import pandas as pd
import datetime as dt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
################################################################
st.set_page_config(
    page_title='Dubai Real Estate',
    page_icon=':bar_chart:',
    layout='wide'
)

st.html('<h1><center>Market and Growth</center></h1>')

# Read
@st.cache_data
def read_data():
    df = pd.read_parquet('data/fully cooked/final.parquet')
    df = df[(df['date'] <= dt.datetime(2024, 6, 1)) & (df['date'] >= dt.datetime(2004, 1, 1))]
    df['year'] = df.year.apply(lambda x: int(x))
    return df

df = read_data()


################################################################
#Side filters
year_value = sorted(df.year.unique())
year_value = [int(i) for i in year_value]
year_value = [i for i in year_value if i >= 2004]

with st.sidebar:
    start_date = st.selectbox('Select Start Year', sorted(df['year'].unique()), index=16)
    


################################################################
#Visuals
    @st.cache_data
    def group_data(df, column):
        gr = df.groupby(['year', column])['actual_worth'].sum().reset_index()
        return gr

    @st.cache_data
    def group_data(df, column=None):
        if column:
            gr = df.groupby(['year', column])['actual_worth'].sum().reset_index()
        else:
            gr = df.groupby(['year'])['actual_worth'].sum().reset_index()
        return gr

    @st.cache_data
    def calculate_growth(df, column=None):
        if column:
            df['growth'] = df.groupby(column)['actual_worth'].pct_change() * 100
        else:
            df['growth'] = df['actual_worth'].pct_change() * 100
        return df


tab1, tab2 = st.tabs([
    'Detailed Visualizations', 'General'
])

# tab1

with tab1:
    with st.container(border=True):
        # Bar
        mapp = {'Property Type' : 'property_type', 'Property Sub Type' : 'property_sub_type','Procedure Name' : 'procedure_name', 'Property Usage' : 'property_usage'}
        
        column_selected = st.selectbox('Select Parameter', mapp.keys())
        column_selected = mapp[column_selected]
    
        data = group_data(df, column_selected)
        filtered_data = data[data['year'] >= start_date]

        fig = px.bar(filtered_data, x='year', y='actual_worth', color=column_selected)
        fig.update_layout(
            xaxis_title="Year",
            yaxis_title= "Actual Worth (AED)")    
        st.html('<h5><center>Market Size</center></h5>')
        st.plotly_chart(fig, on_select='rerun')
        
        # Growth Rate Line
        data = group_data(data, column_selected)
        data = calculate_growth(data,column_selected)

        filtered_data = data[data['year'] >= start_date]

        fig = px.line(filtered_data, x='year', y='growth', labels={'year': 'Year', 'growth': 'Growth Rate (%)'}, color=column_selected)

        fig.update_layout(
            xaxis_title="Year",
            yaxis_title= "Actual Worth (AED)")
        
        st.html('<h5><center>Growth Rate</center></h5>')
        st.plotly_chart(fig, on_select='rerun')    


# tab2
with tab2:
    with st.container(border=True):
        p = st.radio('Select Parameter', ['Year', 'Quarter'], horizontal=True)
        df = df[df['year'] >= start_date]
        # Bar
        if p == 'Year':
            data = df.groupby('year')['actual_worth'].sum().reset_index()
            data = calculate_growth(data)

            fig = make_subplots(rows=1, cols=1, specs=[[{"secondary_y": True}]])
            fig.add_trace(go.Bar(x=data['year'], y=data['actual_worth'], name='Market'), row=1, col=1)
            fig.add_trace(go.Scatter(x=data['year'], y=data['growth'], mode='lines', line=dict(color='red'), name='Growth', hovertemplate='%{y:.2f}%'), row=1, col=1, secondary_y=True)
            st.plotly_chart(fig, on_select='rerun')
        elif p == 'Quarter':
            data = df.groupby('year_quarter')['actual_worth'].sum().reset_index()
            data = calculate_growth(data)

            fig = make_subplots(rows=1, cols=1, specs=[[{"secondary_y": True}]])
            fig.add_trace(go.Bar(x=data['year_quarter'], y=data['actual_worth'], name='Market'), row=1, col=1)
            fig.add_trace(go.Scatter(x=data['year_quarter'], y=data['growth'], mode='lines', line=dict(color='red'), name='Growth', hovertemplate='%{y:.2f}%'), row=1, col=1, secondary_y=True)
            st.plotly_chart(fig, on_select='rerun')        
        
    ################################################################
    













