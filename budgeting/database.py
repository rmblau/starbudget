from sqlalchemy import Column, Float, ForeignKey, String, Integer, Date
from sqlalchemy.orm import relationship
from .base import Base
from sqlalchemy.types import BigInteger


class Transaction(Base):
    __tablename__ = 'budget'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger)
    amount = Column(Float)
    note = Column(String)
    date = Column(Date)
    balance = Column(Float)
    categories = relationship("Categories", backref="budget")

    def __init__(self, amount, note, date, user_id, balance) -> None:
        self.amount = amount
        self.note = note
        self.date = date
        self.user_id = user_id
        self.balance = balance


class Categories(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    user_id = Column(BigInteger, ForeignKey("budget.user_id"))
