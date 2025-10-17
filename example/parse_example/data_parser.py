import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

def parse_hourly_weather():
    # Функция для парсинга погоды по часам с сайта world-weather.ru для спб

    url = "https://world-weather.ru/pogoda/russia/saint_petersburg/24hours/"
    
    try:
        # Заголовки для имитации реального браузера
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Отправляю запрос к сайту
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Проверяем успешность запроса
        
        # Создаю объект BeautifulSoup для парсинга HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Получаю текущую дату в формате сайта, чтобы вывод имел хоть какой-то смысл
        today = datetime.now()
        current_date = today.strftime("%Y-%m-%d")
        
        # Ищу таблицу с почасовым прогнозом
        weather_data = []
        
        # Нахожу все строки таблицы
        rows = soup.find_all('tr')[1:]  # Пропускаю заголовок таблицы
        
        for row in rows:
            try:
                cells = row.find_all('td')
                if len(cells) >= 6:  # Проверяю, что строка содержит достаточно данных
                    time_cell = cells[0].get_text(strip=True)
                    temp_cell = cells[1].get_text(strip=True)
                    feels_like_cell = cells[2].get_text(strip=True)
                    precipitation_cell = cells[3].get_text(strip=True)
                    pressure_cell = cells[4].get_text(strip=True)
                    wind_cell = cells[5].get_text(strip=True)
                    humidity_cell = cells[6].get_text(strip=True)
                    
                    # Добавляю данные в список
                    weather_data.append({
                        'Время': time_cell,
                        'Температура': temp_cell,
                        'Ощущается': feels_like_cell,
                        'Вероятность осадков': precipitation_cell,
                        'Давление': pressure_cell,
                        'Ветер': wind_cell,
                        'Влажность': humidity_cell
                    })
            except Exception as e:
                print(f"Ошибка при парсинге строки: {e}")
                continue
        
        return weather_data
        
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при загрузке страницы, что-то не так: {e}")
        return None

def main():
    print("Погода сегодня в питере ээ ща секунду")
    print("=" * 70)
    
    # Собственно парщю (парсю) данные
    weather_data = parse_hourly_weather()
    
    if weather_data:
        # Создаю DataFrame и показываю его
        df = pd.DataFrame(weather_data)
        
        print(f"Актуально на момент {datetime.now().strftime('%d.%m.%Y')}")
        print("\n" + "=" * 70)
        
        # Выводим DataFrame
        print(df.to_string(index=False))
        
        
    else:
        print("Не получилось получить данные о погоде, прощу прощения")

if __name__ == "__main__":
    main()