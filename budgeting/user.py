from datetime import datetime
from budgeting.database import Users, Categories, Income
from .base import Session
import sqlalchemy
from sqlalchemy import BigInteger, select, update


async def get_first_login(user_id):
    async with Session() as session:
        user = await session.execute(select(Users.first_login).where(Users.user_id == user_id))
        await session.commit()
        return user.scalar()


async def update_first_login(user_id):
    async with Session() as session:
        first_login = await session.execute(update(Users).where(Users.user_id == user_id).values(first_login=False))
        await session.commit()
        return first_login


async def update_user(user_id, categories, bank_balance):
    async with Session() as session:
        user = await session.execute(update(Users).where(Users.user_id == user_id).values(categories=categories,
                                                                                          bank_balance=float(
                                                                                              bank_balance)))
        await session.commit()
    return user


async def create_user(name, user_id, categories, income, bank_balance=None, first_login=True, balance=0.0, hidden=False):
    async with Session() as session:
        user = Users(name=name, user_id=user_id,
                     bank_balance=bank_balance, categories=Categories(categories, user_id, balance=balance, hidden=hidden),
                     income=Income(user_id, income, source="first entry", date=datetime.strptime(datetime.today().strftime("%Y-%m-%d"), "%Y-%m-%d"),  date_added=datetime.today().strftime("%Y-%-m-%d")), first_login=first_login)
                     
        session.add(user)
        await session.commit()
    return user


async def get_user_id(user_id):
    async with Session() as session:
        user = await session.execute(select(Users.user_id).where(Users.user_id == user_id))
        await session.commit()
        return user.scalar_one_or_none()


async def get_user(user_id):
    async with Session() as session:
        user = await session.execute(select(Users.income).where(Users.user_id == user_id))
        await session.commit()
        return user.scalar_one_or_none()


async def update_balance(user_id: BigInteger, balance: float):
    async with Session() as session:
        bank_balance = await session.execute(
            update(Users).values(bank_balance=balance).where(Users.user_id == user_id))
        await session.commit()
        return bank_balance


async def get_balance(user_id: BigInteger):
    async with Session() as session:
        bank_balance = await session.execute(select(Users.bank_balance).where(Users.user_id == user_id))
        balance = bank_balance.scalar()
        return balance


async def create_balance(user_id: BigInteger, balance: float):
    async with Session() as session:
        balance = await session.execute(
            update(Users).where(Users.user_id == user_id).values(user_id=user_id, bank_balance=float(balance)))
        await session.commit()
        return balance


async def get_income(user_id: BigInteger):
    async with Session() as session:
        user = await session.execute(
            select(Income.amount).select_from(Users).where(user_id == user_id).limit(1).order_by(
                Income.id.desc()).join(Users.income))
        await session.commit()
        return user.scalar()


async def sum_of_income(user_id: BigInteger):
    async with Session() as session:
        user = await session.execute(
            select(sqlalchemy.func.coalesce(sqlalchemy.func.sum(Income.amount), 0.00)).select_from(Users).where(
                user_id == user_id).join(Users.income))
        await session.commit()
        return user.scalar()


async def add_income(user_id: BigInteger, amount: float, source: str, date: float, date_added: str) -> Income:
    async with Session() as session:
        income_amount = Income(user_id, amount, source, date, date_added)
        session.add(income_amount)
        await session.commit()
        return income_amount.amount


async def set_balance(user_id: BigInteger, balance: float):
    async with Session() as session:
        balance = await session.execute(update(Users).where(Users.user_id == user_id).values(bank_balance=balance))
        await session.commit()
        return balance

