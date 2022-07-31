from datetime import datetime
from enum import unique
from sqlalchemy import DATETIME, Boolean, Column, DateTime, Float, ForeignKey, String, Integer, Date
from sqlalchemy.orm import relationship

from .base import Base
from sqlalchemy.types import BigInteger


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True,
                autoincrement=True)
    name = Column(String)
    user_id = Column(String, unique=True)
    bank_balance = Column(Float)
    first_login = Column(Boolean)
    transactions = relationship(
        "Transaction", back_populates="user", uselist=False, cascade="all")
    categories = relationship(
        "Categories", back_populates="user", uselist=False, cascade="all")

    def __init__(self, name, user_id, bank_balance, categories, first_login):
        self.name = name
        self.user_id = user_id
        self.bank_balance = bank_balance
        self.categories = categories
        self.first_login = first_login


# class Budget(Base):
#    __tablename__ = 'userbudget'
#    id = Column(Integer, primary_key=True, autoincrement=True)
#    user_id = Column(BigInteger, ForeignKey("users.user_id"))
#    categories = Column(String, ForeignKey(
#        "categories.name", onupdate="cascade"))

class Income(Base):
    __tablename__ = 'income'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey(
        "users.user_id", name="fk_user_id"))
    amount = Column(Float)

    def __init__(self, user_id, amount):
        self.user_id = user_id
        self.amount = amount


class Transaction(Base):
    __tablename__ = 'expenses'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey(
        "users.user_id", name="fk_user_id"))
    amount = Column(Float)
    recipient = Column(String)
    note = Column(String)
    date = Column(DateTime)
    user = relationship("Users", back_populates="transactions",
                        uselist=False, cascade="all")
    category = relationship(
        "Categories", back_populates="transaction", uselist=False)
    categories = Column(String, ForeignKey(
        "categories.name", onupdate="cascade"))
    date_added = Column(DateTime, default=datetime.utcnow)

    def __init__(self, amount, recipient, note, date, user_id, categories, date_added) -> None:
        self.amount = amount
        self.recipient = recipient
        self.note = note
        self.date = date
        self.user_id = user_id
        self.categories = categories
        self.date_added = date_added


class Categories(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)
    user_id = Column(String, ForeignKey("users.user_id"))
    transaction = relationship(
        "Transaction", back_populates="category", uselist=False)
    user = relationship("Users", back_populates="categories",
                        uselist=False, cascade="all")
    balance = Column(Float)

    def __init__(self, name, user_id):
        self.name = name
        self.user_id = user_id
