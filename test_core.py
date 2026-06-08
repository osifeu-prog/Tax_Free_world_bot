import asyncio, os
from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.memory import MemoryStorage

# ייבוא הראוטרים
from bot.routers.start import router as start_router
from bot.routers.menu import router as menu_router
from bot.routers.help import router as help_router
from bot.routers.crypto import router as crypto_router
from bot.routers.vision import router as vision_router
from bot.routers.qr import router as qr_router
from bot.routers.budget import router as budget_router
from bot.routers.academy import router as academy_router
from bot.routers.report import router as report_router
from bot.routers.health import router as health_router

dp = Dispatcher(storage=MemoryStorage())
dp.include_router(start_router)
dp.include_router(menu_router)
dp.include_router(help_router)
dp.include_router(crypto_router)
dp.include_router(vision_router)
dp.include_router(qr_router)
dp.include_router(budget_router)
dp.include_router(academy_router)
dp.include_router(report_router)
dp.include_router(health_router)

class MockMessage:
    def __init__(self, text, user_lang="he"):
        self.text = text
        self.from_user = type('obj', (object,), {'id': 224223270, 'language_code': user_lang, 'is_bot': False, 'first_name': 'Test'})
        self.chat = type('obj', (object,), {'id': 224223270, 'type': 'private'})
        self._answer = None
    async def answer(self, text, **kwargs):
        self._answer = text

async def test(cmd, lang="he", keywords=[]):
    msg = MockMessage(cmd, lang)
    # שימוש בטוקן האמיתי
    bot = Bot(os.getenv("BOT_TOKEN"))
    try:
        await dp.feed_update(bot, {"message": msg, "update_id": 1})
    except Exception as e:
        return False, str(e)
    text = msg._answer or ""
    if not text:
        return False, "No response"
    if text.startswith("[") and text.endswith("]"):
        return False, f"Missing translation: {text}"
    for kw in keywords:
        if kw not in text:
            return False, f"Missing '{kw}'"
    return True, text[:100]

async def main():
    tests = [
        ("/start", ["ברוכים", "TON"]),
        ("/menu", ["תפריט", "חיסכון"]),
        ("/help", ["פקודות", "חיסכון"]),
        ("/crypto", ["קריפטו", "בלוקצ'יין"]),
        ("/vision", ["חזון", "TON"]),
        ("/qr", ["הפניה"]),
        ("/budget", ["תקציב"]),
        ("/academy", ["אקדמיה"]),
        ("/report", ["דוח"]),
        ("/health", ["Health"]),
    ]
    passed = 0
    for cmd, keys in tests:
        ok, info = await test(cmd, "he", keys)
        if ok:
            print(f"✅ {cmd}")
            passed += 1
        else:
            print(f"❌ {cmd}  {info}")
    print(f"\nTests: {passed}/{len(tests)} passed")

    # i18n
    print("\n🌐 i18n check (English):")
    for cmd in ["/start", "/menu", "/help"]:
        ok, info = await test(cmd, "en")
        if ok:
            print(f"  ✅ {cmd}  translated")
        else:
            print(f"  ⚠️ {cmd}  {info}")

asyncio.run(main())
