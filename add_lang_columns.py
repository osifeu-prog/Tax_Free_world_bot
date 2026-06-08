import sqlite3
conn = sqlite3.connect('bot.db')
c = conn.cursor()
# נוסיף רק עמודות שעוד לא קיימות
existing = [i[1] for i in c.execute("PRAGMA table_info(users)").fetchall()]
for col, def_ in [("language", "TEXT DEFAULT 'he'"), ("country", "TEXT DEFAULT 'IL'"), ("timezone", "TEXT DEFAULT 'Asia/Jerusalem'"), ("currency", "TEXT DEFAULT 'ILS'")]:
    if col not in existing:
        c.execute(f"ALTER TABLE users ADD COLUMN {col} {def_}")
        print(f"✅ Added {col}")
conn.commit()
conn.close()
print("✅ Done")
