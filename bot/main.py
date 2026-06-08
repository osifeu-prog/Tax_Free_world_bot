import time
start_time = time.time()
# -*- coding: utf-8 -*-
import asyncio, os, pkgutil, importlib
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand, BotCommandScopeDefault, WebAppInfo, MenuButtonWebApp
from aiohttp import web
from bot.config import settings
from bot.api.email_routes import register, login
from bot.utils.logger import logger
from bot.database.models import Base
from bot.database.session import engine
from bot.migrate_i18n import add_lang_columns
import bot.routers as routers_pkg
from bot.routers import setwallet
from bot.routers import familygroup
from bot.routers import pension
from bot.routers import seed_courses
from bot.routers import academy
from bot.routers import language
from bot.routers import profile_citizen
from bot.routers import translations_status
from bot.routers import seed_kg
from bot.routers import report
from bot.routers import menu

HEALTH_PATH = "/health"

bot = Bot(token=settings.bot_token)
dp = Dispatcher()

# טעינה דינמית עמידה לשגיאות
loaded_routers = []
for importer, modname, ispkg in pkgutil.iter_modules(routers_pkg.__path__):
    try:
        module = importlib.import_module(f"bot.routers.{modname}")
        if hasattr(module, 'router'):
            dp.include_router(module.router)
            loaded_routers.append(modname)
            logger.info(f"✅ Router {modname} loaded")
    except Exception as e:
        logger.error(f"❌ Failed to load router {modname}: {e}")

async def set_default_commands():
    commands = [
        BotCommand(command="start", description="דף הבית"),
        BotCommand(command="compare", description="מחשבון עמלות"),
        BotCommand(command="budget", description="מחשבון תקציב"),
        BotCommand(command="profile", description="פרופיל כלכלי"),
        BotCommand(command="expenses", description="צפה בהוצאות"),
        BotCommand(command="addexpense", description="הוסף הוצאה"),
        BotCommand(command="setincome", description="עדכן הכנסה"),
        BotCommand(command="delexpense", description="מחק הוצאה"),
        BotCommand(command="wallet", description="ארנק TON"),
        BotCommand(command="why", description="למה TON?"),
        BotCommand(command="business", description="לעסקים"),
        BotCommand(command="crypto", description="מה זה קריפטו"),
        BotCommand(command="cbdc", description="מה זה CBDC"),
        BotCommand(command="decentral", description="ביזור מול ריכוזיות"),
        BotCommand(command="socio", description="סוציוקרטיה"),
        BotCommand(command="anti", description="טכנולוגיות נגד שחיתות"),
        BotCommand(command="edu", description="חינוך, כלכלה, רווחה"),
        BotCommand(command="academy_extended", description="ביזוריות, NFT, כלכלה חכמה"),
        BotCommand(command="academy_nft", description="NFT-זהות"),
        BotCommand(command="academy_dao", description="לימודי DAO"),
        BotCommand(command="faq", description="שאלות נפוצות"),
        BotCommand(command="tip", description="טיפ יומי"),
        BotCommand(command="stats", description="סטטיסטיקות"),
        BotCommand(command="top", description="לוח מובילים"),
        BotCommand(command="ref", description="קוד הפניה"),
        BotCommand(command="contact", description="צור קשר"),
        BotCommand(command="id", description="זיהוי"),
        BotCommand(command="daily", description="סיכום יומי"),
        BotCommand(command="mydata", description="הנתונים שלי"),
        BotCommand(command="gift", description="מתנה יומית"),
        BotCommand(command="help", description="עזרה"),
        BotCommand(command="admin", description="אזור אדמין"),
        BotCommand(command="debug", description="סטטוס מערכת"),
        BotCommand(command="miniapp", description="מחשבון ויזואלי"),
        BotCommand(command="keyboard", description="מקלדת"),
        BotCommand(command="hide", description="הסתר מקלדת"),
        BotCommand(command="export", description="ייצוא לוגים"),
        BotCommand(command="donate", description="תרומה"),
        BotCommand(command="feedback", description="דיווח"),
        BotCommand(command="whyus", description="למה אנחנו"),
        BotCommand(command="familyguide", description="המדריך למשפחה"),
        BotCommand(command="menu", description="תפריט ראשי"),
        BotCommand(command="architecture", description="ארכיטקטורת המערכת"),
        BotCommand(command="household", description="ניהול כלכלת הבית"),
        BotCommand(command="ai", description="שאל את הבינה"),
        BotCommand(command="ask", description="שאל שאלה"),
        BotCommand(command="addadmin", description="הוסף מנהל"),
        BotCommand(command="login", description="התחבר"),
        BotCommand(command="setpassword", description="שנה סיסמה"),
        BotCommand(command="requestadmin", description="בקש הרשאת ניהול"),
        BotCommand(command="removeadmin", description="הסר מנהל"),
        BotCommand(command="quiz", description="חידון"),
    ]
    await bot.set_my_commands(commands, scope=BotCommandScopeDefault())
    await bot.set_chat_menu_button(
        menu_button=MenuButtonWebApp(
            text="מחשבון ויזואלי",
            web_app=WebAppInfo(url="https://taxfreeworldbot-production.up.railway.app/landing/miniapp.html")
        )
    )

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        # הוסף עמודות email (SQLite לא תומך ב‑IF NOT EXISTS)
        from sqlalchemy import text
        for col, dtype in [("email", "VARCHAR(255)"), ("google_id", "VARCHAR(255)"), ("password_hash", "VARCHAR(255)")]:
            try:
                await conn.execute(text(f"ALTER TABLE users ADD COLUMN {col} {dtype}"))
            except Exception:
                pass
    logger.info("Database initialized.")
    await add_lang_columns()

