
from datetime import datetime

from psutil import users
from budgeting.database import Users, Categories, Income
from .base import Session
from sqlalchemy import BigInteger, insert, select, update, insert


class User():

    async def set_balance(self, user_id: BigInteger, balance: float):
        async with Session() as session:
            balance = await session.execute(update(Users).where(Users.user_id == user_id).values(bank_balance=balance))
            await session.commit()
            return balance

    async def add_income(self, user_id: BigInteger, amount: float):
        async with Session() as session:
            income_amount = Income(user_id, amount)
            session.add(income_amount)
            await session.commit()
            return income_amount

    async def create_balance(self, user_id: BigInteger, balance: float):
        async with Session() as session:
            balance = await session.execute(update(Users).where(Users.user_id == user_id).values(user_id=user_id, bank_balance=balance))
            await session.commit()
            return balance

    async def get_balance(self, user_id: BigInteger):
        async with Session() as session:
            bank_balance = await session.execute(select(Users.bank_balance).where(Users.user_id == user_id))
            balance = bank_balance.scalar()
            return balance

    async def update_balance(self, user_id: BigInteger, balance: float):
        async with Session() as session:
            bank_balance = await session.execute(update(Users).values(bank_balance=balance).where(Users.user_id == user_id))
            await session.commit()
            return bank_balance

    async def get_user(self, user_id):
        async with Session() as session:
            user = await session.execute(select(Users.user_id).where(Users.user_id == user_id))
            await session.commit()
            return user.scalar_one_or_none()

    async def create_user(self, name, user_id, categories, bank_balance=None, first_login=True):
        async with Session() as session:
            user = Users(name=name, user_id=user_id,
                         bank_balance=bank_balance, categories=Categories(categories, user_id), first_login=first_login)
            session.add(user)
            await session.commit()
        return

    async def update_user(self, user_id, categories, bank_balance):
        async with Session() as session:
            user = await session.execute(update(Users).where(Users.user_id == user_id).values(categories=categories, bank_balance=bank_balance))
            await session.commit()
        return user

    async def get_first_login(self, user_id):
        async with Session() as session:
            user = await session.execute(select(Users.first_login).where(Users.user_id == user_id))
            await session.commit()
            return user.scalar()

    async def update_first_login(self, user_id):
        async with Session() as session:
            first_login = await session.execute(update(Users).where(Users.user_id == user_id).values(first_login=False))
            await session.commit()
            return first_login
