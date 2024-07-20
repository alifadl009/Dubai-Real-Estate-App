# Streamlit App
################################################################
# Import Libraries
import datetime as dt
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
# from streamlit_folium import st_folium
# import folium

################################################################
# Page Configuration
st.set_page_config(
    page_title='Dubai Real Estate',
    page_icon=':bar_chart:',
    layout='wide'
)
st.html('<h1><center>Dubai Real Estate</center></h1>')
logo_url = 'dubai_real_estate_logo.jpg'
# st.image(logo_url, width=850,)
st.logo(logo_url) # Logo


# Read and Filter Data
@st.cache_data
def read_data():
    
    df = pd.read_parquet('./data/fully cooked/final.parquet')
    return df

@st.cache_data
def filter_data(df):
    max_date = df['date'].max()
    ten_years_ago = max_date - pd.DateOffset(years=10)
    filtered_df = df.query('(trans_group in ["Sales", "Mortgages"]) & (property_usage == "Residential") & (property_sub_type in ["Flat", "Villa"])')
    return filtered_df

df1 = read_data()
df = filter_data(df1)
    
    
################################################################
# Sidebar Filters
with st.sidebar:
    min_value = df.date.min()
    max_value = df.date.max()
    start_date = st.date_input('Start Date', min_value=min_value, value=max_value - dt.timedelta(days=30), max_value=max_value, help='Select the start date for the data range')
    end_date = st.date_input('End Date', max_value=max_value, help='Select the end date for the data range')
    if start_date > end_date:
        st.warning('Start Date must be less than end Date')
        st.stop()
        
    if st.checkbox('Select all'):
        area = st.multiselect('Select Area', df.area_name.unique(),df.area_name.unique(), help='Choose the area(s) you want to analyze. Select all to include all areas')
             
    else:
        area = st.multiselect('Select Area', df.area_name.unique(), default=['Business Bay'], help='Choose the area(s) you want to analyze. Select all to include all areas')
    if not area:
        st.warning('Select area to continue')
        st.stop()
    
    transaction_group = st.selectbox('Select Transaction Group', df.trans_group.unique(), help='Choose the transaction group to filter the data')
    property_sub_type = st.selectbox('Select Property Type', df.property_sub_type.unique(), index=1, help='Select the type of property to filter the data')
    
    if st.checkbox('Select all '):
        rooms = st.multiselect('Choose Number of Rooms', ['Studio', '1 B/R', '2 B/R', '3 B/R', '4 B/R'], ['Studio', '1 B/R', '2 B/R', '3 B/R', '4 B/R'], help='Select the number of rooms to filter the data. Select all to include all room types')
    else:
        rooms = st.multiselect('Choose Number of Rooms', ['Studio', '1 B/R', '2 B/R', '3 B/R', '4 B/R'], default='1 B/R', help='Select the number of rooms to filter the data. Select all to include all room types')
    if not rooms:
        st.warning('Select rooms to continue')
        st.stop()
        
# with st.container(border=True):
    
#     col1, col2, col3 = st.columns(3)

#     with col1:
#         min_value = df.date.min()
#         max_value = df.date.max()

#         start_date = st.date_input('Start Date', min_value=min_value, value=max_value - dt.timedelta(days=30), max_value=max_value)
#         end_date = st.date_input('End Date', max_value=max_value)
#         if start_date > end_date:
#             st.warning('Start Date must be less than end Date')
#             st.stop()

#     with col2:
#         if st.checkbox('Select all Areas'):
#             area = st.multiselect('Select Area', df.area_name.unique(), df.area_name.unique())
#         else:
#             area = st.multiselect('Select Area', df.area_name.unique(), default='Marsa Dubai')
#         if not area:
#             st.warning('Select area to continue')
#             st.stop()
        
#         transaction_group = st.selectbox('Select Transaction Group', df.trans_group.unique())

#     with col3:
#         if st.checkbox('Select all Rooms'):
#             rooms = st.multiselect('Choose Number of Rooms', ['Studio', '1 B/R', '2 B/R', '3 B/R', '4 B/R'], ['Studio', '1 B/R', '2 B/R', '3 B/R', '4 B/R'])
#         else:
#             rooms = st.multiselect('Choose Number of Rooms', ['Studio', '1 B/R', '2 B/R', '3 B/R', '4 B/R'], default='1 B/R')
#         if not rooms:
#             st.warning('Select rooms to continue')
#             st.stop()
#         property_sub_type = st.selectbox('Select Property Sub Type', df.property_sub_type.unique())
        
