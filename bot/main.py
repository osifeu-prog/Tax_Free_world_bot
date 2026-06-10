import asyncio, os, pkgutil, importlib, time
from pathlib import Path

start_time = time.time()

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand, BotCommandScopeDefault, MenuButtonCommands
from aiohttp import web

from bot.config import settings
from bot.api.email_routes import register, login
from bot.utils.logger import logger
from bot.database.models import Base
from bot.database.session import engine
import bot.routers as routers_pkg

bot = Bot(token=settings.bot_token)
dp = Dispatcher()
from bot.middlewares.useless_middleware import UselessShareMiddleware
dp.message.middleware(UselessShareMiddleware())

from bot.routers.start import router as start_router
dp.include_router(start_router)

for _, modname, _ in pkgutil.iter_modules(routers_pkg.__path__):
    if modname == 'start': continue
    try:
        module = importlib.import_module(f"bot.routers.{modname}")
        if hasattr(module, 'router'):
            dp.include_router(module.router)
            logger.info(f"✅ Router {modname} loaded")
    except Exception as e:
        logger.error(f"❌ Failed to load router {modname}: {e}")

async def set_default_commands():
    commands = [
        BotCommand(command="start", description="🚀 דף הבית"),
        BotCommand(command="menu", description="📋 תפריט ראשי"),
        BotCommand(command="useless", description="🤖 יוסלס AI"),
        BotCommand(command="pension", description="📊 פנסיה"),
        BotCommand(command="city", description="🏙️ TON City"),
        BotCommand(command="market", description="📈 בורסה"),
        BotCommand(command="donate", description="💖 תרומה"),
        BotCommand(command="report", description="📊 דוח מערכת"),
        BotCommand(command="help", description="❔ עזרה"),
        BotCommand(command="ref", description="🔗 הפניה"),
    ]
    await bot.set_my_commands(commands, scope=BotCommandScopeDefault())
    await bot.set_chat_menu_button(menu_button=MenuButtonCommands())

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("✅ Database initialized")

async def health_check(request):
    return web.Response(text="OK")

async def index_handler(request):
    return web.FileResponse("public/landing/index.html")

async def start_http():
    app = web.Application()
    app.router.add_post("/api/auth/register", register)
    app.router.add_post("/api/auth/login", login)
    app.router.add_get("/health", health_check)
    app.router.add_get("/", index_handler)
    static_path = Path(__file__).parent.parent / "public"
    if static_path.is_dir():
        app.router.add_static('/landing/', path=str(static_path / 'landing'), show_index=True)
        logger.info("✅ Static files served from /landing")
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host="0.0.0.0", port=8080)
    await site.start()
    logger.info("🌐 HTTP Server running on 8080")

async def main():
    await init_db()
    await set_default_commands()
    await bot.delete_webhook(drop_pending_updates=True)
    logger.info(f"🚀 Bot started in {time.time() - start_time:.2f}s")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())