import sys
import requests
import time

BOT_TOKEN = sys.argv[1] if len(sys.argv) > 1 else input("Token: ")
CHAT_ID = int(sys.argv[2]) if len(sys.argv) > 2 else 224223270
BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

def send(cmd):
    requests.post(f"{BASE_URL}/sendMessage", json={"chat_id": CHAT_ID, "text": cmd})

def test(cmd):
    print(f"Testing {cmd}")
    send(cmd)
    time.sleep(1.5)

tests = ["/start", "/profile", "/adde", "/expenses", "/addcategory", "/categories", "/addincome", "/incomes", "/menu"]
for t in tests:
    test(t)
print("✅ Smoke test done.")
