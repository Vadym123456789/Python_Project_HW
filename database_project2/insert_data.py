import sqlite3
# Підключення до бази даних
def connect_to_database():
    db_path = r'C:\Users\vgumenyuk1\Documents\Python projects\pythonProject 2\database_project2\database_Project2.db'
    try:
        connection = sqlite3.connect(db_path)
        print("Підключення до бази даних встановлено")
        return connection
    except sqlite3.Error as e:
        print(f"Помилка підключення до бази даних: {e}")
        return None
# Функція для додавання даних до таблиці User
def insert_user_data(connection):
    cursor = connection.cursor()
    # Перевірка, чи існує вже запис із таким IPN
    check_query = 'SELECT * FROM User WHERE ipn = ?'
    user_data = ('john_doe', 'password123', '1234567890', 'John Doe', 'john.doe@example.com', None)
    cursor.execute(check_query, (user_data[2],))  # IPN знаходиться в третьому елементі
    existing_record = cursor.fetchone()
    if existing_record:
        print(f"Запис із IPN {user_data[2]} вже існує.")
    else:
        insert_user_query = '''
        INSERT INTO User (login, password, ipn, full_name, contacts, photo)
        VALUES (?, ?, ?, ?, ?, ?);
        '''
        cursor.execute(insert_user_query, user_data)
        connection.commit()
        print("Дані успішно додані у таблицю User")
# Функція для додавання даних до таблиці Item
def insert_item_data(connection):
    cursor = connection.cursor()
    insert_item_query = '''
    INSERT INTO Item (photo, name, description, price_hour, price_day, price_week, price_month)
    VALUES (?, ?, ?, ?, ?, ?, ?);
    '''
    item_data = (None, 'Camera', 'High-quality digital camera', 5.0, 30.0, 150.0, 500.0)
    # Виконання запиту
    cursor.execute(insert_item_query, item_data)
    connection.commit()
    print("Дані успішно додані у таблицю Item")
# Основна функція для виконання додавання даних
def main():
    connection = connect_to_database()
    if connection:
        insert_user_data(connection)
        insert_item_data(connection)
        # Можна додати виклики інших функцій для інших таблиць тут
        connection.close()
        print("Підключення до бази даних закрито")
if __name__ == "__main__":
    main()







