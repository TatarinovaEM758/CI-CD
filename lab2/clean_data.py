import pandas as pd
import numpy as np
from faker import Faker
import random

# Инициализация Faker
fake = Faker('ru_RU')  # русские данные

def generate_dirty_real_estate_data(n=100):
    """Генерация 'грязных' данных о недвижимости с пропусками"""
    
    data = {
        'district': [],
        'area_sqm': [],
        'price_rub': [],
        'floor': [],
        'year_built': [],
        'material_type': []
    }
    
    materials = ['кирпич', 'монолит', 'панель', 'дерево', None]
    districts = ['Центральный', 'Северный', 'Южный', 'Западный', 'Восточный']
    
    for i in range(n):
        # Генерируем данные с вероятностью пропусков 10-15%
        data['district'].append(random.choice(districts) if random.random() > 0.1 else None)
        data['area_sqm'].append(round(random.uniform(20, 150), 1) if random.random() > 0.12 else None)
        data['price_rub'].append(random.randint(2_000_000, 50_000_000) if random.random() > 0.1 else None)
        data['floor'].append(random.randint(1, 25) if random.random() > 0.15 else None)
        data['year_built'].append(random.randint(1950, 2025) if random.random() > 0.08 else None)
        data['material_type'].append(random.choice(materials))
    
    return pd.DataFrame(data)

def clean_data(df):
    """Очистка данных: обработка пропусков"""
    
    print("=" * 60)
    print("Исходная информация о данных:")
    print("=" * 60)
    print(f"Всего записей: {len(df)}")
    print(f"Количество пропусков до очистки:\n{df.isnull().sum()}")
    
    # Вариант 1: Заполняем пропуски (fillna)
    df_cleaned = df.copy()
    
    # Заполняем числовые пропуски медианой
    df_cleaned['area_sqm'] = df_cleaned['area_sqm'].fillna(df_cleaned['area_sqm'].median())
    df_cleaned['price_rub'] = df_cleaned['price_rub'].fillna(df_cleaned['price_rub'].median())
    df_cleaned['floor'] = df_cleaned['floor'].fillna(df_cleaned['floor'].median())
    df_cleaned['year_built'] = df_cleaned['year_built'].fillna(df_cleaned['year_built'].median())
    
    # Заполняем категориальные пропуски модой
    df_cleaned['district'] = df_cleaned['district'].fillna(df_cleaned['district'].mode()[0] if not df_cleaned['district'].mode().empty else 'Неизвестно')
    df_cleaned['material_type'] = df_cleaned['material_type'].fillna('не указан')
    
    print("\n" + "=" * 60)
    print("Количество пропусков ПОСЛЕ очистки:")
    print("=" * 60)
    print(df_cleaned.isnull().sum())
    
    return df_cleaned

def calculate_metrics(df):
    """Расчет метрик по очищенным данным"""
    
    # Добавляем расчет цены за квадратный метр
    df['price_per_sqm'] = df['price_rub'] / df['area_sqm']
    
    print("\n" + "=" * 60)
    print("АНАЛИТИКА ПО НЕДВИЖИМОСТИ:")
    print("=" * 60)
    
    # Статистика по районам
    district_stats = df.groupby('district').agg({
        'price_per_sqm': ['mean', 'median', 'min', 'max'],
        'area_sqm': 'mean',
        'price_rub': 'mean'
    }).round(2)
    
    print("\nСтатистика по районам (цена за м²):")
    print(district_stats)
    
    # Общая статистика
    print(f"\nОбщая статистика:")
    print(f"  Средняя цена квартиры: {df['price_rub'].mean():,.0f} руб.")
    print(f"  Медианная цена: {df['price_rub'].median():,.0f} руб.")
    print(f"  Средняя площадь: {df['area_sqm'].mean():.1f} м²")
    print(f"  Средняя цена за м²: {df['price_per_sqm'].mean():.0f} руб./м²")
    
    # Статистика по материалам
    print(f"\nСтатистика по типу материала:")
    material_stats = df.groupby('material_type')['price_per_sqm'].mean().round(0)
    for mat, price in material_stats.items():
        print(f"  {mat}: {price:,.0f} руб./м²")
    
    return district_stats

def main():
    print("=" * 60)
    print("ГЕНЕРАЦИЯ ДАННЫХ О НЕДВИЖИМОСТИ (с пропусками)")
    print("=" * 60)
    
    # Генерация данных
    df_raw = generate_dirty_real_estate_data(100)
    
    # Очистка данных
    df_cleaned = clean_data(df_raw)
    
    # Расчет метрик
    metrics = calculate_metrics(df_cleaned)
    
    # Сохранение результата в файл
    output_file = "/app/cleaned_data.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("=" * 60 + "\n")
        f.write("ОТЧЕТ ПО ОЧИСТКЕ ДАННЫХ НЕДВИЖИМОСТИ\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Всего обработано записей: {len(df_cleaned)}\n\n")
        f.write("Первые 5 записей после очистки:\n")
        f.write(df_cleaned.head().to_string())
        f.write("\n\nСтатистика по районам:\n")
        f.write(metrics.to_string())
    
    print("\n" + "=" * 60)
    print(f"РЕЗУЛЬТАТ СОХРАНЕН В ФАЙЛ: {output_file}")
    print("=" * 60)
    
    # Выводим содержимое файла в консоль
    print("\n" + "=" * 60)
    print("СОДЕРЖИМОЕ ФАЙЛА С ОТЧЕТОМ:")
    print("=" * 60)
    with open(output_file, 'r', encoding='utf-8') as f:
        print(f.read())

if __name__ == "__main__":
    main()