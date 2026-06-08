import sqlite3
conn = sqlite3.connect('bot.db')
c = conn.cursor()

# בדיקה אם הטבלה users קיימת
tables = [row[0] for row in c.execute("SELECT name FROM sqlite_master WHERE type='table'")]
if 'users' not in tables:
    print("⚠️ טבלת users עדיין לא קיימת מקומית - תיווצר אוטומטית בטעינה ראשונה")
else:
    existing = [i[1] for i in c.execute("PRAGMA table_info(users)").fetchall()]
    for col, definition in [
        ("language", "TEXT DEFAULT 'he'"),
        ("country", "TEXT DEFAULT 'IL'"),
        ("timezone", "TEXT DEFAULT 'Asia/Jerusalem'"),
        ("currency", "TEXT DEFAULT 'ILS'")
    ]:
        if col not in existing:
            c.execute(f"ALTER TABLE users ADD COLUMN {col} {definition}")
            print(f"✅ Added column: {col}")
        else:
            print(f"⏭️ {col} already exists")

conn.commit()
conn.close()
print("✅ Migration completed")
