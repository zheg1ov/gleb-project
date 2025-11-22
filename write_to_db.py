import sqlite3
import pandas as pd
from sqlalchemy import create_engine
from data_loader import prepare_dataframe
from dotenv import dotenv_values
CONFIG = dotenv_values('.env')

# конфигурация для базы данных
HOST = CONFIG['HOST']
PORT = CONFIG['PORT']
USER = CONFIG['USER']
PASSWORD = CONFIG['PASSWORD']
DATABASE = CONFIG['DATABASE']

def load_dataset(file_url):
    df = pd.read_csv(file_url)
    return df.head(100)

def write_file():
    TABLE_NAME = 'zhizhimov'  
    FILE_ID = '1HXu3s_EKOPQ2Yk_FeNyw8PsIu3mWr8Te'
    FILE_URL = f'https://drive.google.com/uc?id={FILE_ID}'

    df_row = load_dataset(FILE_URL) # чтение данных
    data = prepare_dataframe(df_row) # подготовка данных для загрузки

    conn_string = f'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}'
    engine = create_engine(conn_string)
    
    data.to_sql(
        TABLE_NAME, 
        engine, 
        schema='public',
        if_exists='replace',
        index=False
    )
    
    print(f'Записано {len(data)} строк')

if __name__ == '__main__':
    write_file()