from datetime import date

import sqlalchemy
from .database import Transaction, Categories as UserCategories, Users
from .base import Session
from sqlalchemy import BigInteger, insert, select, asc, func, update, insert, delete
from sqlalchemy.orm import selectinload


class Categories():

    async def get_user_categories(self, user_id):
        async with Session() as session:
            categories = await session.execute(select(UserCategories)
                                               .join(Users))
            category = categories.scalars().all()
            await session.commit()
            return category

    async def create_category(self, user_id, category):
        async with Session() as session:
            category = UserCategories(name=category, user_id=user_id)
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
        # category_id = await self.get_category_id(user_id)
        async with Session() as session:
            category = await session.execute(update(UserCategories).values(name=new_name).where(UserCategories.user_id == user_id).where(UserCategories.name == old_name).execution_options(synchronize_session="fetch"))
            await session.commit()
            return category

    async def delete_category(self, name, user_id):
        async with Session() as session:
            category = await session.execute(delete(Categories).where(Categories.name == name).where(Categories.user_id == user_id))
            await session.commit()
            return category
