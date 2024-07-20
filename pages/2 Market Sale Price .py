# --------
################################################################
# Import

import streamlit as st
import datetime as dt
import pandas as pd
import plotly.express as px
from scripts.dashboard import group_date
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium

################################################################
# Layout
st.set_page_config(
    page_title='Dubai Real Estate',
    page_icon=':bar_chart:',
    layout='wide'
)

################################################################
# Read
@st.cache_data
def read_data():
    df = pd.read_parquet('data/fully cooked/final.parquet')
    return df

@st.cache_data
def filter_data(df):
    max_date = df['date'].max()
    ten_years_ago = max_date - pd.DateOffset(years=10)
    filtered_df = df.query('(trans_group in ["Sales", "Mortgages"]) & (property_usage == "Residential") & (property_sub_type in ["Flat", "Villa"])')
    return filtered_df

df1 = read_data()
df = filter_data(df1)

original_df = df.copy()


################################################################
# Filters

if 'filtered_df' not in st.session_state:
    st.session_state['filtered_df'] = df

with st.sidebar:
    min_value = df['date'].min()
    max_value = df['date'].max()
    
    start_date = st.date_input('Start Date', min_value=min_value, value=max_value - dt.timedelta(days=30), max_value=max_value, help='Select the start date for the data range')
    end_date = st.date_input('End Date', max_value=max_value, help='Select the end date for the data range')
    if start_date > end_date:
        st.warning('Start Date must be less than End Date')
        st.stop()

    # Filter data for the first figure
    st.session_state['filtered_df'] = df[(df['date'] >= pd.to_datetime(start_date)) & (df['date'] <= pd.to_datetime(end_date))]
    st.divider()
    
    if st.checkbox('Select all areas'):
        areas = st.multiselect('Select Area', st.session_state['filtered_df']['area_name'].unique(), st.session_state['filtered_df']['area_name'].unique(), help='Choose the area(s) you want to analyze. Select all to include all areas')
    else:
        areas = st.multiselect('Select Area', st.session_state['filtered_df']['area_name'].unique(), default=['Business Bay'], help='Choose the area(s) you want to analyze. Select all to include all areas')
    if not areas:
        st.warning('Select area(s) to continue')
        st.stop()
    st.session_state['filtered_df'] = st.session_state['filtered_df'][st.session_state['filtered_df']['area_name'].isin(areas)]
    st.divider()
    
    property_sub_type = st.selectbox('Select Property Type', st.session_state['filtered_df']['property_sub_type'].unique(), help='Select the type of property to filter the data', index=0)
    st.session_state['filtered_df'] = st.session_state['filtered_df'][st.session_state['filtered_df']['property_sub_type'] == property_sub_type]
    st.divider()
    

    rooms = st.selectbox('Choose Number of Rooms', st.session_state['filtered_df']['rooms'].unique(),  help='Select the number of rooms to filter the data. Select all to include all room types')
    if not rooms:
        st.warning('Select rooms to continue')
        st.stop()
    st.session_state['filtered_df'] = st.session_state['filtered_df'][st.session_state['filtered_df']['rooms'] == rooms]
    
    st.divider()

################################################################
# Filter data

filtered = st.session_state['filtered_df']
# filtered = filtered[filtered['meter_sale_price'] <= 50000]

if filtered.shape[0] == 0:
    st.warning('No Transactions Data', icon='❗')
    st.stop()

################################################################
# Visuals

grouped_date = group_date(column1='date', column2='meter_sale_price', df=filtered)  # fig1
filtered_for_fig2 = original_df[
    (original_df['area_name'].isin(areas)) &
    (original_df['property_sub_type'] == property_sub_type) &
    (original_df['rooms'] == rooms)
]

grouped_date['month_name'] = grouped_date.Date.dt.strftime('%Y %b')

grouped_date_all = group_date(column1='date', column2='meter_sale_price', df=filtered_for_fig2)  # fig2





def calculate_average_price(df, months_ago):
    target_date = pd.to_datetime("today") - pd.DateOffset(months=months_ago)
    start_date = target_date.replace(day=1)
    end_date = (start_date + pd.DateOffset(months=1)).replace(day=1)
    price_data = df[(df['date'] >= start_date) & (df['date'] < end_date)]
    
    if not price_data.empty:
        return price_data['meter_sale_price'].mean()
    return None

average_6_months_ago = calculate_average_price(filtered_for_fig2, 6)
average_12_months_ago = calculate_average_price(filtered_for_fig2, 12)
average_24_months_ago = calculate_average_price(filtered_for_fig2, 24)

min_date = grouped_date[grouped_date['Date'] == grouped_date['Date'].min()].reset_index().month_name[0]
min_date_price = grouped_date[grouped_date['Date'] == grouped_date['Date'].min()]['Average'].values[0]

max_date = grouped_date[grouped_date['Date'] == grouped_date['Date'].max()].reset_index().month_name[0]
max_date_price = grouped_date[grouped_date['Date'] == grouped_date['Date'].max()]['Average'].values[0]

diff = max_date_price - min_date_price
perc = diff / min_date_price * 100
perc = f"{abs(perc):,.2f}%"