################################################################       
# Filter
filtered = df.query('(date >= @start_date) and (date <= @end_date) and (property_sub_type == @property_sub_type) and (trans_group == @transaction_group) and (rooms == @rooms) and (area_name == @area)')
hs = df.query('(date >= @start_date) and (date <= @end_date) and (property_sub_type == @property_sub_type) and (rooms == @rooms) and (area_name == @area) ')
bx = df.query('(date >= @start_date) and (date <= @end_date) and (property_sub_type == @property_sub_type) and (rooms.isin(["Studio", "1 B/R", "2 B/R", "3 B/R", "4 B/R"]) and (area_name == @area))')

if filtered.shape[0] == 0:
    st.warning('No Transactions Data', icon='❗')
    st.stop()
################################################################
# Metrics
total_unit_sold_count = int(filtered['actual_worth'].count())
total_unit_sold = int(filtered['actual_worth'].sum())
average_price_per_unit = int(filtered['actual_worth'].mean())
median_price_per_unit = int(filtered['actual_worth'].median())
average_meter_price = int(filtered['meter_sale_price'].mean())


def format_value(value):
    if value >= 1_000_000:
        return f"{value / 1_000_000:.2f} M"
    elif value >= 1_000:
        return f"{value / 1_000:.2f} K"
    else:
        return f"{value:.0f}"
    
c1, c2, c3, c4, c5 = st.columns(5)

c1.container(border=True).metric(label='Total Price', value=format_value(total_unit_sold), help='Shows the total price of units sold over the selected time period')
c2.container(border=True).metric(label='Units Sold', value=format_value(total_unit_sold_count), help='Displays the count of units sold over the selected time period')
c3.container(border=True).metric(label='Average Price per Unit', value=format_value(average_price_per_unit), help='Shows the average price per unit over the selected time period')
c4.container(border=True).metric(label='Median Price Per Unit', value=format_value(median_price_per_unit), help='Shows the median price per unit over the selected time period')
c5.container(border=True).metric(label='Average Meter Price', value=format_value(average_meter_price), help='Shows the average price per meter over the selected time period')

# @st.cache_data
# def calculate_growth_rate(df, date_column='date'):
#     df = df.sort_values(by=date_column)
#     df['previous_count'] = df['actual_worth'].shift(1)
#     df['growth_rate'] = (df['actual_worth'] - df['previous_count']) / df['previous_count']
#     return df

# growth_df = calculate_growth_rate(filtered)
# latest_growth_rate = growth_df['growth_rate'].iloc[-1]
# c3.container(border=True).metric(label='Transaction Volume Growth Rate', value=f"{latest_growth_rate:.2%}", help='Growth rate of transaction volume over a selected period')

# Raw Data
@st.cache_data
def convert_df(df):
    return df.to_csv().encode("utf-8")

################################################################
# Expanded Data Frame
with st.expander('Show/Hide Data'):
    names = {k:i.replace('_', ' ').title() for k,i in zip(df.columns, df.columns) if i != 'date'}
    column_config = {'date': st.column_config.DateColumn('Date',format="D MMM YYYY")}
    column_config.update(names)
    st.dataframe(filtered.sort_values(by='date', ascending=False).set_index('date'),height=300, column_config=column_config)
    csv = convert_df(filtered)   # Download Button

    st.download_button(
        label="Download as CSV",
        data=csv,
        file_name="data.csv",
        mime="text/csv",
    )

################################################################
#Visuals
@st.cache_data
def group_date(column,df):
    date_summary = df.groupby(column).agg(
        {'actual_worth': ['mean', 'median', 'count', 'sum']}).reset_index()
    if type(column) is list:
        date_summary.columns = ['Date', column[1], 'Average Price', 'Median Price', 'Sold Count', 'Total Sold']
    else:

        date_summary.columns = ['Date', 'Average Price', 'Median Price', 'Sold Count', 'Total Sold']
    return date_summary

