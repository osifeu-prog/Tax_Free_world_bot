import asyncio
import os
from aiogram import Bot, Dispatcher
from aiohttp import web
from bot.config import settings
from bot.utils.logger import logger
from bot.database.models import Base
from bot.database.session import engine
from bot.routers import routers

HEALTH_PATH = "/health"

bot = Bot(token=settings.bot_token)
dp = Dispatcher()
for router in routers:
    dp.include_router(router)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database initialized.")

async def health_handler(request):
    return web.Response(text="OK")

async def index_handler(request):
    return web.FileResponse(os.path.join(os.path.dirname(__file__), "..", "public", "index.html"))

async def start_polling():
    await bot.delete_webhook(drop_pending_updates=True)
    logger.info("Starting polling...")
    await dp.start_polling(bot)

async def start_http():
    app = web.Application()
    app.router.add_get(HEALTH_PATH, health_handler)
    app.router.add_get("/", index_handler)

    static_path = os.path.join(os.path.dirname(__file__), "..", "public")
    if os.path.isdir(static_path):
        app.router.add_static('/landing/', path=os.path.join(static_path, 'landing'), show_index=True)
        logger.info(f"Static files served from {static_path}/landing")

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host="0.0.0.0", port=8080)
    logger.info("HTTP server starting on port 8080")
    await site.start()
    await asyncio.Event().wait()

async def main():
    await init_db()
    await asyncio.gather(
        start_polling(),
        start_http()
    )

if __name__ == "__main__":
    asyncio.run(main())
