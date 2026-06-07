# 📁 TON Israel  מפת פרויקט מלאה

## 🗂️ מבנה התיקיות
D:\PROJ\TON-Israel
├── bot\ # קוד הבוט
│ ├── main.py # כניסה ראשית, רישום פקודות, Webhook/Polling
│ ├── config.py # הגדרות (טעינת .env)
│ ├── database
│ │ ├── models.py # כל המודלים (User, CommandLog, Referral, UserProfile, UserExpense, UserMemory)
│ │ └── session.py # חיבור למסד הנתונים (SQLite / PostgreSQL)
│ ├── routers\ # נתבי טלגרם (כל פקודה/כפתור)
│ │ ├── start.py # /start, תפריטים, callbacks
│ │ ├── compare.py # /compare, תרחישים
│ │ ├── budget.py # /budget
│ │ ├── profile.py # /profile, /setincome, /addexpense, /expenses, /delexpense
│ │ ├── admin.py # /admin (לאדמין בלבד)
│ │ ├── debug.py # /debug (סטטוס מערכת)
│ │ ├── daily.py # /daily (סיכום יומי)
│ │ ├── mydata.py # /mydata (זיכרון למשתמש)
│ │ ├── crypto.py, cbdc.py, decentral.py, socio.py, anti.py, edu.py # אקדמיה
│ │ ├── faq.py, tip.py, stats.py, top.py, ref.py, wallet.py, why.py, business.py, help.py, id.py, contact.py, export.py, miniapp.py, keyboard.py
│ │ └── init.py # רשימת כל הראוטרים
│ ├── services\ # לוגיקה עסקית
│ │ ├── calculator.py # מחשבון עמלות
│ │ ├── budget.py # מחשבון תקציב
│ │ ├── profile_service.py # ניהול פרופילים, הוצאות
│ │ ├── referral_service.py# קודי הפניה, לוח מובילים
│ │ ├── memory_service.py # זיכרון למשתמש
│ │ ├── export_service.py # ייצוא CSV
│ │ └── redis_service.py # Redis (אופציונלי)
│ ├── keyboards\ # תפריטי Inline
│ │ └── inline.py # main_menu, savings_menu, academy_menu, community_menu, presets_menu
│ ├── messages\ # טקסטים
│ │ └── he.py # כל ההודעות בעברית
│ └── utils\ # לוגים
│ └── logger.py
├── public\ # דפי נחיתה ומיני-אפ
│ ├── index.html # דף נחיתה ראשי
│ └── landing
│ ├── miniapp.html # מיני-אפ (מחשבון ויזואלי)
│ ├── css\style.css
│ └── js\script.js
├── test_bot.ps1 # סקריפט בדיקות אוטומטיות (21 פקודות)
├── run_dev.ps1 # סקריפט הרצה מקומית
├── connect_pg.ps1 # חיבור ל-PostgreSQL
├── connect_redis.ps1 # חיבור ל-Redis
├── Dockerfile # Docker build
├── docker-compose.yml
├── requirements.txt
├── .env # משתני סביבה (לא בגיט!)
├── .gitignore
├── OPS.md # מדריך תפעול
├── PROJECT_MAP.md # המסמך הזה
└── README.md


## 🔐 אדמין
- `/admin`  זמין רק למשתמשים ברשימת `ADMIN_IDS` (קובץ `.env`).
- `/debug`  מציג סטטוס מערכת (זמין לכולם).

## 🚀 המשך פיתוח
1. **הוספת פקודה חדשה**  צור קובץ `routers/חדש.py` עם ראוטר, הוסף אותו ל-`__init__.py`.
2. **עדכון טקסטים**  ערוך את `messages/he.py`.
3. **הרצה**  `python bot/main.py` (מקומי) או `git push` (Railway).

## 📊 מסדי נתונים
- **SQLite** (ברירת מחדל)  `data.db`.
- **PostgreSQL**  הפעל דרך Railway, הגדר `DATABASE_URL` (הקוד תומך אוטומטית).
- **Redis**  `redis_service.py` מוכן, דורש `REDIS_URL`.

## 🧪 בדיקות
- `.\test_bot.ps1`  בודק שכל הפקודות חוזרות תשובה (200 OK).
- לבדיקת תוכן  הרץ ידנית את הפקודה בבוט ווודא שהתשובה נכונה.
