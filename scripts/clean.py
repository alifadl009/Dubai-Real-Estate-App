import pandas as pd
from write_log import log


def determine_season(date):
    month = date.month
    if 6 <= month <= 8:
        return 'Summer'
    elif 11 <= month <= 3:
        return 'Winter'
    elif 9 <= month <= 10:
        return 'Transition (Summer to Winter)'
    elif 4 <= month <= 5:
        return 'Transition (Winter to Summer)'
    else:
        return 'Unknown'  # Just in case
    
    
def transaction_processing():
    df = pd.read_parquet('./data/raw/transactions.parquet')
    print('read successfully')
    
    df['date'] = pd.to_datetime(df['instance_date'], format='%d-%m-%Y', errors='coerce') 
    df['year'] = df.date.dt.year.apply(lambda x: f'{x:.0f}')
    df['month_name'] = df.date.dt.month
    df['month_name'] = df.date.dt.strftime('%m-%b')
    df['day_of_month'] = df.date.dt.day.apply(lambda x: f'{x:.0f}')
    df['day_of_week_name'] = df.date.dt.strftime('%u-%a')
    df['year_month'] = df.date.dt.strftime('%Y-%m')
    df['quarter'] = df.date.dt.quarter.apply(lambda x: f'{x:.0f}')
    df['year_quarter'] = df['year'] + '-Q' + df['quarter']
    df['season'] = df['date'].apply(determine_season)
    print('date processed successfully')

    max_date = df['date'].max()
    min_date = max_date - pd.DateOffset(years=20)
    filtered_df = df.query('date >= @min_date')
    
    df_en = filtered_df.drop(columns=[i for i in filtered_df.columns if i.endswith('_ar')], axis=1)
    en_columns = [i for i in df_en.columns if i.endswith('_en')]
    renamed = [i.replace('_en','') for i in en_columns]
    rename_dic = {k:v for k, v in zip(en_columns, renamed)}
    df_renamed = df_en.rename(columns=rename_dic)
    print('column renamed successfully')

    columns_to_drop = ['instance_date', 'transaction_id', 'procedure_id', 'trans_group_id',
                        'property_type_id', 'property_sub_type_id', 'reg_type_id', 'area_id',
                        'project_number', 'no_of_parties_role_1','no_of_parties_role_2',
                        'no_of_parties_role_3', 'rent_value', 'meter_rent_price',
                    ]
    data = df_renamed.drop(columns_to_drop, axis=1)
    
    mask = (data['property_type'] == 'Land') & data['property_sub_type'].isna()
    data.loc[mask, 'property_sub_type'] = 'Land'

    mask = (data['property_type'] == 'Building') & data['property_sub_type'].isna()
    data.loc[mask, 'property_sub_type'] = 'Building'

    mask = (data['property_type'] == 'Villa') & data['property_sub_type'].isna()
    data.loc[mask, 'property_sub_type'] = 'Villa'
    data['rooms'] = data.apply(lambda row: row['rooms'] if pd.notnull(row['rooms']) else 
                            'Unknown' if row['property_sub_type'] in ['Villa', 'Flat'] else 
                            row['property_sub_type'], axis=1)
    print('Nulls filled successfully')
            

    
    
    
    final = data.dropna(subset='date')
    print('Nulls dropped successfully')

    final = final.copy()
    final['building_name'] = final['building_name'].fillna('')
    final.loc[:,'address'] = final['area_name'] + ', ' + final['building_name'] + ', Dubai, UAE'
    print('Adress created successfully')
    

    data = data.query('(trans_group in ["Sales", "Mortgages"])')
    print('Data filtered successfully')
    
    final.to_parquet('./data/half cooked/transactions.parquet')
    print('File saved successfully')
    
    print('Endede')

    

    
def join_data():
    transaction = pd.read_parquet('./data/half cooked/transactions.parquet')
    print('Transactions readed')
    coordinates = pd.read_parquet('./data/half cooked/coordinates.parquet')
    print('Coordinates readed')
    
    last = pd.merge(transaction, coordinates, on='address', how='left')
        
    print('Saving ..')
    last.to_parquet('./data/fully cooked/final.parquet')



def clean():
    log('Transform job started')

    log('processing transaction data')
    transaction_processing()
    log('transaction data processed')
    
   
    log('joining data')
    join_data()
    log('data joined')

    log('Transform job Finished')
    
clean()
