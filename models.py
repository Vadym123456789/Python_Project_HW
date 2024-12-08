from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Підключення до бази даних
engine = create_engine(f'sqlite:///database_project2/database_Project2.db')
Base = declarative_base()

class Item(Base):
    __tablename__ = 'Item'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255))  # Додали опис
    price_hour = Column(Integer)      # Додали ціну за годину
    price_day = Column(Integer)       # Додали ціну за день
    price_week = Column(Integer)      # Додали ціну за тиждень
    price_month = Column(Integer)     # Додали ціну за місяць
    # Додай інші поля таблиці Item, якщо вони є

class User(Base):  # Додали модель User
    __tablename__ = 'User'
    id = Column(Integer, primary_key=True)
    login = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    full_name = Column(String(255))
    contacts = Column(String(255))
    ipn = Column(String(255))

# Створення таблиць у базі даних (якщо їх ще немає)
Base.metadata.create_all(engine)

# Створення сесії для роботи з базою даних
Session = sessionmaker(bind=engine)