from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from bot.config import settings
import os

# נסה קודם את DATABASE_URL מהסביבה (Railway), אחרת fallback ל‑SQLite
db_url = os.environ.get("DATABASE_URL")
if db_url:
    # אם זה PostgreSQL, ודא שאנחנו משתמשים בסיסמה הנכונה
    db_url = db_url.replace("postgresql://", "postgresql+asyncpg://")
else:
    db_url = "sqlite+aiosqlite:///./bot.db"

engine = create_async_engine(db_url, echo=False)
async_session = async_sessionmaker(engine, expire_on_commit=False)
