from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.schema import MetaData
engine = create_async_engine(
    'sqlite+aiosqlite:///budget.sql', echo=True,)

Session = sessionmaker(
    bind=engine, expire_on_commit=False, class_=AsyncSession)
Base = declarative_base(class_registry=dict())
metadata = MetaData()


async def create_table():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
