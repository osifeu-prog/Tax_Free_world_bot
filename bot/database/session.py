from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from bot.config import settings
import os

# SQLite בלבד  עקיפת PostgreSQL
db_url = "sqlite+aiosqlite:///./bot.db"

engine = create_async_engine(db_url, echo=False)
async_session = async_sessionmaker(engine, expire_on_commit=False)
