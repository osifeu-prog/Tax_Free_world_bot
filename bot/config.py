import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///bot/database/data/bot.db")
ADMIN_IDS = os.getenv("ADMIN_IDS", "[224223270]")
