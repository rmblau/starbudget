import sqlalchemy

from .database import Categories as UserCategories, Income, Transaction
from .base import Session
from sqlalchemy.sql import Delete
from sqlalchemy import select, update


async def get_category_transactions(category, user_id) -> str:
    async with Session() as session:
        transactions = await session.execute(
            select(UserCategories.transaction).where(UserCategories.name == category).where(
                UserCategories.user_id == user_id))
        return transactions.scalar()


async def delete_category(name, user_id):
    async with Session() as session:
        category = await session.execute(
            Delete(UserCategories).where(UserCategories.name == name).where(UserCategories.user_id == user_id))
        await session.commit()
        return category


async def get_category_balance(category, user_id) -> float:
    async with Session() as session:
        category_balance = await session.execute(
            select(UserCategories.balance).where(UserCategories.name == category).where(
                UserCategories.user_id == user_id))
        return category_balance.scalar()


async def update_category_balance(category, user_id, balance):
    async with Session() as session:
        category = await session.execute(
            update(UserCategories).values(balance=balance).where(UserCategories.user_id == user_id)
            .where(UserCategories.name == category))
        await session.commit()
        return category


async def update_category_name(new_name, old_name, user_id):
    async with Session() as session:
        category = await session.execute(
            update(UserCategories).values(name=f'{new_name}~{user_id}').where(UserCategories.user_id == user_id).where(
                UserCategories.name == f'{old_name}~{user_id}').execution_options(synchronize_session="fetch"))
        await session.commit()
        return category


async def get_old_category_id(user_id, category_name):
    async with Session() as session:
        category_id = await session.execute(select(UserCategories.id).where(UserCategories.user_id == user_id).where(
            UserCategories.name == category_name))
        return category_id.scalar()


async def get_category_id(user_id):
    async with Session() as session:
        category_id = await session.execute(select(UserCategories.id).where(UserCategories.user_id == user_id))
        return category_id.scalar()


async def create_category(user_id, category, balance, hidden=False, income=False):
    async with Session() as session:
        category = UserCategories(
            name=f'{category}~{user_id}', user_id=user_id, balance=balance, hidden=hidden, income=income)
        session.add(category)
        await session.commit()
    return category


async def get_all_minus_income_user_categories(user_id):
    async with Session() as session:
        categories = await session.execute(
            select(UserCategories).where(UserCategories.user_id == user_id).where(UserCategories.income == False))
        category = categories.scalars().all()
        await session.commit()
        return category


async def get_all_user_categories(user_id):
    async with Session() as session:
        categories = await session.execute(select(UserCategories).where(UserCategories.user_id == user_id))
        category = categories.scalars().all()
        await session.commit()
        return category


async def get_unhidden_user_categories(user_id):
    async with Session() as session:
        categories = await session.execute(
            select(UserCategories).where(UserCategories.user_id == user_id).where(UserCategories.hidden == False))
        category = categories.scalars().all()
        await session.commit()
        return category


async def sum_of_category_transactions(user_id, category_id):
    async with Session() as session:
        transaction = await session.execute(
            select(sqlalchemy.func.coalesce(sqlalchemy.func.sum(Transaction.amount), 0.00)).where(
                Transaction.user_id == user_id).where(UserCategories.name == category_id))
        transactions = transaction.scalar()
        return transactions
