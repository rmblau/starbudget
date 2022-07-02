from datetime import date

import sqlalchemy
from .database import Transaction
from .base import Session
from sqlalchemy import BigInteger, select, asc, func, update


class Budget():

    async def add_transaction(self, amount: float, note: str, date_of_transaction: float, user_id: BigInteger, balance=0.0):
        async with Session() as session:
            transaction = Transaction(
                amount=amount, note=note, date=date_of_transaction, user_id=user_id, balance=balance)
            print(transaction)
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
            transactions = transaction.scalars().all()
            return transactions

    async def set_balance(self, user_id: BigInteger, balance: float):
        async with Session() as session:
            balance = await session.execute(update(Transaction).where(Transaction.user_id == user_id).values(balance=balance))
