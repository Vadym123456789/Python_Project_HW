import sqlite3
import os


# Підключення до бази даних (шлях до файлу бази даних)
def connect_to_database(db_path):
    try:
        connection = sqlite3.connect(db_path)
        print("Підключення до бази даних встановлено")
        return connection
    except sqlite3.Error as e:
        print(f"Помилка підключення до бази даних: {e}")
        return None


# Створення таблиць у базі даних
def create_tables(cursor):
    create_tables_queries = [
        '''
        CREATE TABLE IF NOT EXISTS User (
            login TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            ipn TEXT UNIQUE,
            full_name TEXT,
            contacts TEXT,
            photo BLOB
        );
        ''',
        '''
        CREATE TABLE IF NOT EXISTS Item (
            item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            photo BLOB,
            name TEXT NOT NULL,
            description TEXT,
            price_hour REAL,
            price_day REAL,
            price_week REAL,
            price_month REAL
        );
        ''',
        '''
        CREATE TABLE IF NOT EXISTS Contract (
            contract_num INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT,
            start_date DATE,
            end_date DATE,
            leaser TEXT,
            taker TEXT,
            item_id INTEGER,
            FOREIGN KEY (leaser) REFERENCES User(login),
            FOREIGN KEY (taker) REFERENCES User(login),
            FOREIGN KEY (item_id) REFERENCES Item(item_id)
        );
        ''',
        '''
        CREATE TABLE IF NOT EXISTS Feedback (
            feedback_id INTEGER PRIMARY KEY AUTOINCREMENT,
            author TEXT,
            user TEXT,
            text TEXT,
            grade INTEGER CHECK (grade BETWEEN 1 AND 5),
            contract_num INTEGER,
            FOREIGN KEY (author) REFERENCES User(login),
            FOREIGN KEY (user) REFERENCES User(login),
            FOREIGN KEY (contract_num) REFERENCES Contract(contract_num)
        );
        ''',
        '''
        CREATE TABLE IF NOT EXISTS SearchHistory (
            search_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT,
            search_text TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user) REFERENCES User(login)
        );
        ''',
        '''
        CREATE TABLE IF NOT EXISTS Favorites (
            favorite_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT,
            item_id INTEGER,
            FOREIGN KEY (user) REFERENCES User(login),
            FOREIGN KEY (item_id) REFERENCES Item(item_id)
        );
        '''
    ]

    for query in create_tables_queries:
        cursor.execute(query)
    print("Таблиці успішно створені")


# Основна функція для підключення до бази даних і створення таблиць
def main():
    db_path = r'C:\Users\vgumenyuk1\Documents\Python projects\pythonProject 2\database_project2\database_Project2.db'
    connection = connect_to_database(db_path)

    if connection:
        cursor = connection.cursor()
        create_tables(cursor)
        connection.commit()
        connection.close()
        print("Підключення до бази даних закрито")


if __name__ == "__main__":
    main()
