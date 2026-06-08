import sqlite3

conn = sqlite3.connect('bot.db')
cursor = conn.cursor()

# יצירת טבלאות אם לא קיימות (בטוח)
cursor.executescript('''
    CREATE TABLE IF NOT EXISTS courses (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        description TEXT,
        content TEXT,
        required_role TEXT DEFAULT "citizen",
        order_num INTEGER DEFAULT 0,
        is_active BOOLEAN DEFAULT 1,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS user_progress (
        id INTEGER PRIMARY KEY,
        telegram_id INTEGER,
        course_id INTEGER,
        completed_lessons TEXT DEFAULT "[]",
        score INTEGER DEFAULT 0,
        last_accessed DATETIME DEFAULT CURRENT_TIMESTAMP
    );
''')

# בדיקה אם כבר יש קורסים
cursor.execute("SELECT COUNT(*) FROM courses")
if cursor.fetchone()[0] > 0:
    print("✅ קורסים כבר קיימים ב-DB")
else:
    courses = [
        ("מבוא לקריפטו", "למה ביטקוין ו-TON משנים את העולם", "citizen", 1),
        ("CBDC והסכנות", "למה מטבעות בנק מרכזי הם סיכון לחירות", "citizen", 2),
        ("ביזור מול ריכוז", "ההבדל בין מערכות מבוזרות לריכוזיות", "entrepreneur", 3),
        ("סוציוקרטיה", "דמוקרטיה מבוזרת ושיתופית", "leader", 4),
    ]
    
    cursor.executemany(
        "INSERT INTO courses (title, description, required_role, order_num) VALUES (?, ?, ?, ?)",
        courses
    )
    conn.commit()
    print(f"✅ {len(courses)} קורסים נוספו בהצלחה!")

conn.close()
