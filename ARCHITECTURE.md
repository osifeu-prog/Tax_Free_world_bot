# 🏗️ ארכיטקטורת TON Israel Bot

## תרשים זרימה
משתמש ←→ Telegram Bot ←→ aiogram Dispatcher
↓
┌───────┴────────┐
│ Routers │
│ (47 פקודות) │
└───────┬────────┘
↓
┌───────┴────────┐
│ Services │
│ (AI, Profile, │
│ Points, RBAC) │
└───────┬────────┘
↓
┌───────┴────────┐
│ Database │
│ (PostgreSQL) │
└────────────────┘



## רכיבים
- **aiogram**  Telegram API.
- **aiohttp**  Healthcheck, API.
- **SQLAlchemy**  ORM (PostgreSQL/SQLite).
- **Alembic**  מיגרציות.
- **Redis**  מטמון.
- **Gemini API**  AI.
- **bcrypt**  סיסמאות.

## פריסה
- **Railway**  Dockerfile.
- **GitHub**  ניהול גרסאות.
