from datetime import date

import sqlalchemy
from .database import Transaction, Categories, Users
from .base import Session
from sqlalchemy import BigInteger, insert, select, asc, func, update, insert
from sqlalchemy.orm import selectinload


class Transactions():

    async def add_transaction(self, amount: float, note: str, date_of_transaction: float, user_id: BigInteger, categories=None):
        async with Session() as session:
            transaction = Transaction(
                amount=amount, note=note, date=date_of_transaction, user_id=user_id, categories=categories)
            session.add(transaction)
            await session.commit()
        return transaction

    async def get_transaction(self, user_id: BigInteger):
        async with Session() as session:
            transaction = await session.execute(select(Transaction).where(Transaction.user_id == user_id).order_by(Transaction.date.asc()))
            transactions = transaction.scalars().all()
            return transactions

    async def sum_of_transactions(self, user_id: BigInteger):
        async with Session() as session:
            transaction = await session.execute(select(sqlalchemy.func.sum(Transaction.amount)).where(Transaction.user_id == user_id))
            transactions = transaction.scalar()
            return transactions

    async def last_five_transactions(self, user_id: BigInteger):
        async with Session() as session:
            transaction = await session.execute(select(Transaction).where(Transaction.user_id == user_id).limit(5).order_by(Transaction.date.desc()))
            transactions = transaction.scalars().all()
            return transactions
