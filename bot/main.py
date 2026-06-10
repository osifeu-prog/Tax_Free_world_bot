import asyncio
import logging
from aiogram import Bot, Dispatcher
from bot.config import BOT_TOKEN
from bot.database.session import engine
from bot.database.models import Base
# Import your routers
from bot.routers import start, profile, donate, pension, useless, admin  # add your other routers

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def init_db():
    """יצירת כל הטבלאות אוטומטית"""
    logger.info("🔧 Initializing database tables...")
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("✅ All tables created successfully!")
    except Exception as e:
        logger.error(f"❌ Failed to create tables: {e}")

async def main():
    await init_db()   # <-- חשוב: רץ בכל הפעלה
    
    bot = Bot(token=BOT_TOKEN, parse_mode='HTML')
    dp = Dispatcher()
    
    # Middlewares
    # dp.message.middleware(...) 
    
    # Routers
    dp.include_router(start.router)
    dp.include_router(profile.router)
    dp.include_router(donate.router)
    dp.include_router(pension.router)
    dp.include_router(useless.router)
    dp.include_router(admin.router)
    # הוסף את שאר ה-routers שלך כאן

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
