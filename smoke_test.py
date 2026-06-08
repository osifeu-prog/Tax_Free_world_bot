import asyncio

class MockMsg:
    def __init__(self, text, lang="he"):
        self.text = text
        self.from_user = type('u',(),{
            'id':224223270,'language_code':lang,'is_bot':False,'first_name':'Test'
        })
        self.chat = type('c',(),{'id':224223270,'type':'private'})
        self._ans = ""
    async def answer(self, txt, **kw):
        self._ans = txt
    async def answer_photo(self, photo, caption="", **kw):
        self._ans = caption or "[photo]"

async def main():
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
    from bot.routers.language import cmd_language
    from bot.routers.familygroup import cmd_familygroup
    from bot.routers.pension import cmd_pension
    from bot.routers.setwallet import cmd_setwallet
    from bot.routers.family_finance import cmd_setincome, cmd_addexpense, cmd_mysavings
    from bot.routers.donate import cmd_donate
    from bot.routers.morning import cmd_morning

    tests = [
        (cmd_start, "/start", ["התחל","menu"]),
        (cmd_menu, "/menu", ["חיסכון","פנסיה"]),
        (cmd_help, "/help", ["עזרה","חיסכון"]),
        (cmd_crypto, "/crypto", ["קריפטו","בלוקצ'יין"]),
        (cmd_vision, "/vision", ["חזון","TON"]),
        (cmd_qr, "/qr", ["הפניה"]),
        (cmd_budget, "/budget", ["השתמש"]),
        (cmd_academy, "/academy", ["בחר"]),
        (cmd_report, "/report", ["משתמשים","הפניות"]),
        (cmd_health, "/health", ["Health","Uptime"]),
        (cmd_language, "/language", ["שפה"]),
        (cmd_familygroup, "/familygroup", ["קבוצה","בוט"]),
        (cmd_pension, "/pension", ["עובד","מדינה"]),
        (cmd_setwallet, "/setwallet", ["ארנק","TON"]),
        (cmd_setincome, "/setincome", ["השתמש"]),
        (cmd_addexpense, "/addexpense", ["השתמש"]),
        (cmd_mysavings, "/mysavings", ["הכנסה"]),
        (cmd_donate, "/donate", ["תמכו"]),
        (cmd_morning, "/morning", ["צעדים","smoke_test"]),
    ]

    ok = 0
    for handler, cmd, keys in tests:
        msg = MockMsg(cmd)
        try:
            await handler(msg)
        except Exception as e:
            print(f"❌ {cmd}  {e}")
            continue
        text = msg._ans
        if not text:
            print(f"❌ {cmd}  No output")
            continue
        if all(k in text for k in keys):
            print(f"✅ {cmd}")
            ok += 1
        else:
            missing = [k for k in keys if k not in text]
            print(f"❌ {cmd}  Missing: {missing} (got: {text[:80]})")
    print(f"\n✅ {ok}/{len(tests)} passed")

asyncio.run(main())


