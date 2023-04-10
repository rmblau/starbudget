from datetime import date
import datetime
import sqlalchemy
import calendar

from dateutil.relativedelta import relativedelta
from sqlalchemy import BigInteger, delete, select, update
from .database import Transaction, Income, Categories as UserCategories
from .base import Session


async def last_five_transactions(user_id: BigInteger):
    now = datetime.datetime.now()
    number_of_days = calendar.monthrange(now.year, now.month)[1]
    first_of_month = datetime.datetime.today().replace(day=1) - datetime.timedelta(days=1)
    async with Session() as session:
        transaction = await session.execute(
            select(Transaction).where(Transaction.user_id == user_id).where(
                Transaction.date.between(first_of_month, now)).limit(5).order_by(Transaction.date.desc()))
        transactions = transaction.scalars().all()
        recipient = [t.recipient for t in transactions]
        amount = [t.amount for t in transactions]
        description = [t.note for t in transactions]
        category = [t.categories for t in transactions]
        category_stripped = [c.split('~')[0] for c in category]
        date = [d.date for d in transactions]
        return recipient, amount, description, category_stripped, date


async def add_transaction(amount: float, recipient: str, note: str, date_of_transaction: datetime, user_id: BigInteger,
                          categories: str, date_added: str) -> Transaction:
    async with Session() as session:
        transaction = Transaction(
            amount=float(amount), recipient=recipient, note=note, date=date_of_transaction, user_id=user_id,
            categories=f'{categories}~{user_id}', date_added=date_added)
        session.add(transaction)
        await session.commit()
    return transaction


async def edit_transaction(amount: float, recipient: str, note: str, date_of_transactions: date, user_id: str,
                           old_category_id: int, categories: str, submit_time: str):
    async with Session() as session:
        now = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f")
        updated_transaction = await session.execute(
            update(Transaction).values(recipient=recipient, amount=float(amount), note=note,
                                       date=date_of_transactions, user_id=user_id, categories=categories,
                                       date_added=now).where(Transaction.user_id == user_id).where(
                Transaction.id == old_category_id).where(Transaction.date_added == submit_time))
        await session.commit()
    return updated_transaction


async def delete_transaction(user_id: str, old_category_id: int):
    async with Session() as session:
        updated_transaction = await session.execute(
            delete(Transaction).where(Transaction.user_id == user_id).where(Transaction.id == old_category_id))
        await session.commit()
    return updated_transaction


async def get_transaction_category(user_id):
    async with Session() as session:
        transaction = await session.execute(select(Transaction.categories).select_from(UserCategories).where(
            UserCategories.user_id == user_id).join(UserCategories.transaction))
        transaction_category = transaction.scalars().all()
        return transaction_category


async def get_transaction(user_id):
    async with Session() as session:
        transaction = await session.execute(
            select(Transaction).where(Transaction.user_id == user_id).order_by(Transaction.date.asc()))
        transactions = transaction.scalars().all()
        return transactions


async def get_month_transaction(user_id, month):
    now = datetime.datetime.now()
    current_month = datetime.datetime.strptime(month, '%b').date().replace(year=now.year)
    number_of_days = calendar.monthrange(now.year, now.month)[1]
    first_of_month = current_month - datetime.timedelta(days=1)
    last_day_of_month = current_month + relativedelta(day=number_of_days)
    async with Session() as session:
        transaction = await session.execute(
            select(Transaction).where(Transaction.user_id == user_id).where(Transaction.date >= current_month)
            .where(Transaction.date <= last_day_of_month).order_by(Transaction.date.asc()))
        transactions = transaction.scalars().all()
        return transactions


async def get_transaction_by_category(user_id, category):
    async with Session() as session:
        transaction = await session.execute(select(Transaction).where(Transaction.user_id == user_id).where(
            Transaction.categories == category).order_by(Transaction.date.asc()))
        transactions = transaction.scalars().all()
        return transactions


async def get_transaction_id(user_id, recipient: str, amount: float, note: str, date: date,
                             category: str, submit_time: datetime):
    async with Session() as session:
        transaction = await session.execute(select(Transaction.id)
                                            .where(Transaction.user_id == user_id)
                                            .where(Transaction.recipient == recipient)
                                            .where(Transaction.amount == amount)
                                            .where(Transaction.date == date)
                                            .where(Transaction.categories == category)
                                            .where(Transaction.note == note)
                                            .where(Transaction.date_added == submit_time))
        transaction_id = transaction.scalar_one_or_none()
        return transaction_id


async def sum_of_transactions(user_id):
    async with Session() as session:
        transaction = await session.execute(
            select(sqlalchemy.func.coalesce(sqlalchemy.func.sum(Transaction.amount), 0.00)).where(
                Transaction.user_id == user_id).where(Transaction.categories != f"{'Income'}~{user_id}"))
        transactions = transaction.scalar()
        return transactions


async def month_sum_of_transactions(user_id, month):
    now = datetime.datetime.now()
    current_month = datetime.datetime.strptime(month, '%b').date().replace(year=now.year)
    number_of_days = calendar.monthrange(now.year, now.month)[1]
    first_of_month = current_month - datetime.timedelta(days=1)
    last_day_of_month = current_month + relativedelta(day=number_of_days)
    async with Session() as session:
        transaction = await session.execute(
            select(sqlalchemy.func.coalesce(sqlalchemy.func.sum(Transaction.amount), 0.00)).where(
                Transaction.user_id == user_id).where(Transaction.categories != f"{'Income'}~{user_id}").where(
                Transaction.date >= current_month).where(Transaction.date <= last_day_of_month))
        transactions = transaction.scalar()
        return round(transactions, 4)


async def sum_of_income(user_id):
    async with Session() as session:
        income_amount = await session.execute(
            select(sqlalchemy.func.coalesce(sqlalchemy.func.sum(Transaction.amount), 0.00)).where(
                Income.user_id == user_id).where(Transaction.categories == f"{'Income'}~{user_id}"))
        income = income_amount.scalar()
        return income
