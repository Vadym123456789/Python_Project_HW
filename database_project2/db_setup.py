import sqlite3
import os
from typing import Optional, List, Dict, Any
import logging

logger = logging.getLogger(__name__)


class DatabaseManager:
    def __init__(self,
                 db_path: str = r'C:\Users\vgumenyuk1\Documents\Python projects\pythonProject 2\database_project2\database_Project2.db'):
        self.db_path = db_path
        self.connection = None
        self.cursor = None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def connect(self) -> None:
        """Встановлює з'єднання з базою даних"""
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row
            self.cursor = self.connection.cursor()
            logger.debug("Database connection established")
        except sqlite3.Error as e:
            logger.error(f"Database connection error: {e}")
            raise

    def close(self) -> None:
        """Закриває з'єднання з базою даних"""
        if self.connection:
            self.connection.close()
            logger.debug("Database connection closed")

    def commit(self) -> None:
        """Зберігає зміни в базі даних"""
        if self.connection:
            self.connection.commit()

    def rollback(self) -> None:
        """Відміняє зміни в базі даних"""
        if self.connection:
            self.connection.rollback()

    # Методи для роботи з користувачами
    def create_user(self, login: str, password: str, ipn: str = None,
                    full_name: str = None, contacts: str = None) -> bool:
        """Створює нового користувача"""
        try:
            self.cursor.execute('''
                INSERT INTO User (login, password, ipn, full_name, contacts)
                VALUES (?, ?, ?, ?, ?)
            ''', (login, password, ipn, full_name, contacts))
            self.commit()
            logger.info(f"User {login} created successfully")
            return True
        except sqlite3.Error as e:
            logger.error(f"Error creating user: {e}")
            self.rollback()
            return False

    def get_user(self, login: str) -> Optional[Dict]:
        """Отримує користувача за логіном"""
        try:
            self.cursor.execute('SELECT * FROM User WHERE login = ?', (login,))
            user = self.cursor.fetchone()
            return dict(user) if user else None
        except sqlite3.Error as e:
            logger.error(f"Error getting user: {e}")
            return None

    # Методи для роботи з товарами
    def get_all_items(self) -> List[Dict]:
        """Отримує всі товари"""
        try:
            self.cursor.execute('SELECT * FROM Item')
            items = self.cursor.fetchall()
            return [dict(item) for item in items]
        except sqlite3.Error as e:
            logger.error(f"Error getting items: {e}")
            return []

    def create_item(self, name: str, description: str = None,
                    price_hour: float = None, price_day: float = None,
                    price_week: float = None, price_month: float = None) -> Optional[int]:
        """Створює новий товар"""
        try:
            self.cursor.execute('''
                INSERT INTO Item (name, description, price_hour, price_day, price_week, price_month)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (name, description, price_hour, price_day, price_week, price_month))
            self.commit()
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            logger.error(f"Error creating item: {e}")
            self.rollback()
            return None

    def get_item_by_id(self, item_id: int) -> Optional[Dict]:
        """Отримує товар за ID"""
        try:
            self.cursor.execute('SELECT * FROM Item WHERE item_id = ?', (item_id,))
            item = self.cursor.fetchone()
            return dict(item) if item else None
        except sqlite3.Error as e:
            logger.error(f"Error getting item: {e}")
            return None

    # Загальні методи для роботи з базою даних
    def execute_query(self, query: str, params: tuple = None) -> Optional[List[Dict]]:
        """Виконує довільний SQL запит"""
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            result = self.cursor.fetchall()
            self.commit()
            return [dict(row) for row in result] if result else None
        except sqlite3.Error as e:
            logger.error(f"Query execution error: {e}")
            self.rollback()
            return None

    def select(self, table: str, columns: List[str] = None,
               where: Dict[str, Any] = None, limit: int = None) -> List[Dict]:
        """Генерує та виконує SELECT запит"""
        try:
            columns_str = "*" if not columns else ", ".join(columns)
            query = f"SELECT {columns_str} FROM {table}"

            params = ()
            if where:
                conditions = []
                for key, value in where.items():
                    conditions.append(f"{key} = ?")
                    params += (value,)
                query += " WHERE " + " AND ".join(conditions)

            if limit:
                query += f" LIMIT {limit}"

            self.cursor.execute(query, params)
            results = self.cursor.fetchall()
            return [dict(row) for row in results]

        except sqlite3.Error as e:
            logger.error(f"Select error: {e}")
            return []