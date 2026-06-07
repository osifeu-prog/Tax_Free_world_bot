import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), 'bot.db')
conn = sqlite3.connect(db_path)
cur = conn.cursor()

for col in ['email', 'google_id', 'password_hash']:
    try:
        cur.execute(f'ALTER TABLE users ADD COLUMN {col} VARCHAR(255)')
        print(f'Added column {col}')
    except sqlite3.OperationalError as e:
        if 'duplicate' in str(e).lower():
            print(f'Column {col} already exists')
        else:
            print(f'Error adding {col}: {e}')

conn.commit()
conn.close()
print('Done')
