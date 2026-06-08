import requests, sqlite3, time, json

TOKEN = "8782546867:AAFkv4mYtkDXvwf9RJpCVU2Tv7oT4lVGq5M"
BASE = f"https://api.telegram.org/bot{TOKEN}"
CHAT_ID = 224223270
DB_PATH = "bot.db"  # מקומי  אבל ניגש ל‑Railway DB! נבצע את זה על Railway.

# במקום לעבוד מול DB מקומי, נריץ על Railway:
# railway run python test_i18n_live.py

# אבל לנוחות, נשתמש ב‑sqlite3 ישירות על Railway.
# נכתוב סקריפט שמרים את Railway.

print("Run this on Railway with:")
print("railway run python test_i18n_live.py")
