from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from bot.config import settings

db_url = settings.database_url
# PostgreSQL: וידוא שימוש ב-asyncpg
if db_url.startswith("postgresql://"):
    db_url = db_url.replace("postgresql://", "postgresql+asyncpg://", 1)
elif db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql+asyncpg://", 1)

engine = create_async_engine(
    db_url,
    echo=False,
    pool_size=10 if "postgresql" in db_url else None,
    max_overflow=20 if "postgresql" in db_url else None
)
async_session = async_sessionmaker(engine, expire_on_commit=False)

async def get_db():
    async with async_session() as session:
        yield session
