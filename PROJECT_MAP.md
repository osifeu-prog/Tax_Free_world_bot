# 📁 TON Israel  מפת פרויקט מלאה

## 🗂️ מבנה התיקיות
D:\PROJ\TON-Israel
├── bot
│ ├── main.py # כניסה ראשית, רישום פקודות, Webhook/Polling
│ ├── config.py # הגדרות
│ ├── database
│ │ ├── models.py # כל המודלים
│ │ └── session.py # חיבור למסד נתונים
│ ├── routers\ # 32 נתבים
│ ├── services\ # לוגיקה עסקית
│ ├── keyboards\ # תפריטי Inline
│ ├── messages\ # טקסטים בעברית
│ └── utils\ # לוגים
├── public\ # דפי נחיתה ומיני-אפ
├── test_bot.ps1 # 32 בדיקות אוטומטיות
├── COMMANDS.md # רשימת כל הפקודות
├── OPS.md # מדריך תפעול
├── PROJECT_MAP.md # מפת פרויקט
└── README.md


## 🔐 אדמין
- IDs: 224223270, 8789977826

## 🚀 פיתוח עתידי
- **הוספת פקודה**  `routers/חדש.py` + `__init__.py` + `main.py`.
- **שינוי טקסטים**  `messages/he.py`.
- **בדיקות**  `.\test_bot.ps1`.