################################################################
# Lines
tab1, tab2 = st.tabs(['General', 'Room Details'])
with tab1:
    with st.container(border=True):
        
        date_para = st.radio('Time Period', ['Date','Month', 'Quarter','Year'],horizontal=True, help='Select Time Period')
               
        if date_para == 'Date':
            gr = group_date('date',filtered)
        elif date_para == 'Month':
            gr = group_date('year_month',filtered)
        elif date_para == 'Quarter':
            gr = group_date('year_quarter',filtered)
        else:
            gr = group_date('year',filtered)
            
        col1, col2 , col3 = st.columns(3)
        with col1:
            st.html('<h5><center>Average Price per Unit Over Time</center></h5>')
            fig1 = px.line(data_frame=gr, x='Date', y='Average Price')
            st.plotly_chart(fig1, on_select="rerun")
        with col2:    
            st.html('<h5><center>Units Sold Over Time</center></h5>')
            fig2 = px.line(data_frame=gr, x='Date', y='Sold Count')
            st.plotly_chart(fig2, on_select="rerun")
        with col3:
            st.html('<h5><center>Total Price Over Time</center></h5>')
            fig3 = px.line(data_frame=gr, x='Date', y='Total Sold')
            st.plotly_chart(fig3, on_select="rerun")

with tab2:
    with st.container(border=True):
        date_para = st.radio('Time Period ', ['Date','Month', 'Quarter','Year'],horizontal=True, help='Select Time Period')
                
        if date_para == 'Date':
            q = group_date(['date', 'rooms'], bx)
        elif date_para == 'Month':
            q = group_date(['year_month', 'rooms'], bx)
        elif date_para == 'Quarter':
            q = group_date(['year_quarter', 'rooms'], bx)
        else:
            q = group_date(['year', 'rooms'], bx)
        
            
        col1, col2 , col3 = st.columns(3)
        with col1:
            st.html('<h5><center>Averge Price Per Unit</center></h5>')
            fig1 = px.line(data_frame=q ,x='Date', y='Average Price', color='rooms')
            st.plotly_chart(fig1, on_select="rerun")
        with col2:    
            st.html('<h5><center>Unit Sold</center></h5>')
            fig2 = px.line(data_frame=q ,x='Date', y='Sold Count', color='rooms')
            st.plotly_chart(fig2, on_select="rerun")
        with col3:
            st.html('<h5><center>Total Price</center></h5>')
            fig3 = px.line(data_frame=q, x='Date', y='Total Sold',  color='rooms')
            st.plotly_chart(fig3, on_select="rerun")



################################################################     
# Bar
@st.cache_data
def gro(column, df):
    z = df.groupby(column).agg(
        {'actual_worth': ['sum', 'mean', 'count']}
    ).reset_index()
    z.columns = [column, 'total_price', 'average_price', 'transaction_count']
    return z

with st.container(border=True):
    r = st.radio('Parameter', ['Total', 'Count'], horizontal=True)
    if r == 'Count':
        left, right = st.columns(2)
        dw = gro('day_of_week_name', filtered)
        mn = gro('month_name', filtered)
        fig1 =px.bar(x=dw.day_of_week_name , y=dw.transaction_count)
        fig1.update_layout(title='Transactions by Day of Week')
        fig2 =px.bar(x=mn.month_name , y=mn.transaction_count)
        fig2.update_layout(title='Transactions by Month')
        left.plotly_chart(fig1, on_select="rerun")
        right.plotly_chart(fig2, on_select="rerun")
    else:
        left, right = st.columns(2)
        dw = gro('day_of_week_name', filtered)
        mn = gro('month_name', filtered)
        fig1 =px.bar(x=dw.day_of_week_name , y=dw.total_price)
        fig1.update_layout(title='Transactions by Day of Week')
        fig2 =px.bar(x=mn.month_name , y=mn.total_price)
        fig2.update_layout(title='Transactions by Month')
        left.plotly_chart(fig1, on_select="rerun")
        right.plotly_chart(fig2, on_select="rerun")
        

################################################################
# Data Frame & Pie
@st.cache_data()    
def group_column(column, df):
    g = df.groupby(column)['actual_worth'].mean().reset_index()
    g['actual_worth'] = g['actual_worth'].apply(lambda x: '{:,}'.format(int(x)))
    t = g.T
    t.columns = g.rooms
    return t.iloc[1:,:]

@st.cache_data
def group_sum(column, df):
    sm = df.groupby(column)['actual_worth'].sum().reset_index()
    sm = sm.sort_values(by='actual_worth', ascending=False)
    return sm.head(5)

