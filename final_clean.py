import os

def write_clean(path, content):
    """כותב קובץ UTF-8 ללא BOM"""
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def clean_all():
    base = os.path.dirname(__file__)
    
    # --- main.py ---
    write_clean(os.path.join(base, 'bot', 'main.py'), '''import asyncio
import os
import pkgutil
import importlib
import time
from pathlib import Path

start_time = time.time()

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand, BotCommandScopeDefault, WebAppInfo, MenuButtonDefault
from aiohttp import web

from bot.config import settings
from bot.api.email_routes import register, login
from bot.utils.logger import logger
from bot.database.models import Base
from bot.database.session import engine
from bot.migrate_i18n import add_lang_columns
import bot.routers as routers_pkg

bot = Bot(token=settings.bot_token)
dp = Dispatcher()

# טעינה דינמית
loaded_routers = []
for _, modname, _ in pkgutil.iter_modules(routers_pkg.__path__):
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
        BotCommand(command="start", description="🚀 דף הבית"),
        BotCommand(command="menu", description="📋 תפריט ראשי"),
        BotCommand(command="pension", description="📊 פנסיה"),
        BotCommand(command="academy", description="🎓 אקדמיה"),
        BotCommand(command="city", description="🏙️ TON City"),
        BotCommand(command="market", description="📈 בורסה"),
        BotCommand(command="donate", description="💖 תרומה"),
        BotCommand(command="report", description="📊 דוח מערכת"),
        BotCommand(command="help", description="❔ עזרה"),
        BotCommand(command="ref", description="🔗 הפניה"),
        BotCommand(command="language", description="🌐 שפה"),
        BotCommand(command="miniapp", description="📱 מחשבון ויזואלי"),
    ]
    await bot.set_my_commands(commands, scope=BotCommandScopeDefault())
    await bot.set_chat_menu_button(menu_button=MenuButtonDefault())

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

async def start_polling():
    await bot.delete_webhook(drop_pending_updates=True)
    await set_default_commands()
    logger.info("🤖 Starting polling...")
    await dp.start_polling(bot)

async def main():
    await init_db()
    logger.info(f"🚀 Bot started in {time.time() - start_time:.2f}s")
    await asyncio.gather(start_polling(), start_http())

if __name__ == "__main__":
    asyncio.run(main())
''')

    # --- start.py ---
    write_clean(os.path.join(base, 'bot', 'routers', 'start.py'), '''from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from bot.database.session import async_session
from bot.database.models import User
from sqlalchemy import select
from bot.services.translation_service import translator

router = Router()

async def get_lang(user_id: int) -> str:
    async with async_session() as s:
        user = (await s.execute(select(User).where(User.telegram_id == user_id))).scalar_one_or_none()
        return user.language if user and user.language else "he"

@router.message(Command("start"))
async def cmd_start(msg: Message):
    lang = await get_lang(msg.from_user.id)
    name = msg.from_user.first_name or "חבר"
    welcome = translator.t(lang, "welcome_message", name=name)
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🇮🇱 עברית", callback_data="lang_he"), InlineKeyboardButton(text="🇬🇧 English", callback_data="lang_en")],
        [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru"), InlineKeyboardButton(text="🇸🇦 العربية", callback_data="lang_ar")],
        [InlineKeyboardButton(text="🇪🇸 Español", callback_data="lang_es"), InlineKeyboardButton(text="🇫🇷 Français", callback_data="lang_fr")],
        [InlineKeyboardButton(text="🇾🇮 יידיש", callback_data="lang_yi")],
        [InlineKeyboardButton(text="📱 מחשבון ויזואלי", callback_data="open_miniapp")],
        [InlineKeyboardButton(text="📋 תפריט מלא", callback_data="show_menu")]
    ])
    await msg.answer(welcome, parse_mode="HTML", reply_markup=kb)

@router.callback_query(F.data.startswith("lang_"))
async def set_language(callback: CallbackQuery):
    lang = callback.data.split("_")[1]
    uid = callback.from_user.id
    async with async_session() as session:
        user = (await session.execute(select(User).where(User.telegram_id == uid))).scalar_one_or_none()
        if user:
            user.language = lang
        else:
            session.add(User(telegram_id=uid, language=lang))
        await session.commit()
    await callback.message.edit_text(translator.t(lang, "welcome_message"), parse_mode="HTML")
    await callback.answer(f"✅ שפה שונתה ל-{lang}")

@router.callback_query(F.data == "show_menu")
async def show_full_menu(callback: CallbackQuery):
    from bot.routers.menu import cmd_menu
    await cmd_menu(callback.message)
    await callback.answer()
''')

    # --- menu.py ---
    write_clean(os.path.join(base, 'bot', 'routers', 'menu.py'), '''from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
router = Router()

@router.message(Command("menu"))
async def cmd_menu(msg: Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💰 חיסכון", callback_data="cmd_budget")],
        [InlineKeyboardButton(text="📊 פנסיה", callback_data="cmd_pension")],
        [InlineKeyboardButton(text="🎓 אקדמיה", callback_data="cmd_academy")],
        [InlineKeyboardButton(text="🏙️ TON City", callback_data="cmd_city")],
        [InlineKeyboardButton(text="🔗 הפניה", callback_data="cmd_ref")],
        [InlineKeyboardButton(text="💖 תרומה", callback_data="cmd_donate")],
        [InlineKeyboardButton(text="❔ עזרה", callback_data="cmd_help")]
    ])
    await msg.answer("📋 <b>תפריט ראשי TON Israel</b>", parse_mode="HTML", reply_markup=kb)
''')

    print("✅ כל הקבצים נכתבו מחדש ללא BOM")

if __name__ == "__main__":
    clean_all()
