import time
import pandas as pd
from sqlalchemy import create_engine

DB_USER = "my_user"
DB_PASSWORD = "my_password"
DB_HOST = "127.0.0.1"
DB_PORT = "3306"
DB_NAME = "my_database"

DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


def get_engine_with_retry(max_retries=10, delay_seconds=10):

    for attempt in range(1, max_retries + 1):
        try:
            print(f"Спроба підключення до MySQL ({attempt}/{max_retries})...")
            engine = create_engine(DATABASE_URL)
            with engine.connect() as conn:
                print("Успішно підключено до бази даних!")
                return engine
        except Exception as e:
            print(f"База ще не готова. Очікуємо {delay_seconds} секунд...")
            time.sleep(delay_seconds)

    raise ConnectionError("Не вдалося підключитись до бази даних після всіх спроб.")


def main():
    try:
        engine = get_engine_with_retry()

        query = "SELECT * FROM titanic;"
        df = pd.read_sql(query, engine)

        print("\n--- Результат завантаження ---")
        print(f"Розмір DataFrame: {df.shape} (Рядки, Колонки)")
        print("Перші 5 рядків:")
        print(df.head())

        print("\nКількість пропущених (NULL) значень по колонках:")
        print(df[['Age', 'Cabin', 'Embarked']].isna().sum())

    except Exception as e:
        print("\nВиникла критична помилка під час роботи скрипта:")
        print(e)


if __name__ == "__main__":
    main()