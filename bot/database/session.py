from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from bot.config import settings
import os

# השתמש ב‑DATABASE_URL מהסביבה (אם קיים), אחרת fallback ל‑settings
db_url = os.environ.get("DATABASE_URL")
if db_url:
    # PostgreSQL → asyncpg
    db_url = db_url.replace("postgresql://", "postgresql+asyncpg://")
else:
    db_url = settings.database_url

engine = create_async_engine(db_url, echo=False)
async_session = async_sessionmaker(engine, expire_on_commit=False)
