from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

# SQLite  הנתיב בתוך הקונטיינר, Volume ידאג לשמור
DATABASE_URL = "sqlite+aiosqlite:////app/bot/database/bot.db"

engine = create_async_engine(DATABASE_URL, echo=False)
async_session = async_sessionmaker(engine, expire_on_commit=False)
