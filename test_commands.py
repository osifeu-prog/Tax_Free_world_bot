import asyncio, sys

class MockMessage:
    def __init__(self, text, user_lang="he"):
        self.text = text
        self.from_user = type('u', (), {
            'id': 224223270,
            'language_code': user_lang,
            'is_bot': False,
            'first_name': 'Test'
        })
        self.chat = type('c', (), {'id': 224223270, 'type': 'private'})
        self._answer = None

    async def answer(self, text, **kwargs):
        self._answer = text

async def run():
    # ייבוא הפונקציות ישירות
    from bot.routers.start import cmd_start
    from bot.routers.menu import cmd_menu
    from bot.routers.help import cmd_help
    from bot.routers.crypto import cmd_crypto
    from bot.routers.vision import cmd_vision
    from bot.routers.qr import cmd_qr
    from bot.routers.budget import cmd_budget
    from bot.routers.academy import cmd_academy
    from bot.routers.report import cmd_report
    from bot.routers.health import cmd_health

    tests = [
        (cmd_start, "/start", ["ברוכים", "TON"]),
        (cmd_menu, "/menu", ["תפריט", "חיסכון"]),
        (cmd_help, "/help", ["פקודות", "חיסכון"]),
        (cmd_crypto, "/crypto", ["קריפטו", "בלוקצ'יין"]),
        (cmd_vision, "/vision", ["חזון", "TON"]),
        (cmd_qr, "/qr", ["הפניה"]),
        (cmd_budget, "/budget", ["תקציב"]),
        (cmd_academy, "/academy", ["אקדמיה"]),
        (cmd_report, "/report", ["דוח"]),
        (cmd_health, "/health", ["Health"]),
    ]

    passed = 0
    for handler, cmd, keywords in tests:
        msg = MockMessage(cmd, "he")
        try:
            await handler(msg)
        except Exception as e:
            print(f"❌ {cmd}  Exception: {e}")
            continue
        text = msg._answer or ""
        if not text:
            print(f"❌ {cmd}  No response")
            continue
        if text.startswith("[") and text.endswith("]"):
            print(f"❌ {cmd}  Missing translation")
            continue
        if not all(kw in text for kw in keywords):
            missing = [kw for kw in keywords if kw not in text]
            print(f"❌ {cmd}  Missing keywords: {missing}")
            continue
        print(f"✅ {cmd}")
        passed += 1

    # i18n
    print("\n🌐 i18n check (English):")
    for handler, cmd in [(cmd_start, "/start"), (cmd_menu, "/menu"), (cmd_help, "/help")]:
        msg = MockMessage(cmd, "en")
        await handler(msg)
        text = msg._answer or ""
        if text and not (text.startswith("[") and text.endswith("]")):
            print(f"  ✅ {cmd}  translated")
        else:
            print(f"  ⚠️ {cmd}  not translated")

    print(f"\nTests: {passed}/{len(tests)} passed")

asyncio.run(run())

