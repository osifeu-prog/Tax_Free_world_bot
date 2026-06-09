# 🏙️ TON Israel Bot (@Tax_Free_world_bot)

בוט טלגרם רב-לשוני לחיסכון, פנסיה, אקדמיה וקהילה כלכלית מבוזרת.

## 🚀 תכונות
- 💰 **מחשבון חיסכון**  השוואת עמלות Bit vs PayBox vs TON
- 📊 **אשף פנסיה**  חישוב פנסיה תקציבית וצוברת
- 🎓 **אקדמיה**  קורסים בקריפטו, CBDC, ביזור, סוציוקרטיה
- 🏙️ **TON City**  דשבורד עירוני
- 🌐 **7 שפות**  עברית, English, Русский, العربية, Español, Français, יידיש

## 📦 טכנולוגיות
- Python 3.10 + Aiogram 3
- SQLite + Volume (Railway)
- aiohttp (HTTP Server)
- Redis (מטמון)
- Railway (Deploy)

## 📂 מבנה
bot/
main.py
config.py
routers/
start.py, menu.py, pension.py, ...
services/
translation_service.py, ...
locales/
he.json, en.json, ru.json, ar.json, ...
public/
landing/
index.html, miniapp.html


## 🔧 Deploy
```bash
git push
railway up --service Tax_Free_world_bot --detach
🧪 בדיקות
/start  7 שפות + כפתורים

/menu  תפריט כפתורים

/pension  אשף פנסיה

/city  דשבורד

/report  דוח מערכת

/db_test  בדיקת DB

📊 סטטוס
✅ ליבה (start, menu, pension)

✅ DB + Redis

✅ 7 שפות (חלקי)

🚧 Gamification (בקרוב)

🚧 Mini App (בקרוב)

🔒 משתני סביבה (Railway)
BOT_TOKEN, ADMIN_IDS, GEMINI_API_KEY, REDIS_URL, DATABASE_URL
📞 קישורים
בוט

דף נחיתה

🛡️ רישיון
MIT
