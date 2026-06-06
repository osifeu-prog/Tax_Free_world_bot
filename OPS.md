# OPS Guide  TON Israel Bot

## כללי עבודה
- כל שינוי בקבצים יתבצע **אך ורק דרך PowerShell** (Set-Content, Add-Content וכו').
- לפני כל שינוי מוודאים שהבוט לא רץ (אלא אם מדובר בעדכון גרסה חמה).
- שומרים גיבוי של `.env` ו-`data.db` טרם מיגרציות.
- כל פיצ'ר חדש  מוסיפים `router` ייעודי ומעדכנים את `bot/routers/__init__.py`.

## סביבת עבודה
- PowerShell בתיקייה `D:\PROJ\TON-Israel`, מופעל venv: `.\.venv\Scripts\Activate.ps1`
- הרצה: `python bot/main.py`

## מבנה הפרויקט
- `bot/`  קוד הבוט.
- `bot/routers/`  כל פיצ'ר ממומש כנתב נפרד.
- `bot/services/`  לוגיקה טהורה (חישובים).
- `bot/keyboards/`  מקלדות Inline.
- `bot/messages/`  טקסטים בעברית.
- `bot/database/`  מודלים ו-Session (SQLite).
- `bot/utils/`  לוגים.

## פקודות שימושיות
- `python bot/main.py`  הרצת הבוט.
- `pip freeze > requirements.txt`  שמירת תלויות (אם הותקנו חדשות).

## פתרון בעיות
- שגיאת ModuleNotFoundError: וודא שקבצי `__init__.py` קיימים בתיקיות הנכונות.
- שגיאות Pydantic: בדוק את `.env`  במיוחד ADMIN_IDS כרשימה `[224223270]`.
