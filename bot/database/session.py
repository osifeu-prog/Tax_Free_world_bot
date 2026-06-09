from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
import os

db_url = os.getenv("DATABASE_URL", "sqlite+aiosqlite:////app/bot/database/bot.db")
engine = create_async_engine(db_url, echo=False)
async_session = async_sessionmaker(engine, expire_on_commit=False)
