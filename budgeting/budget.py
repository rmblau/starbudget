from datetime import date

import sqlalchemy
from .database import Transaction, Categories, Users
from .base import Session
from sqlalchemy import BigInteger, insert, select, asc, func, update, insert
from sqlalchemy.orm import selectinload


class Budget():

    async def add_transaction(self, amount: float, note: str, date_of_transaction: float, user_id: BigInteger, categories=None):
        async with Session() as session:
            transaction = Transaction(
                amount=amount, note=note, date=date_of_transaction, user_id=user_id, categories=categories)
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
            await session.commit()
            return balance

    async def get_user_categories(self, user_id):
        async with Session() as session:
            categories = await session.execute(select(Categories)
                                               .where(Categories.user_id == user_id).options(
                selectinload(Categories.user)
            )
            )
            category = categories.scalars().all()
            return category

    async def create_category(self, user_id, category):
        async with Session() as session:
            category = Categories(name=category, user_id=user_id)
            session.add(category)
            await session.commit()
        return category

    async def create_user(self, name,  user_id, bank_balance, categories):
        async with Session() as session:
            user = Users(name=name, user_id=user_id,
                         bank_balance=bank_balance, categories=Categories(name=categories, user_id=user_id))
            session.add(user)
            await session.commit()
        return user
