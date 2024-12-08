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
    # Додай інші поля таблиці Item, якщо вони є

# Створення таблиць у базі даних (якщо їх ще немає)
Base.metadata.create_all(engine)

# Створення сесії для роботи з базою даних
Session = sessionmaker(bind=engine)