from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
import os

# התעלם מה-DATABASE_URL מ-Railway, השתמש תמיד ב-SQLite
DB_URL = "sqlite+aiosqlite:///bot/database/data/bot.db"

engine = create_async_engine(DB_URL, echo=False)
async_session = async_sessionmaker(engine, expire_on_commit=False)
