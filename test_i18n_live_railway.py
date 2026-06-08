import os
os.environ.setdefault("BOT_TOKEN", "dummy_for_test")  # למנוע קריסה ב-config

import asyncio, requests, json
from sqlalchemy import select
from bot.database.session import async_session
from bot.database.models import User

TOKEN = "8782546867:AAFkv4mYtkDXvwf9RJpCVU2Tv7oT4lVGq5M"
BASE = f"https://api.telegram.org/bot{TOKEN}"
CHAT_ID = 224223270
LANGUAGES = ["he", "en", "ar", "ru"]
COMMANDS = ["/start", "/menu", "/academy", "/help"]

async def set_language(telegram_id, lang):
    async with async_session() as session:
        user = (await session.execute(select(User).where(User.telegram_id == telegram_id))).scalar_one_or_none()
        if user:
            user.language = lang
        else:
            session.add(User(telegram_id=telegram_id, language=lang))
        await session.commit()

async def test_language(lang):
    await set_language(CHAT_ID, lang)
    for cmd in COMMANDS:
        url = f"{BASE}/sendMessage?chat_id={CHAT_ID}&text={cmd}&parse_mode=HTML"
        r = requests.get(url, timeout=10)
        data = r.json()
        if data.get("ok"):
            text = data["result"].get("text", "")
            if "[key]" in text or "Unknown" in text:
                print(f"❌ {lang}/{cmd}: missing key")
            else:
                print(f"✅ {lang}/{cmd}: OK ({len(text)} chars)")
        else:
            print(f"❌ {lang}/{cmd}: API error {data.get('description')}")
    await set_language(CHAT_ID, "he")

async def main():
    for lang in LANGUAGES:
        await test_language(lang)

asyncio.run(main())
