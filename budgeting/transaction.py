from datetime import date, datetime

import sqlalchemy

from budgeting.categories import Categories
from .database import Transaction
from .base import Session
from sqlalchemy import BigInteger, delete, insert, select, asc, func, update, insert
from sqlalchemy.orm import selectinload


class Transactions():

    async def add_transaction(self, amount: float, recipient: str, note: str, date_of_transaction: float, user_id: BigInteger, categories: Categories, date_added: datetime):
        async with Session() as session:
            transaction = Transaction(
                amount=float(amount), recipient=recipient, note=note, date=date_of_transaction, user_id=user_id, categories=categories, date_added=date_added)
            session.add(transaction)
            await session.commit()
        return transaction

    async def edit_transaction(self, amount: float, recipient: str, note: str, date_of_transactions: float, user_id: BigInteger, old_category_id: int, categories: str, submit_time: date):
        async with Session() as session:
            now = datetime.utcnow()
            updated_transaction = await session.execute(update(Transaction).values(amount=float(amount), recipent=recipient, note=note, date=date_of_transactions, user_id=user_id, categories=categories, date_added=now).where(Transaction.user_id == user_id).where(Transaction.id == old_category_id).where(Transaction.date_added == submit_time))
            await session.commit()
        return updated_transaction

    async def delete_transaction(self, user_id: BigInteger, old_category_id: int):
        async with Session() as session:
            updated_transaction = await session.execute(delete(Transaction).where(Transaction.user_id == user_id).where(Transaction.id == old_category_id))
            await session.commit()
        return updated_transaction

    async def get_transaction(self, user_id):
        async with Session() as session:
            transaction = await session.execute(select(Transaction).where(Transaction.user_id == user_id).order_by(Transaction.date.asc()))
            transactions = transaction.scalars().all()
            return transactions

    async def get_transaction_id(self, user_id, amount: float, note: str, date: datetime, category: Categories, submit_time: datetime):
        async with Session() as session:
            transaction_id = await session.execute(select(Transaction.id).where(Transaction.user_id == user_id).where(Transaction.amount == float(amount)).where(Transaction.date == datetime.date(date)).where(Transaction.categories == category).where(Transaction.note == note).where(Transaction.date_added == datetime(submit_time)))
            return transaction_id.scalar_one_or_none()

    async def sum_of_transactions(self, user_id):
        async with Session() as session:
            transaction = await session.execute(select(sqlalchemy.func.coalesce(sqlalchemy.func.sum(Transaction.amount), 0.00)).where(Transaction.user_id == user_id))
            transactions = transaction.scalar()
            return transactions

    async def last_five_transactions(self, user_id: BigInteger):
        async with Session() as session:
            transaction = await session.execute(select(Transaction).where(Transaction.user_id == user_id).limit(5).order_by(Transaction.date.desc()))
            transactions = transaction.scalars().all()
            return transactions
