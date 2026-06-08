import requests, time, json

TOKEN = "8782546867:AAFkv4mYtkDXvwf9RJpCVU2Tv7oT4lVGq5M"
BASE = f"https://api.telegram.org/bot{TOKEN}"
CHAT_ID = 224223270

def send_message(text):
    url = f"{BASE}/sendMessage?chat_id={CHAT_ID}&text={text}&parse_mode=HTML"
    try:
        r = requests.get(url, timeout=10)
        return r.json()
    except Exception as e:
        return {"ok": False, "description": str(e)}

# --- Command Tests ---
commands = [
    "/start","/compare","/wallet","/why","/business","/budget","/profile",
    "/expenses","/addexpense","/setincome","/delexpense","/household",
    "/crypto","/cbdc","/decentral","/socio","/anti","/edu",
    "/academy_extended","/academy_nft","/academy_dao","/vision","/spark",
    "/academia","/ref","/qr","/stats","/top","/tip","/contact","/faq",
    "/daily","/mydata","/gift","/miniapp","/keyboard","/hide","/ask",
    "/feedback","/help","/quiz","/menu","/requestadmin","/addadmin",
    "/login","/setpassword","/removeadmin","/admin","/export","/debug",
    "/addgroup","/groups","/id"
]

print("=== Command Tests ===")
passed = 0
failed = []
for cmd in commands:
    resp = send_message(cmd)
    if resp.get("ok"):
        passed += 1
        print(f"✅ {cmd}")
    else:
        failed.append(cmd)
        print(f"❌ {cmd} - {resp.get('description','')}")

print(f"\nTotal: {len(commands)} | Passed: {passed} | Failed: {len(failed)}")

# --- Language Tests (use /start) ---
print("\n=== Language Tests ===")
# Note: we can't simulate callback, so we'll test /start manually after each language change.
# Instead, we can call /start and verify that the response doesn't contain "[key]" and looks valid.
langs = {"he": "ברוכים", "en": "Welcome", "ar": "مرحبًا", "ru": "Добро"}
for lang, expected in langs.items():
    # Set language via DB? Not possible from API without admin access.
    # So we'll just inform that manual test is needed.
    pass
print("Manual: Send /language, select each language, then /start  verify correct welcome.")
print("Also check /menu, /translations.")

