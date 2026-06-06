from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from bot.config import settings

db_url = settings.database_url
if not db_url.startswith("sqlite"):
    # ברירת מחדל: SQLite (אם Railway לא נתן PostgreSQL)
    db_url = "sqlite+aiosqlite:///./data.db"

engine = create_async_engine(db_url, echo=False)
async_session = async_sessionmaker(engine, expire_on_commit=False)

async def get_db():
    async with async_session() as session:
        yield session