with st.container(border=True):
    st.html(f'<h1><center>Market Sale Price and Value Trend for {rooms} {property_sub_type}</center></h1>')
    st.divider()

    col1, col2,  = st.columns([2,1])
    with col1:
        with st.container(border=True, height=750):
            fig = px.line(x=grouped_date.Date, y=grouped_date.Average)
            st.plotly_chart(fig, height=400)
            fig2 = px.area(x=grouped_date_all.Date, y=grouped_date_all.Average,height=250)
            st.plotly_chart(fig2, height=50)

    
    with col2:
        with st.container(border=True, height=750):
            st.html('<b><center>CURRENT PRICE</center></b>')
            st.html(f'<center>({max_date})</center>')         
            html = f"""
                        <div style="display: flex; justify-content: center; align-items: center;">
                            <p style="margin: 0;">AED</p>
                            <h3 style="margin: 0; margin-left: 10px;">{max_date_price:,.0f}</h3>
                            <p style="margin: 0;">/sqm</p>
                        </div>
                    """         
            st.html(html)   
            
            st.divider()
            
            st.html('<b><center>HISTORICAL PRICE/ Sqm</center></b>')
            with st.container(border=True,):
                left, right = st.columns(2)
                
                with left:
                    st.html(f'<center>6 Months Ago</center>')
                    st.html(f'<center>12 Months Ago</center>')
                    st.html(f'<center>24 Months Ago</center>')
                    
                with right:
                    if average_6_months_ago is None:
                        st.html(f'<center>No Data</center>')
                    else:
                        fmt = f'{average_6_months_ago:,.0f}'
                        html = f"""
                                <div style="display: flex; justify-content: center; align-items: center;">
                                    <p style="margin: 0;">AED</p>
                                    <b style="margin: 0; margin-left: 10px;">{fmt}</b>
                                    <p style="margin: 0;">/sqm</p>
                                </div>
                            """         
                        st.html(html)

                        
                    if average_12_months_ago is None:
                        st.html(f'<center>No Data</center>')
                    else:
                        fmt = f'{average_12_months_ago:,.0f}'
                        html = f"""
                                <div style="display: flex; justify-content: center; align-items: center;">
                                    <p style="margin: 0;">AED</p>
                                    <b style="margin: 0; margin-left: 10px;">{fmt}</b>
                                    <p style="margin: 0;">/sqm</p>
                                </div>
                            """         
                        st.html(html)

                        
                    if average_24_months_ago is None:
                        st.html(f'<center>No Data</center>')
                    else:
                        fmt = f'{average_24_months_ago:,.0f}'
                        html = f"""
                                <div style="display: flex; justify-content: center; align-items: center;">
                                    <p style="margin: 0;">AED</p>
                                    <b style="margin: 0; margin-left: 10px;">{fmt}</b>
                                    <p style="margin: 0;">/sqm</p>
                                </div>
                            """         
                        st.html(html)                        

                        

            
            st.divider()
            st.html('<b><center>PRICE CHANGE IN THE SELECTED PERIOD</center></b>')
            st.html(f'<center>({min_date}-{max_date})</center>')
            if diff > 0:
                html = f"""
                        <div style="display: flex; justify-content: center; align-items: center;">
                            <p style="margin: 0;">AED</p>
                            <h3 style="color: MediumSeaGreen; margin: 0; margin-left: 10px;">{abs(diff):,.0f}</h3>
                            <p style="color: MediumSeaGreen; margin: 0;">({perc}🠉)</p>
                        </div>
                    """
                st.markdown(html, unsafe_allow_html=True)
            else:
                html = f"""
                        <div style="display: flex; justify-content: center; align-items: center;">
                            <p style="margin: 0;">AED</p>
                            <h3 style="color: Tomato; margin: 0; margin-left: 10px;">{abs(diff):,.0f}</h3>
                            <p style="color: Tomato; margin: 0;">({perc}🠋)</p>
                        </div>
                    """
                st.markdown(html, unsafe_allow_html=True)


################################################################
@st.cache_data
def heat_data(df):
    df.dropna(subset='coordinates', inplace=True)
    df['coordinates'] = df.coordinates.apply(lambda x: list(x))   
    return df       

@st.cache_data
def buildings(df):
    data = df.groupby('building_name').agg(
        {
            'actual_worth': ['count', 'sum']
        }
    ).reset_index()
    data.columns = ['Building', 'Number of Unit Sold', 'Total Price']
    data['Pice Per Unit'] = (data['Total Price'] / data['Number of Unit Sold'])
    data['Pice Per Unit'] = data['Pice Per Unit'].apply(lambda x:int(x))
    data = data.sort_values(by='Number of Unit Sold', ascending=False)
    return data

heat = heat_data(filtered)
data = buildings(filtered)

with st.container(border=True):
    col1, col2 = st.columns(2) 
    with st.container(border=True):
        
        with col1:
            st.html('<h5><center>Transactions Heat Map</center></h5>')
            
            m = folium.Map(location=[25.2048,  55.2708], zoom_start=10)
            HeatMap(heat['coordinates']).add_to(m)
        
            st_folium(m,use_container_width=True)
    with st.container(border=True):
        with col2:
            st.html('<h5><center>Transactions By Building</center></h5>')
            
            st.dataframe(data,hide_index=True, use_container_width=True, height=702)