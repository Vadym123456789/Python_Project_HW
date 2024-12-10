from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from flask_login import UserMixin

# Підключення до бази даних
engine = create_engine(f'sqlite:///database_project2/database_Project2.db')
Base = declarative_base()


class Item(Base):
    __tablename__ = 'Item'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255))
    price_hour = Column(Integer)
    price_day = Column(Integer)
    price_week = Column(Integer)
    price_month = Column(Integer)

    # Додаємо зв'язок з контрактами
    contracts = relationship("Contract", back_populates="item")


class User(Base, UserMixin):  # Додаємо UserMixin
    __tablename__ = 'User'
    id = Column(Integer, primary_key=True)
    login = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    full_name = Column(String(255))
    contacts = Column(String(255))
    ipn = Column(String(255))

    # Додаємо зв'язок з контрактами
    contracts = relationship("Contract", back_populates="user")

    @property
    def is_active(self):
        return True  # Поки що всі користувачі активні


class Contract(Base):
    __tablename__ = 'Contract'
    id = Column(Integer, primary_key=True)
    item_id = Column(Integer, ForeignKey('Item.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('User.id'), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    price = Column(Integer, nullable=False)

    # Додаємо зв'язки з товаром та користувачем
    item = relationship("Item", back_populates="contracts")
    user = relationship("User", back_populates="contracts")


# Створення таблиць у базі даних (якщо їх ще немає)
Base.metadata.create_all(engine)

# Створення сесії для роботи з базою даних
Session = sessionmaker(bind=engine)