@st.cache_data
def count_value(column, df):
    cn = df[column].value_counts()
    return cn.reset_index().head(5)

with st.container(border=True):
    st.html('<center><b>Averge Price Per Unit for Rooms with Applied Filters</b></center>')
    rooms = group_column('rooms',df)
    st.dataframe(rooms,hide_index=True,)
    
    para = st.radio('Parameter', ['Total ', 'Count'], horizontal=True)
    
    if para == 'Total ':
        left, right = st.columns(2)
        
        rm = group_sum('rooms', df)
        tr = group_sum('property_sub_type', df)
        
        
        
        fig1 = go.Figure(data=[go.Pie(labels=rm['rooms'], values=rm['actual_worth'])])
        fig1.update_traces(hoverinfo='percent', textinfo='label', textfont_size=20,
                        marker=dict(line=dict(color='#000000', width=2)))
        
        fig2 = go.Figure(data=[go.Pie(labels=tr['property_sub_type'], values=tr['actual_worth'])],)
        fig2.update_traces(hoverinfo='percent', textinfo='label', textfont_size=20,
                        marker=dict(line=dict(color='#000000', width=2)))
        
        with left:
            with st.container(border=True):
                st.html('<b><center>Units Sold by Number of Rooms</center></b>')
                st.plotly_chart(fig1, on_select="rerun")
        with right:
            with st.container(border=True):
                st.html('<b><center>Units Sold by Property Type</center></b>')
                st.plotly_chart(fig2, on_select="rerun")
        
    else:
        left, right = st.columns(2)
        rm = count_value('rooms', df)
        tr = count_value('property_sub_type', df)
            
        fig1 = go.Figure(data=[go.Pie(labels=rm['rooms'], values=rm['count'])])
        fig1.update_traces(hoverinfo='percent', textinfo='label', textfont_size=20,
                        marker=dict(line=dict(color='#000000', width=2)))
        fig1.update_layout(title='Number of  Unit Sold by Number of Room')
        
        fig2 = go.Figure(data=[go.Pie(labels=tr['property_sub_type'], values=tr['count'])],)
        fig2.update_traces(hoverinfo='percent', textinfo='label', textfont_size=20,
                        marker=dict(line=dict(color='#000000', width=2)))
        fig2.update_layout(title='Number of  Unit Sold by Type')
        
        right.container(border=True).plotly_chart(fig2, on_select="rerun")
        left.container(border=True).plotly_chart(fig1, on_select="rerun")
        

################################################################        
# Boxplot
@st.cache_data
def remove_outliers(df, column):
    q1 = df[column].quantile(0.25)
    q3 = df[column].quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    return df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]

with st.container(border=True):
    select = st.radio('Outliers', ['With Outliers', 'Without Outliers'], horizontal=True, help='fdfdf')
    
    if select == 'Without Outliers':
        df_no_outliers = bx.groupby('rooms').apply(lambda group: remove_outliers(group, 'actual_worth')).reset_index(drop=True)
        fig = px.box(df_no_outliers, x="rooms", y="actual_worth")
    else:
        fig = px.box(bx, x="rooms", y="actual_worth")
    
    st.plotly_chart(fig, on_select="rerun")


################################################################
# Histogram
fig = px.histogram(hs[hs['actual_worth'] <= 15000_000], x='actual_worth', color='trans_group', nbins=100)
fig.update_layout( title='Price Distribution by Transaction Group')
st.container(border=True).plotly_chart(fig, on_select="rerun")
   
################################################################
# Heat Map
# from folium.plugins import HeatMap
# with st.container(border=True, height=450):
#     data = pd.read_parquet('./data/test/test_geo.parquet')
#     m = folium.Map(location=[25.2048,  55.2708], zoom_start=10)
#     HeatMap(data.coordinates).add_to(m)

#     st.html('<h5><center>Transaction Heatmap</center></h5>')
#     st_folium(m,use_container_width=True)
    
################################################################
# Bubble Chart
with st.container(border=True):
    fig = px.scatter(bx, x='procedure_area', y='actual_worth', color='rooms', size='actual_worth',
                    hover_name='area_name',
                    labels={'procedure_area': 'Area Size (sqm)', 'actual_worth': 'Price (AED)', 'rooms': 'Number of Rooms'})

    st.html('<h5><center>Impact of Property Features on Price</center></h5>')
    st.plotly_chart(fig, on_select='rerun')

################################################################