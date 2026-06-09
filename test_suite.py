import json, os, sys

errors = 0
warnings = 0  # שגיאות "מותרות" (Settings / DB מקומי)

def ok(msg):
    print(f"  ✅ {msg}")

def fail(msg):
    global errors
    errors += 1
    print(f"  ❌ {msg}")

def warn(msg):
    global warnings
    warnings += 1
    print(f"  ⚠️  {msg}")

print("=== JSON Tests ===")
for lang in ['he', 'en', 'ru', 'ar', 'es', 'fr', 'yi']:
    path = f'bot/locales/{lang}.json'
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        ok(f'{lang}.json loaded ({len(data)} keys)')
    except Exception as e:
        fail(f'{lang}.json: {e}')

print("\n=== Router Tests ===")
import pkgutil, importlib, bot.routers
for _, modname, _ in pkgutil.iter_modules(bot.routers.__path__):
    try:
        importlib.import_module(f'bot.routers.{modname}')
        ok(f'Router: {modname}')
    except Exception as e:
        if 'Settings' in str(e) or 'bot_token' in str(e):
            warn(f'Router {modname} (Settings missing - OK)')
        else:
            fail(f'Router {modname}: {str(e)[:80]}')

print("\n=== Translation Service ===")
try:
    from bot.services.translation_service import translator
    for lang in ['he', 'en', 'ar']:
        txt = translator.t(lang, 'welcome_message')
        ok(f'translate {lang}: {txt[:40]}...')
except Exception as e:
    fail(f'translation_service: {e}')

print("\n=== DB Test (optional) ===")
try:
    import asyncio
    from sqlalchemy import text
    from bot.database.session import engine
    async def test():
        async with engine.begin() as conn:
            tables = await conn.run_sync(lambda c: [row[0] for row in c.execute(text("SELECT name FROM sqlite_master WHERE type='table'")).fetchall()])
            ok(f'DB: {len(tables)} tables')
            count = await conn.run_sync(lambda c: c.execute(text("SELECT COUNT(*) FROM users")).fetchone()[0])
            ok(f'Users: {count}')
    asyncio.get_event_loop().run_until_complete(test())
except Exception as e:
    warn(f'DB local not available (OK on Railway): {str(e)[:60]}')

print(f'\n{"="*40}')
print(f'Results: {errors} errors, {warnings} warnings')
if errors:
    print(f'❌ {errors} REAL ERRORS (must fix)')
    sys.exit(1)
else:
    print('✅ ALL CRITICAL TESTS PASSED')
    sys.exit(0)
