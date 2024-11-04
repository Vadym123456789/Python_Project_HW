import sqlite3

# Підключення до бази даних
db_path = r'C:\Users\vgumenyuk1\Documents\Python projects\pythonProject 2\database_project2\database_Project2.db'
connection = sqlite3.connect(db_path)
cursor = connection.cursor()

# SQL-запит для вибірки даних
select_query = 'SELECT * FROM User;'

# Виконання запиту та отримання результатів
cursor.execute(select_query)
rows = cursor.fetchall()

# Виведення результатів
for row in rows:
    print(row)

# Закриття підключення
connection.close()
