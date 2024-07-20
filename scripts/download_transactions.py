import wget
import pandas as pd
import os
from write_log import log

def download_data():
    try:
        URL = 'https://www.dubaipulse.gov.ae/dataset/3b25a6f5-9077-49d7-8a1e-bc6d5dea88fd/resource/a37511b0-ea36-485d-bccd-2d6cb24507e7/download/transactions.csv'
        file_path = './data/raw/transactions.csv'
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        if os.path.exists(file_path):
            os.remove(file_path)
            log('Existing file removed')
            print('Existing file removed')
        
        file = wget.download(URL, out=file_path)
        log('File downloaded successfully')
        print(f'{file}\ndownloaded successfully')
        
    except Exception as e:
        print(f'Failed to download:\n{e}')
        log(f'Error downloading file: {e}')

def to_parquet():
    df = pd.read_csv('./data/raw/transactions.csv')
    df.to_parquet('./data/raw/transactions.parquet')
    os.remove('./data/raw/transactions.csv')
    

download_data()
to_parquet()