import requests, json, time

BASE = "https://api.telegram.org/bot8782546867:AAFkv4mYtkDXvwf9RJpCVU2Tv7oT4lVGq5M"
CHAT_ID = 224223270  # Osif (admin)

commands = {
    "/start": {"expect": ["ברוכים", "TON Israel", "menu"]},
    "/menu": {"expect": ["תפריט", "חיסכון", "אקדמיה"]},
    "/help": {"expect": ["פקודות", "חיסכון", "אקדמיה"]},
    "/crypto": {"expect": ["קריפטו", "בלוקצ'יין"]},
    "/cbdc": {"expect": ["CBDC"]},
    "/decentral": {"expect": ["ביזור"]},
    "/socio": {"expect": ["סוציוקרטיה"]},
    "/anti": {"expect": ["שחיתות"]},
    "/edu": {"expect": ["חינוך"]},
    "/academy_extended": {"expect": ["NFT", "ביזוריות"]},
    "/academy_nft": {"expect": ["NFT"]},
    "/academy_dao": {"expect": ["DAO"]},
    "/vision": {"expect": ["חזון", "TON Israel"]},
    "/spark": {"expect": ["SLH_Spark_AI_BOT"]},
    "/academia": {"expect": ["SLH_Academia_bot"]},
    "/ref": {"expect": ["הפניה"]},
    "/qr": {"expect": ["הפניה"]},
    "/stats": {"expect": ["סטטיסטיקות"]},
    "/top": {"expect": ["מובילים"]},
    "/tip": {"expect": ["טיפ"]},
    "/contact": {"expect": ["קשר"]},
    "/faq": {"expect": ["שאלות"]},
    "/daily": {"expect": ["סיכום"]},
    "/mydata": {"expect": ["נתונים"]},
    "/gift": {"expect": ["מתנה"]},
    "/miniapp": {"expect": ["מחשבון"]},
    "/keyboard": {"expect": ["מקלדת"]},
    "/hide": {"expect": ["מקלדת"]},
    "/ask": {"expect": ["שאל"]},
    "/feedback": {"expect": ["דיווח"]},
    "/quiz": {"expect": ["חידון"]},
    "/wallet": {"expect": ["ארנק", "TON"]},
    "/why": {"expect": ["TON"]},
    "/business": {"expect": ["עסקים"]},
    "/budget": {"expect": ["תקציב"]},
    "/profile": {"expect": ["פרופיל"]},
    "/expenses": {"expect": ["הוצאות"]},
    "/addexpense": {"expect": ["הוסף"]},
    "/setincome": {"expect": ["הכנסה"]},
    "/delexpense": {"expect": ["מחק"]},
    "/household": {"expect": ["משק בית"]},
    "/requestadmin": {"expect": ["מנהל"]},
    "/addadmin": {"expect": ["מנהל"]},
    "/login": {"expect": ["התחבר"]},
    "/setpassword": {"expect": ["סיסמה"]},
    "/removeadmin": {"expect": ["מנהל"]},
    "/admin": {"expect": ["אדמין"]},
    "/export": {"expect": ["ייצוא"]},
    "/debug": {"expect": ["סטטוס"]},
    "/addgroup": {"expect": ["קבוצה"]},
    "/groups": {"expect": ["קבוצות"]},
    "/id": {"expect": ["זיהוי"]},
    "/health": {"expect": ["Health"]},
    "/seed_courses": {"expect": ["קורסים"]},
    "/language": {"expect": ["שפה"]},
    "/translations": {"expect": ["תרגומים"]},
    "/myrole": {"expect": ["תפקיד"]},
    "/setrole": {"expect": ["תפקיד"]},
    "/seed_kg": {"expect": ["Knowledge Graph"]},
    "/report": {"expect": ["דוח"]},
    "/xp": {"expect": ["XP"]},
    "/profile_citizen": {"expect": ["פרופיל"]},
    "/compare": {"expect": ["עמלות", "חיסכון"]},
}

passed = 0
failed = 0

for cmd, check in commands.items():
    try:
        r = requests.get(BASE + "/sendMessage", params={"chat_id": CHAT_ID, "text": cmd}, timeout=30)
        if r.status_code == 200:
            resp = r.json()
            text = resp.get("result", {}).get("text", "")
            if any(exp in text for exp in check["expect"]):
                print(f"✅ {cmd}")
                passed += 1
            else:
                print(f"⚠️ {cmd}  unexpected response: {text[:80]}...")
                failed += 1
        else:
            print(f"❌ {cmd} (HTTP {r.status_code})")
            failed += 1
    except Exception as e:
        print(f"❌ {cmd} ({e})")
        failed += 1
    time.sleep(0.5)

print(f"\nTotal: {len(commands)} | Passed: {passed} | Failed: {failed}")
