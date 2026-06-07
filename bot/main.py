import asyncio, os
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand, BotCommandScopeDefault, WebAppInfo, MenuButtonWebApp
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

async def set_default_commands():
    commands = [
        BotCommand(command="start", description="🚀 דף הבית"),
        BotCommand(command="compare", description="💸 מחשבון עמלות"),
        BotCommand(command="budget", description="📊 מחשבון תקציב"),
        BotCommand(command="profile", description="👤 פרופיל כלכלי"),
        BotCommand(command="expenses", description="📋 הוצאות"),
        BotCommand(command="addexpense", description="➕ הוסף הוצאה"),
        BotCommand(command="setincome", description="💰 עדכן הכנסה"),
        BotCommand(command="delexpense", description="🗑️ מחק הוצאה"),
        BotCommand(command="wallet", description="👛 ארנק TON"),
        BotCommand(command="why", description="🔍 למה TON?"),
        BotCommand(command="business", description="🏢 לעסקים"),
        BotCommand(command="crypto", description="🪙 מה זה קריפטו"),
        BotCommand(command="cbdc", description="🏦 מה זה CBDC"),
        BotCommand(command="decentral", description="🔓 ביזור מול ריכוזיות"),
        BotCommand(command="socio", description="🌿 סוציוקרטיה"),
        BotCommand(command="anti", description="🛡️ טכנולוגיות נגד שחיתות"),
        BotCommand(command="edu", description="🎓 חינוך וכלכלה"),
        BotCommand(command="faq", description="❓ שאלות נפוצות"),
        BotCommand(command="tip", description="💡 טיפ יומי"),
        BotCommand(command="stats", description="📊 סטטיסטיקות"),
        BotCommand(command="top", description="🏆 לוח מובילים"),
        BotCommand(command="ref", description="🔗 קוד הפניה"),
        BotCommand(command="contact", description="📬 צור קשר"),
        BotCommand(command="id", description="🆔 זיהוי"),
        BotCommand(command="daily", description="📈 סיכום יומי"),
        BotCommand(command="mydata", description="📋 הנתונים שלי"),
        BotCommand(command="help", description="ℹ️ עזרה"),
        BotCommand(command="admin", description="🔐 אדמין"),
        BotCommand(command="debug", description="🔧 סטטוס מערכת"),
        BotCommand(command="miniapp", description="📱 מחשבון ויזואלי"),
        BotCommand(command="keyboard", description="⌨️ מקלדת"),
        BotCommand(command="hide", description="🙈 הסתר מקלדת"),
        BotCommand(command="export", description="📤 ייצוא לוגים"),
    ]
    await bot.set_my_commands(commands, scope=BotCommandScopeDefault())
    await bot.set_chat_menu_button(
        menu_button=MenuButtonWebApp(
            text="📱 מחשבון ויזואלי",
            web_app=WebAppInfo(url="https://taxfreeworldbot-production.up.railway.app/landing/miniapp.html")
        )
    )

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
    await set_default_commands()
    logger.info("Commands & menu set. Polling...")
    await dp.start_polling(bot)

async def start_http():
    app = web.Application()
    app.router.add_get(HEALTH_PATH, health_handler)
    app.router.add_get("/", index_handler)
    static_path = os.path.join(os.path.dirname(__file__), "..", "public")
    if os.path.isdir(static_path):
        app.router.add_static('/landing/', path=os.path.join(static_path, 'landing'), show_index=True)
        logger.info(f"Static served from {static_path}/landing")
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host="0.0.0.0", port=8080)
    logger.info("HTTP server on 8080")
    await site.start()
    await asyncio.Event().wait()

async def main():
    await init_db()
    await asyncio.gather(start_polling(), start_http())

if __name__ == "__main__":
    asyncio.run(main())
