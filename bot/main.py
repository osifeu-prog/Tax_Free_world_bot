# -*- coding: utf-8 -*-
import asyncio, os, pkgutil, importlib
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand, BotCommandScopeDefault, WebAppInfo, MenuButtonWebApp
from aiohttp import web
from bot.config import settings
from aiogram import BaseMiddleware
from aiogram.types import Message

class AdminMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Message, data):
        if event.text and event.text.split()[0] in ['/addadmin', '/removeadmin', '/setpassword', '/admin', '/export', '/debug', '/approve', '/deny', '/negotiations', '/addgroup', '/groups', '/setrole']:
            if str(event.from_user.id) not in (settings.admin_ids or ''):
                await event.answer("? ????? ?? ????? ??????? ????.\n??? /requestadmin ???? ??????.")
                return
        return await handler(event, data)
from aiogram import BaseMiddleware
from aiogram.types import Message

class AdminMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Message, data):
        if event.text and event.text.split()[0] in ['/addadmin', '/removeadmin', '/setpassword', '/admin', '/export', '/debug', '/approve', '/deny', '/negotiations', '/addgroup', '/groups', '/setrole']:
            if str(event.from_user.id) not in (settings.admin_ids or ''):
                await event.answer("? ????? ?? ????? ??????? ????.\n??? /requestadmin ???? ??????.")
                return
        return await handler(event, data)
from bot.api.email_routes import register, login
from bot.utils.logger import logger
from bot.database.models import Base
from bot.database.session import engine
import bot.routers as routers_pkg

HEALTH_PATH = "/health"

bot = Bot(token=settings.bot_token)
dp = Dispatcher()
dp.message.middleware(AdminMiddleware())
dp.message.middleware(AdminMiddleware())

# ????? ?????? ????? ???????
loaded_routers = []
for importer, modname, ispkg in pkgutil.iter_modules(routers_pkg.__path__):
    try:
        module = importlib.import_module(f"bot.routers.{modname}")
        if hasattr(module, 'router'):
            dp.include_router(module.router)
            loaded_routers.append(modname)
            logger.info(f"? Router {modname} loaded")
    except Exception as e:
        logger.error(f"? Failed to load router {modname}: {e}")

async def set_default_commands():
    commands = [
        BotCommand(command="start", description="?? ????"),
        BotCommand(command="compare", description="?????? ?????"),
        BotCommand(command="budget", description="?????? ?????"),
        BotCommand(command="profile", description="?????? ?????"),
        BotCommand(command="expenses", description="??? ???????"),
        BotCommand(command="addexpense", description="???? ?????"),
        BotCommand(command="setincome", description="???? ?????"),
        BotCommand(command="delexpense", description="??? ?????"),
        BotCommand(command="wallet", description="???? TON"),
        BotCommand(command="why", description="??? TON?"),
        BotCommand(command="business", description="??????"),
        BotCommand(command="crypto", description="?? ?? ??????"),
        BotCommand(command="cbdc", description="?? ?? CBDC"),
        BotCommand(command="decentral", description="????? ??? ????????"),
        BotCommand(command="socio", description="??????????"),
        BotCommand(command="anti", description="?????????? ??? ??????"),
        BotCommand(command="edu", description="?????, ?????, ?????"),
        BotCommand(command="academy_extended", description="????????, NFT, ????? ????"),
        BotCommand(command="academy_nft", description="NFT-????"),
        BotCommand(command="academy_dao", description="?????? DAO"),
        BotCommand(command="faq", description="????? ??????"),
        BotCommand(command="tip", description="??? ????"),
        BotCommand(command="stats", description="??????????"),
        BotCommand(command="top", description="??? ???????"),
        BotCommand(command="ref", description="??? ?????"),
        BotCommand(command="contact", description="??? ???"),
        BotCommand(command="id", description="?????"),
        BotCommand(command="daily", description="????? ????"),
        BotCommand(command="mydata", description="??????? ???"),
        BotCommand(command="gift", description="???? ?????"),
        BotCommand(command="help", description="????"),
        BotCommand(command="admin", description="???? ?????"),
        BotCommand(command="debug", description="????? ?????"),
        BotCommand(command="miniapp", description="?????? ???????"),
        BotCommand(command="keyboard", description="?????"),
        BotCommand(command="hide", description="???? ?????"),
        BotCommand(command="export", description="????? ?????"),
        BotCommand(command="donate", description="?????"),
        BotCommand(command="feedback", description="?????"),
        BotCommand(command="whyus", description="??? ?????"),
        BotCommand(command="familyguide", description="?????? ??????"),
        BotCommand(command="menu", description="????? ????"),
        BotCommand(command="architecture", description="?????????? ??????"),
        BotCommand(command="household", description="????? ????? ????"),
        BotCommand(command="ai", description="??? ?? ?????"),
        BotCommand(command="ask", description="??? ????"),
        BotCommand(command="addadmin", description="???? ????"),
        BotCommand(command="login", description="?????"),
        BotCommand(command="setpassword", description="??? ?????"),
        BotCommand(command="requestadmin", description="??? ????? ?????"),
        BotCommand(command="removeadmin", description="??? ????"),
        BotCommand(command="quiz", description="?????"),
    ]
    await bot.set_my_commands(commands, scope=BotCommandScopeDefault())
    await bot.set_chat_menu_button(
        menu_button=MenuButtonWebApp(
            text="?????? ???????",
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


