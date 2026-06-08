import requests, time

TOKEN = "8782546867:AAFkv4mYtkDXvwf9RJpCVU2Tv7oT4lVGq5M"
BASE = f"https://api.telegram.org/bot{TOKEN}"
CHAT_ID = 224223270  # <-- עדכן למספר שלך

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

total = len(commands)
passed = 0
failed = []
start_time = time.time()

for cmd in commands:
    url = f"{BASE}/sendMessage?chat_id={CHAT_ID}&text={cmd}"
    try:
        r = requests.get(url, timeout=5)
        if r.json().get("ok"):
            passed += 1
            print(f"✅ {cmd}")
        else:
            failed.append(cmd)
            print(f"❌ {cmd} - {r.json().get('description','unknown')}")
    except Exception as e:
        failed.append(cmd)
        print(f"❌ {cmd} - exception {e}")

elapsed = time.time() - start_time
print(f"\n{'='*30}")
print(f"Total: {total} | Passed: {passed} | Failed: {len(failed)}")
print(f"Time: {elapsed:.1f}s")
if failed:
    print(f"Failures: {', '.join(failed)}")
