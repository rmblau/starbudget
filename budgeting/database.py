from datetime import datetime
from sqlalchemy.dialects.postgresql import TIME
from enum import unique
from h11 import Data
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
    income = relationship("Income", back_populates="income_amount", uselist=False)

    def __init__(self, name, user_id, bank_balance, income, categories, first_login):
        self.name = name
        self.user_id = user_id
        self.bank_balance = bank_balance
        self.categories = categories
        self.income = income
        self.first_login = first_login

class Income(Base):
    __tablename__ = 'income'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey(
        "users.user_id", name="fk_user_id"))
    amount = Column(Float)
    source = Column(String)
    date = Column(Date)
    date_added = Column(String)
    income_amount = relationship("Users", back_populates="income", uselist=False)

    def __init__(self, user_id, amount, source, date, date_added):
        self.user_id = user_id
        self.amount = amount
        self.source = source
        self.date = date
        self.date_added = date_added
       


class Transaction(Base):
    __tablename__ = 'expenses'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey(
        "users.user_id", name="fk_user_id"))
    amount = Column(Float)
    recipient = Column(String)
    note = Column(String)
    date = Column(Date)
    date_added = Column(String)
    user = relationship("Users", back_populates="transactions",
                        uselist=False, cascade="all")
    category = relationship(
        "Categories", back_populates="transaction", uselist=False)
    categories = Column(String, ForeignKey(
        "categories.name", onupdate="cascade"))
    

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
    balance = Column(Float)
    transaction = relationship(
        "Transaction", back_populates="category",uselist=False)
   
    user = relationship("Users", back_populates="categories",
                        uselist=False, foreign_keys=[user_id], cascade="all")
    hidden = Column(Boolean)
    

    def __init__(self, name, user_id, balance, hidden):
        self.name = name
        self.user_id = user_id
        self.balance = balance
        self.hidden = hidden
