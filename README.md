# 🏙️ TON Israel Bot (@Tax_Free_world_bot)

בוט טלגרם רב-לשוני לחיסכון, פנסיה, אקדמיה, קהילה כלכלית מבוזרת  **ויוסלס AI**.

## 🚀 תכונות עיקריות
- 🤖 **יוסלס AI**  48 תגובות קיומיות, רולטה, QR, סטטיסטיקות
- 💰 **מחשבון חיסכון**  השוואת עמלות Bit vs PayBox vs TON
- 📊 **אשף פנסיה**  חישוב פנסיה תקציבית וצוברת
- 🎓 **אקדמיה**  קורסים בקריפטו, CBDC, ביזור, סוציוקרטיה
- 🏙️ **TON City**  דשבורד עירוני
- 🌐 **7 שפות**  עברית, English, Русский, العربية, Español, Français, יידיש
- 🎮 **Gamification**  `/daily` סטריק, `/top` לוח מובילים, `/ref` הפניות
- 💖 **Donate Flow**  7 שפות, כפתורי סכומים + TON
- 📊 **סטטיסטיקות אמת**  `/stats_useless`
- 🔴 **Broadcast**  כפתור אדום למי שלא לחץ 6 שעות
- 🛡️ **Rate Limiter**  2 בקשות/שנייה
- 📋 **73+ פקודות**

## 📦 טכנולוגיות
- Python 3.10 + Aiogram 3
- SQLite + Volume (Railway)
- aiohttp (HTTP Server)
- Redis (מטמון)
- Google Gemini API (AI)
- Railway (Deploy)

## 📂 מבנה
bot/
main.py
routers/
start.py, menu.py, useless.py, gamification.py, pension.py, donate.py, ...
services/
translation_service.py, useless_logger.py, ...
middlewares/
rate_limit.py
locales/
he.json, en.json, ru.json, ar.json, es.json, fr.json, yi.json
public/
landing/
index.html, miniapp.html


## 🔧 Deploy
```bash
git push
railway up --service Tax_Free_world_bot --detach
🧪 בדיקות

python test_all_commands.py <BOT_TOKEN> <CHAT_ID>
python test_suite.py
📊 סטטוס
✅ ליבה (start, menu, useless, pension, donate)

✅ DB + Redis

✅ 7 שפות (חלקי)

✅ Gamification

🚧 AI (Gemini)  בקרוב

🚧 Webhook  בקרוב

📞 קישורים
בוט

דף נחיתה

🛡️ רישיון
MIT
