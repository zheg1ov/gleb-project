# api_reader.py - АЛЬТЕРНАТИВНЫЙ ВАРИАНТ
import requests
import pandas as pd
from datetime import datetime

def fetch_crypto_data_alternative():
    """
    Альтернативные API для получения данных о криптовалютах
    """
    alternatives = [
        {
            'name': 'CoinGecko',
            'url': 'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd,eur,rub&include_24hr_change=true'
        },
        {
            'name': 'Binance', 
            'url': 'https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT'
        },
        {
            'name': 'Kraken',
            'url': 'https://api.kraken.com/0/public/Ticker?pair=XBTUSD'
        }
    ]
    
    for api in alternatives:
        try:
            print(f"Пробую загрузить {api['name']} API")
            response = requests.get(api['url'], timeout=10)
            response.raise_for_status()
            data = response.json()
            print(f"{api['name']} позволяет всё грузить, так что всё круто")
            return data, api['name']
        except Exception as e:
            print(f" {api['name']}: {e}")
            continue
    
    return None, None

def create_dataframe(data, api_name):
    # Создание датасета в зависимости от данных
    if api_name == 'CoinGecko':
        df_data = [{
            'cryptocurrency': 'Bitcoin',
            'price_usd': data['bitcoin']['usd'],
            'price_eur': data['bitcoin']['eur'],
            'price_rub': data['bitcoin']['rub'],
            'change_24h': data['bitcoin']['usd_24h_change'],
            'source': 'CoinGecko',
            'timestamp': datetime.now()
        }]
    
    elif api_name == 'Binance':
        df_data = [{
            'symbol': data['symbol'],
            'price': float(data['price']),
            'source': 'Binance', 
            'timestamp': datetime.now()
        }]
    
    elif api_name == 'Kraken':
        price = list(data['result'].values())[0]['c'][0]
        df_data = [{
            'pair': 'XBTUSD',
            'price': float(price),
            'source': 'Kraken',
            'timestamp': datetime.now()
        }]
    
    else:
        return None
    
    return pd.DataFrame(df_data)

def main():
    print("Загружаю данные о крипте")
    print("-" * 50)
    
    data, api_name = fetch_crypto_data_alternative()
    
    if data and api_name:
        df = create_dataframe(data, api_name)
        
        print(f"\nСупер, данные успешно загружены из {api_name}")
        print(f"Данные:\n{df.to_string(index=False)}")
        
    else:
        print("Не получилось загрузить данные ни из одного API, походу че-то не работает :( ")

if __name__ == "__main__":
    main()