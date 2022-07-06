from sqlalchemy import Column, Float, ForeignKey, String, Integer, Date
from sqlalchemy.orm import relationship
from .base import Base
from sqlalchemy.types import BigInteger


class Users(Base):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True,
                autoincrement=True, nullable=True)
    name = Column(String)
    user_id = Column(BigInteger)
    bank_balance = Column(Float)
    transactions = relationship(
        "Transaction", back_populates="user", uselist=False, cascade="all")
    categories = relationship(
        "Categories", back_populates="user", uselist=False, cascade="all")

    def __init__(self, name, user_id, bank_balance, categories):
        self.name = name
        self.user_id = user_id
        self.bank_balance = bank_balance
        self.categories = categories


class Transaction(Base):
    __tablename__ = 'budget'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.user_id"))
    amount = Column(Float)
    note = Column(String)
    date = Column(Date)
    user = relationship("Users", back_populates="transactions",
                        uselist=False, cascade="all")
    category = relationship(
        "Categories", back_populates="transaction", uselist=False)
    categories = Column(String, ForeignKey("categories.name"))

    def __init__(self, amount, note, date, user_id, categories) -> None:
        self.amount = amount
        self.note = note
        self.date = date
        self.user_id = user_id
        self.categories = categories


class Categories(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    user_id = Column(BigInteger, ForeignKey("users.user_id"))
    transaction = relationship(
        "Transaction", back_populates="category", uselist=False)
    user = relationship("Users", back_populates="categories",
                        uselist=False, cascade="all")

    def __init__(self, name, user_id):
        self.name = name
        self.user_id = user_id
