import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.types import Update
from aiohttp import web
from bot.config import settings
from bot.utils.logger import logger
from bot.database.models import Base
from bot.database.session import engine
from bot.routers import routers

TELEGRAM_API_URL = "https://api.telegram.org"
WEBHOOK_PATH = "/webhook"
HEALTH_PATH = "/health"

bot = Bot(token=settings.bot_token)
dp = Dispatcher()
for router in routers:
    dp.include_router(router)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database initialized.")

async def on_startup(app: web.Application):
    await init_db()
    public_domain = os.environ.get("RAILWAY_PUBLIC_DOMAIN")
    if public_domain:
        webhook_url = f"https://{public_domain}{WEBHOOK_PATH}"
        await bot.set_webhook(webhook_url)
        logger.info(f"Webhook set to {webhook_url}")
    else:
        logger.info("Running locally, use polling")
        asyncio.create_task(dp.start_polling(bot))

async def on_shutdown(app: web.Application):
    await bot.delete_webhook()
    await bot.session.close()

async def webhook_handler(request):
    try:
        data = await request.json()
        update = Update(**data)
        await dp.feed_webhook_update(bot, update)
        return web.Response(status=200)
    except Exception as e:
        logger.error(f"Webhook error: {e}")
        return web.Response(status=500)

async def health_handler(request):
    return web.Response(text="OK")

app = web.Application()
app.router.add_post(WEBHOOK_PATH, webhook_handler)
app.router.add_get(HEALTH_PATH, health_handler)

# טיפול בקבצים סטטיים  הגשת public/
static_path = os.path.join(os.path.dirname(__file__), "..", "public")
if os.path.isdir(static_path):
    app.router.add_static('/landing/', path=os.path.join(static_path, 'landing'), show_index=True)
    logger.info(f"Static files served from {static_path}/landing")

app.on_startup.append(on_startup)
app.on_shutdown.append(on_shutdown)

if __name__ == "__main__":
    if os.environ.get("RAILWAY_PUBLIC_DOMAIN"):
        web.run_app(app, host="0.0.0.0", port=8080)
    else:
        asyncio.run(init_db())
        logger.info("Bot started. Polling...")
        asyncio.run(dp.start_polling(bot))