async def health_handler(request):
    return web.Response(text="OK")

async def index_handler(request):
    return web.FileResponse(os.path.join(os.path.dirname(__file__), "..", "public", "index.html"))

async def api_profile(request):
    user_id = request.query.get("user_id")
    if not user_id:
        return web.json_response({"error": "missing user_id"}, status=400)
    from bot.services.profile_service import get_or_create_profile, get_total_savings, get_expenses
    profile = await get_or_create_profile(int(user_id))
    total = await get_total_savings(int(user_id))
    expenses = await get_expenses(int(user_id))
    return web.json_response({
        "user_id": int(user_id),
        "monthly_income": profile.monthly_income,
        "total_savings": round(total, 2),
        "expenses": [{"id": e.id, "category": e.category, "amount": e.amount, "frequency": e.frequency, "ton_savings": e.potential_ton_savings} for e in expenses]
    })

async def api_last_compare(request):
    user_id = request.query.get("user_id")
    if not user_id:
        return web.json_response({"error": "missing user_id"}, status=400)
    from bot.services.memory_service import get_user_memory
    mem = await get_user_memory(int(user_id))
    if mem and mem.last_command == "compare":
        parts = mem.last_params.split()
        amount = float(parts[0]) if parts else 500
        tx = int(parts[1]) if len(parts) > 1 else 10
    else:
        amount, tx = 500, 10
    return web.json_response({"amount": amount, "tx": tx})

async def debug_routers(request):
    return web.json_response({"loaded_routers": loaded_routers})

async def start_polling():
    await bot.delete_webhook(drop_pending_updates=True)
    await set_default_commands()
    logger.info("Commands & menu set. Polling...")
    await dp.start_polling(bot)

async def start_http():
    app = web.Application()
    app.router.add_post("/api/auth/register", register)
    app.router.add_post("/api/auth/login", login)
    app.router.add_get(HEALTH_PATH, health_handler)
    app.router.add_get("/", index_handler)
    app.router.add_get("/api/profile", api_profile)
    app.router.add_get("/api/last-compare", api_last_compare)
    app.router.add_get('/debug/routers', debug_routers)
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
















