from aiohttp import web
import traceback, hashlib, os
from bot.database.session import engine
from sqlalchemy import text

async def register(request):
    try:
        data = await request.json()
        email = data.get("email")
        password = data.get("password")
        if not email or not password:
            return web.json_response({"error": "Missing email/password"}, status=400)
        # hash with SHA‑256 (without bcrypt)
        salt = os.urandom(16).hex()
        hashed = hashlib.sha256((password + salt).encode()).hexdigest()
        async with engine.begin() as conn:
            await conn.execute(text(
                "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, email VARCHAR(255) UNIQUE, password_hash VARCHAR(255), language VARCHAR(2) DEFAULT 'he')"
            ))
            res = await conn.execute(text("SELECT id FROM users WHERE email = :email"), {"email": email})
            if res.fetchone():
                return web.json_response({"error": "Email already registered"}, status=400)
            res = await conn.execute(
                text("INSERT INTO users (email, password_hash, language) VALUES (:email, :pwd, 'he')"),
                {"email": email, "pwd": hashed}
            )
            # fetch the newly inserted id
            user_id = (await conn.execute(text("SELECT last_insert_rowid()"))).fetchone()[0]
            from bot.utils.auth import create_access_token
            token = create_access_token({"sub": str(user_id), "email": email})
            return web.json_response({"access_token": token, "user_id": user_id})
    except Exception as e:
        return web.json_response({"error": str(e), "traceback": traceback.format_exc()}, status=500)

async def login(request):
    try:
        data = await request.json()
        email = data.get("email")
        password = data.get("password")
        if not email or not password:
            return web.json_response({"error": "Missing email/password"}, status=400)
        async with engine.begin() as conn:
            res = await conn.execute(text("SELECT id, password_hash FROM users WHERE email = :email"), {"email": email})
            row = res.fetchone()
            if not row:
                return web.json_response({"error": "Invalid credentials"}, status=401)
            # compare hash
            salt = row[1][:32]   # first 32 chars are the salt
            expected = hashlib.sha256((password + salt).encode()).hexdigest()
            if expected != row[1]:
                return web.json_response({"error": "Invalid credentials"}, status=401)
            from bot.utils.auth import create_access_token
            token = create_access_token({"sub": str(row[0]), "email": email})
            return web.json_response({"access_token": token, "user_id": row[0]})
    except Exception as e:
        return web.json_response({"error": str(e), "traceback": traceback.format_exc()}, status=500)
