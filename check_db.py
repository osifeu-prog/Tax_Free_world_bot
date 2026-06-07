# -*- coding: utf-8 -*-
import sqlite3

DB_PATH = "data.db"

print("📊 בדיקת מסד הנתונים (SQLite)...")
try:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    tables = ["users", "user_profiles", "user_expenses", "command_logs", "referrals", "admins", "user_memory", "admin_requests", "households", "shopping_items", "chores"]
    for t in tables:
        try:
            cur.execute(f"SELECT COUNT(*) FROM {t}")
            count = cur.fetchone()[0]
            print(f"  {t}: {count}")
        except:
            print(f"  {t}: ❌ not found")

    print("\n📊 Sample user_profiles:")
    try:
        cur.execute("SELECT telegram_id, monthly_income FROM user_profiles LIMIT 5")
        for row in cur.fetchall():
            print(f"  ID: {row[0]}, Income: {row[1]}")
    except: pass

    print("\n💰 Sample user_expenses:")
    try:
        cur.execute("SELECT id, category, amount FROM user_expenses LIMIT 5")
        for row in cur.fetchall():
            print(f"  ID: {row[0]}, Category: {row[1]}, Amount: {row[2]}")
    except: pass

    conn.close()
except Exception as e:
    print(f"❌ Error: {e}")

