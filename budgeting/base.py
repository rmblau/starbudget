from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from starlette.config import Config
from sqlalchemy.sql.schema import MetaData
import os
config = Config(".env")
engine = create_async_engine(
    config.get('LOCAL_DATABASE'), echo=False,)
Session = sessionmaker(
    bind=engine, expire_on_commit=False, class_=AsyncSession)
Base = declarative_base(class_registry=dict())
metadata = MetaData()


async def create_table():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
