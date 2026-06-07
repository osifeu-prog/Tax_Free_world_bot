import requests, sys

BASE = "https://api.telegram.org/bot8782546867:AAFkv4mYtkDXvwf9RJpCVU2Tv7oT4lVGq5M"
commands = [
    "/start", "/compare", "/wallet", "/why", "/business", "/budget", "/profile", "/expenses",
    "/addexpense", "/setincome", "/delexpense", "/household",
    "/crypto", "/cbdc", "/decentral", "/socio", "/anti", "/edu",
    "/academy_extended", "/academy_nft", "/academy_dao", "/vision", "/spark", "/academia",
    "/ref", "/qr", "/stats", "/top", "/tip", "/contact", "/faq", "/daily", "/mydata", "/gift",
    "/miniapp", "/keyboard", "/hide", "/ask", "/feedback", "/help", "/quiz", "/menu",
    "/requestadmin", "/addadmin", "/login", "/setpassword", "/removeadmin",
    "/admin", "/export", "/debug", "/addgroup", "/groups", "/id"
]

passed = 0
failed = 0
for cmd in commands:
    try:
        r = requests.get(BASE + "/sendMessage", params={"chat_id": 224223270, "text": cmd}, timeout=10)
        if r.status_code == 200:
            print(f"✅ {cmd}")
            passed += 1
        else:
            print(f"❌ {cmd} ({r.status_code})")
            failed += 1
    except Exception as e:
        print(f"❌ {cmd} (Exception: {e})")
        failed += 1

print(f"\nTotal: {len(commands)} | Passed: {passed} | Failed: {failed}")
