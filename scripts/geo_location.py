from dotenv import load_dotenv
import os
import googlemaps
import pandas as pd
from write_log import log

def get_geo(location):
    load_dotenv()
    gmap_api = os.getenv('GMAP_API')
    gmaps = googlemaps.Client(key=gmap_api)
    geocode_result = gmaps.geocode(location)
    lat = geocode_result[0]['geometry']['location']['lat']
    lng = geocode_result[0]['geometry']['location']['lng']
    geo = [lat,lng]
    return geo

def geo_processing():
    try:
        print('Geo Data Job Started')
        log('Geo Data Job Started')
        df = pd.read_parquet('./data/half cooked/transactions.parquet')
        print('Data Readed Sucessfully')
        log('Data Readed Sucessfully')
        
        address = pd.DataFrame(df.address.unique(), columns=['address'])
        
        address['coordinates'] = address['address'].apply(get_geo)
        print('Geo Data Collected Sucessfully')
        log('Geo Data Collected Sucessfully')
        
        address['lat'] = address.coordinates.apply(lambda x: x[0])
        address['lng'] = address.coordinates.apply(lambda x: x[1])
        

        address.to_parquet('./data/half cooked/coordinates.parquet')
        print('Geo Data Job Ended')
        log('Geo Data Job Ended')
    except Exception as e:
        print(f'Error: {e}')
        log(f'Geo Data Job Error: {e}')


# geo_processing()