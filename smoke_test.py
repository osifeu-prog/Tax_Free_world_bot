import sys
import requests
import time

BOT_TOKEN = sys.argv[1] if len(sys.argv) > 1 else input("Enter BOT_TOKEN: ")
CHAT_ID = int(sys.argv[2]) if len(sys.argv) > 2 else 224223270
BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

def send(cmd):
    requests.post(f"{BASE_URL}/sendMessage", json={"chat_id": CHAT_ID, "text": cmd, "parse_mode": "HTML"})

def test(cmd):
    print(f"🧪 Testing: {cmd}")
    send(cmd)
    time.sleep(2)
    print(f"   ✅ {cmd} sent")

tests = [
    "/start", "/menu", "/profile", "/help", "/pension",
    "/budget", "/donate", "/academy", "/crypto", "/vision",
    "/setwallet", "/addexpense", "/setincome", "/familygroup"
]

print("🚀 Starting smoke tests...")
for t in tests:
    test(t)
print("\n✅ Smoke test finished. Check the bot manually.")
