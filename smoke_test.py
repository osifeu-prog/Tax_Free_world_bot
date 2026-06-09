import requests, time

BOT_TOKEN = "8782546867:AAFxsqjad8RHCLjRcLpJp8WJ_uQ_mQnHKJc"
BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"
CHAT_ID = 224223270  # ה-ID שלך

def send(msg):
    return requests.post(f"{BASE_URL}/sendMessage", json={"chat_id": CHAT_ID, "text": msg}).json()

def get_bot_reply():
    time.sleep(2)  # תן לבוט זמן לעבד
    resp = requests.get(f"{BASE_URL}/getUpdates", params={"offset": -1, "limit": 1}).json()
    if resp["ok"] and resp["result"]:
        last_msg = resp["result"][-1]
        if "message" in last_msg and "text" in last_msg["message"]:
            return last_msg["message"]["text"]
    return ""

def test(cmd, keywords):
    send(cmd)
    reply = get_bot_reply()
    ok = all(kw in reply for kw in keywords)
    print(f"{'✅' if ok else '❌'} {cmd}  {'Found' if ok else 'Missing: ' + str(keywords)} [{reply[:60]}]")

# /pension דורש בדיקת כפתורים
def test_pension():
    send("/pension")
    time.sleep(2)
    resp = requests.get(f"{BASE_URL}/getUpdates", params={"offset": -1, "limit": 1}).json()
    if resp["ok"] and resp["result"]:
        last = resp["result"][-1]
        if "message" in last and "reply_markup" in last["message"]:
            for row in last["message"]["reply_markup"]["inline_keyboard"]:
                for btn in row:
                    if "עובד מדינה" in btn["text"]:
                        print("✅ /pension")
                        return
    print("❌ /pension  Missing: ['עובד מדינה']")

# רשימת הבדיקות
test("/start", ["ברוכים"])
test("/menu", ["תפריט"])
test("/help", ["עזרה"])
test("/crypto", ["קריפטו"])
test("/vision", ["חזון"])
test_pension()
test("/budget", ["תקציב"])
test("/academy", ["בחר"])
test("/report", ["הפניות"])
test("/health", ["תקין"])
test("/language", ["בחר"])
test("/familygroup", ["צור"])
test("/setwallet", ["הארנק"])
test("/setincome", ["הכנסה"])
test("/addexpense", ["הוצאה"])
test("/mysavings", ["חיסכון"])
test("/donate", ["תמכו"])
test("/morning", ["בוקר"])
