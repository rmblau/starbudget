
from budgeting.user import User
from .database import Transaction, Categories as UserCategories, Users
from .base import Session
import itertools
from sqlalchemy import BigInteger, insert, select, asc, func, update, insert, delete
from sqlalchemy.orm import selectinload


class Categories():

    async def get_user_categories(self, user_id):
        async with Session() as session:
            categories = await session.execute(select(UserCategories).where(UserCategories.user_id == user_id))
            category = categories.scalars().all()
            delimiter = '~'
            #category_names = [c.name for c in category]
            #category_stripped = [c.split('~')[0] for c in category_names]
            print([c.name for c in category])
            await session.commit()
            return category

    async def create_category(self, user_id, category):
        async with Session() as session:
            category = UserCategories(
                name=f'{category}~{user_id}', user_id=user_id)
            session.add(category)
            await session.commit()
        return category

    async def get_category_id(self, user_id):
        async with Session() as session:
            category_id = await session.execute(select(UserCategories.id).where(UserCategories.user_id == user_id))
            return category_id.scalar()

    async def get_old_category_id(self, user_id, category_name):
        async with Session() as session:
            category_id = await session.execute(select(UserCategories.id).where(UserCategories.user_id == user_id).where(UserCategories.name == category_name))
            return category_id.scalar()

    async def update_category_name(self, new_name, old_name, user_id):
        async with Session() as session:
            category = await session.execute(update(UserCategories).values(name=f'{new_name}~{user_id}').where(UserCategories.user_id == user_id).where(UserCategories.name == f'{old_name}~{user_id}').execution_options(synchronize_session="fetch"))
            await session.commit()
            return category

    async def delete_category(self, name, user_id):
        async with Session() as session:
            category = await session.execute(delete(UserCategories).where(UserCategories.name == name).where(UserCategories.user_id == user_id))
            await session.commit()
            return category
