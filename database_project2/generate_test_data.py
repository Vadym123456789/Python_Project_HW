import sqlite3
import random
from werkzeug.security import generate_password_hash
import os

# Визначення шляху до бази даних
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = r'C:\Users\vgumenyuk1\Documents\Python projects\pythonProject 2\database_project2\database_Project2.db'

# Перевірка наявності файлу бази даних та створення, якщо потрібно
if not os.path.exists(DATABASE):
    try:
        os.makedirs(os.path.dirname(DATABASE), exist_ok=True)
        open(DATABASE, 'w').close()
        print(f"Файл бази даних створено: {DATABASE}")
    except OSError as e:
        print(f"Помилка при створенні файлу бази даних: {e}")
        exit(1)

# Підключення до бази даних
conn = sqlite3.connect(DATABASE)
cursor = conn.cursor()

# Створення таблиць, якщо вони не існують
cursor.execute('''
    CREATE TABLE IF NOT EXISTS User (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        login VARCHAR(255) NOT NULL UNIQUE,
        password VARCHAR(255) NOT NULL,
        full_name VARCHAR(255),
        contacts VARCHAR(255),
        photo BLOB
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Item (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        photo BLOB,
        name VARCHAR(255) NOT NULL,
        description TEXT,
        price_hour REAL,
        price_day REAL,
        price_week REAL,
        price_month REAL
    )
''')


cursor.execute('''
    CREATE TABLE IF NOT EXISTS Contract (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Text TEXT,
        start_date DATE,
        end_date DATE,
        Contract_num INTEGER,
        Leaser INTEGER,
        Taker INTEGER,
        Item INTEGER,
        FOREIGN KEY (Leaser) REFERENCES User(id),
        FOREIGN KEY (Taker) REFERENCES User(id),
        FOREIGN KEY (Item) REFERENCES Item(id)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        author INTEGER,
        user INTEGER,
        text TEXT,
        Grade INTEGER,
        Contract INTEGER,
        FOREIGN KEY (author) REFERENCES User(id),
        FOREIGN KEY (user) REFERENCES User(id),
        FOREIGN KEY (Contract) REFERENCES Contract(id)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Search_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user INTEGER,
        Search_text TEXT,
        timestamp DATETIME,
        FOREIGN KEY (user) REFERENCES User(id)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Favorites (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user INTEGER,
        Item INTEGER,
        FOREIGN KEY (user) REFERENCES User(id),
        FOREIGN KEY (Item) REFERENCES Item(id)
    )
''')

conn.commit()

# Очищення таблиці User перед додаванням нових користувачів
cursor.execute("DELETE FROM User;")
conn.commit()

# Генерація тестових даних для користувачів
logins = [f'user{i}' for i in range(1, 11)]
passwords = [generate_password_hash(str(random.randint(10000000, 99999999))) for _ in range(10)]
full_names = [f'User {i}' for i in range(1, 11)]
contacts = [f'user{i}@example.com' for i in range(1, 11)]

# Генерація тестових даних для товарів
item_names = [f'item{i}' for i in range(1, 21)]
descriptions = [f'Description for item {i}' for i in range(1, 21)]
prices_hour = [round(random.uniform(10, 100), 2) for _ in range(20)]
prices_day = [round(random.uniform(50, 200), 2) for _ in range(20)]
prices_week = [round(random.uniform(200, 700), 2) for _ in range(20)]
prices_month = [round(random.uniform(800, 3000), 2) for _ in range(20)]

# Додавання користувачів
for i in range(10):
    cursor.execute(
        "INSERT INTO User (login, password, full_name, contacts) VALUES (?, ?, ?, ?)",
        (logins[i], passwords[i], full_names[i], contacts[i])
    )

# Додавання товарів
for i in range(20):
    cursor.execute(
        "INSERT INTO Item (name, description, price_hour, price_day, price_week, price_month) VALUES (?, ?, ?, ?, ?, ?)",
        (item_names[i], descriptions[i], prices_hour[i], prices_day[i], prices_week[i], prices_month[i])
    )

# Збереження змін та закриття з'єднання
conn.commit()
conn.close()

print("База даних успішно заповнена тестовими даними!")