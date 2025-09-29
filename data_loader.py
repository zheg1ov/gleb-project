import pandas as pd
import numpy as np

raw_data = pd.read_csv(f"https://drive.google.com/uc?id={'1HXu3s_EKOPQ2Yk_FeNyw8PsIu3mWr8Te'}")

### Функции для перобразования str в float
def clean_features (x):
    try:
        return float(x)
    except ValueError:
        return np.nan

def clean_y(x):
    if x == '#NUM!':
        return np.nan
    try:
        return float(x)
    except:
        return np.nan
    
### Применение функций методом бродкаста для экономии времени
    
raw_data['ammonia'] = np.vectorize(clean_features)(raw_data['ammonia'])
raw_data['is_safe'] = np.vectorize(clean_y)(raw_data['is_safe'])

### Преобразование целевой переменной в категориальную переменную
raw_data['is_safe'] = raw_data['is_safe'].astype('category')

### Конвертация значений фичей в удобный вид. Приведённый к нужным типам данных датасет называется data
data = raw_data.convert_dtypes()

print(data.head(10))