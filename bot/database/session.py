from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from bot.config import settings

# זיהוי סוג ה-DB לפי ה-URL
db_url = settings.database_url
if db_url.startswith("postgresql://"):
    # PostgreSQL  שימוש ב-asyncpg
    engine = create_async_engine(db_url, echo=False, pool_size=10, max_overflow=20)
else:
    # SQLite (מקומי)
    engine = create_async_engine(db_url, echo=False)

async_session = async_sessionmaker(engine, expire_on_commit=False)

async def get_db():
    async with async_session() as session:
        yield session
