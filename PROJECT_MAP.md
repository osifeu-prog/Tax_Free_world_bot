# 📁 TON Israel  מפת פרויקט מלאה

## 🗂️ מבנה התיקיות

D:\PROJ\TON-Israel
├── bot\ # קוד הבוט
│ ├── main.py # כניסה ראשית, 46 פקודות, API
│ ├── config.py # הגדרות
│ ├── database
│ │ ├── models.py # כל המודלים (User, Referral, UserProfile, UserExpense, UserMemory, Admin, AdminRequest)
│ │ └── session.py # חיבור למסד נתונים
│ ├── routers\ # 30+ נתבים
│ ├── services\ # לוגיקה עסקית
│ ├── keyboards\ # תפריטי Inline
│ ├── messages\ # טקסטים בעברית
│ └── utils\ # לוגים
├── public\ # דפי נחיתה ומיני-אפ
├── test_bot.ps1 # 46 בדיקות
├── check_replies.ps1 # 35 בדיקות תוכן
├── check_infra.ps1 # בדיקת DB/Redis
├── PROGRESS_REPORT.md # דוח התקדמות
├── COMMANDS.md # רשימת פקודות
├── OPS.md # תפעול
├── RBAC.md # מערכת הרשאות
├── PROJECT_MAP.md # המסמך הזה
└── README.md


## 🔐 אדמין
- IDs: 224223270, 8789977826
- `/addadmin`, `/login`, `/setpassword`, `/removeadmin`

## 🚀 פיתוח עתידי
- **הוספת פקודה**  `routers/חדש.py` + `__init__.py` + `main.py`.
- **שינוי טקסטים**  `messages/he.py`.
- **בדיקות**  `.\test_bot.ps1`.
