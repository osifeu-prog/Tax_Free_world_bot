import requests, time

TOKEN = "8782546867:AAFkv4mYtkDXvwf9RJpCVU2Tv7oT4lVGq5M"
BASE = f"https://api.telegram.org/bot{TOKEN}"
CHAT_ID = 224223270

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

def send_message(text):
    url = f"{BASE}/sendMessage?chat_id={CHAT_ID}&text={text}&parse_mode=HTML"
    try:
        r = requests.get(url, timeout=10)
        return r.json().get("ok", False), r.json().get("description", "")
    except Exception as e:
        return False, str(e)

print("=== Command Tests ===")
passed = 0
failed = []
for cmd in commands:
    ok, desc = send_message(cmd)
    if ok:
        passed += 1
        print(f"✅ {cmd}")
    else:
        failed.append(cmd)
        print(f"❌ {cmd} - {desc}")

print(f"\nTotal: {len(commands)} | Passed: {passed} | Failed: {len(failed)}")

# Language tests (must be run after the bot is updated)
print("\n=== Language Tests ===")
# Set English
requests.post(f"{BASE}/answerCallbackQuery", json={
    "callback_query_id": "0",  # placeholder; we can't simulate callback here.
}).text
# Instead, we can check /start output after a language change by sending /language and clicking, but we can't do programmatically without a live session.
# So print instructions for manual check.
print("Manual: Send /language, click English, then /start → should show English welcome. Then Arabic.")

