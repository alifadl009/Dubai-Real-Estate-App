import requests
import pandas as pd
from scripts.write_log import log

def get_data(start_date, end_date):
    url = "https://archive-api.open-meteo.com/v1/era5"
    params = {
        'latitude': 25.276987,  # Dubai latitude
        'longitude': 55.296249,  # Dubai longitude
        'start_date': start_date.strftime('%Y-%m-%d'),
        'end_date': end_date.strftime('%Y-%m-%d'),
        'daily': 'temperature_2m_max,temperature_2m_min',
        'timezone': 'Asia/Dubai'
    }
    response = requests.get(url, params=params)
    data = response.json()
    df = pd.DataFrame(data['daily'])
    df.rename(columns={'temperature_2m_max': 'max_temperature', 'temperature_2m_min': 'min_temperature'}, inplace=True)  
    return df

def get_weather(start_date, end_date):
    log('downloading transaction data')    
    
    df = pd.read_parquet('./data/transaction_processed.csv')
    try:
        start_date = df.date.min()
        end_date = df.date.max()

        weather_df = get_data(start_date, end_date)
        weather_df['date'] = pd.to_datetime(weather_df['time'])
        weather_df.drop('time', axis=1, inplace=True)
        weather_df.to_parquet('./data/weather.parquet', index=False)
        log('weather data downloaded')    

    except Exception as e:
        print(f"An error occurred: {e}")
        log(f'Filed to downloaded, {e}') 
        try:
            end_date = end_date - pd.Timedelta(days=1)
            weather_df = get_data(start_date, end_date)
            weather_df['date'] = pd.to_datetime(weather_df['time'])
            weather_df.drop('time', axis=1, inplace=True)
            weather_df.to_csv('./data/weather.csv', index=False)
            print("Weather data saved successfully with adjusted end date.")
            log('weather data downloaded')    

        except Exception as inner_e:
            print(f"An additional error occurred when adjusting the end date: {inner_e}")
            log(f'Filed to downloaded {inner_e}')    




    
    