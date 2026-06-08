import asyncio, os, sys

# הוסף את תיקיית הפרויקט לנתיב
sys.path.insert(0, r"D:\PROJ\TON-Israel")

from aiogram import Bot, Dispatcher
from aiogram.types import Message, Chat, User
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command
import bot.routers as routers_pkg
import pkgutil, importlib

# טען כל הראוטרים
dp = Dispatcher(storage=MemoryStorage())
for importer, modname, ispkg in pkgutil.iter_modules(routers_pkg.__path__):
    module = importlib.import_module(f"bot.routers.{modname}")
    if hasattr(module, 'router'):
        dp.include_router(module.router)

# סימולציית משתמש
class MockUser(User):
    def __init__(self, id=224223270, language="he"):
        super().__init__(id=id, is_bot=False, first_name="Test")
        self._language = language
    @property
    def language_code(self):
        return self._language

class MockMessage(Message):
    def __init__(self, text, user_lang="he"):
        self.text = text
        self.from_user = MockUser(language=user_lang)
        self.chat = Chat(id=224223270, type="private")
        self._answer = None
    async def answer(self, text, **kwargs):
        self._answer = text
    async def reply(self, text, **kwargs):
        self._answer = text

async def test_command(cmd: str, lang="he", expected_keywords=[]):
    msg = MockMessage(cmd, user_lang=lang)
    # הפעל את ה-dispatcher עם ה-message
    try:
        await dp.feed_update(Bot("dummy"), {"message": msg, "update_id": 1})
    except Exception as e:
        return False, f"Exception: {e}"
    text = msg._answer or ""
    if not text:
        return False, "No response"
    # בדוק תרגום חסר
    if text.startswith("[") and text.endswith("]"):
        return False, f"Missing translation: {text}"
    # בדוק מילות מפתח
    for kw in expected_keywords:
        if kw not in text:
            return False, f"Missing keyword: '{kw}'"
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
        ("/health", ["Health", "Uptime"]),
    ]

    passed = 0
    for cmd, keywords in tests:
        ok, detail = await test_command(cmd, "he", keywords)
        if ok:
            print(f"✅ {cmd}")
            passed += 1
        else:
            print(f"❌ {cmd}  {detail}")

    # i18n check  אנגלית
    print("\n🌐 i18n check (English):")
    for cmd in ["/start", "/menu", "/help"]:
        ok, detail = await test_command(cmd, "en")
        if ok:
            print(f"  ✅ {cmd}  translated")
        else:
            print(f"  ⚠️ {cmd}  {detail}")

    print(f"\nTests: {passed}/{len(tests)} passed")

asyncio.run(main())
