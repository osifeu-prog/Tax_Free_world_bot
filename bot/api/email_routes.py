from aiohttp import web
import traceback
from passlib.context import CryptContext
from bot.database.session import engine
from sqlalchemy import text

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def register(request):
    try:
        data = await request.json()
        email = data.get("email")
        password = data.get("password")
        if not email or not password:
            return web.json_response({"error": "Missing email/password"}, status=400)
        async with engine.begin() as conn:
            # וודא שהטבלה קיימת
            await conn.execute(text("CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, email VARCHAR(255) UNIQUE, password_hash VARCHAR(255), language VARCHAR(2) DEFAULT 'he')"))
            # בדוק אם האימייל כבר קיים
            res = await conn.execute(text("SELECT id FROM users WHERE email = :email"), {"email": email})
            if res.fetchone():
                return web.json_response({"error": "Email already registered"}, status=400)
            hashed = pwd_context.hash(password)
            res = await conn.execute(
                text("INSERT INTO users (email, password_hash, language) VALUES (:email, :pwd, 'he') RETURNING id"),
                {"email": email, "pwd": hashed}
            )
            user_id = res.fetchone()[0]
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
            # וודא שהטבלה קיימת
            await conn.execute(text("CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, email VARCHAR(255) UNIQUE, password_hash VARCHAR(255), language VARCHAR(2) DEFAULT 'he')"))
            res = await conn.execute(text("SELECT id, password_hash FROM users WHERE email = :email"), {"email": email})
            row = res.fetchone()
            if not row or not pwd_context.verify(password, row[1]):
                return web.json_response({"error": "Invalid credentials"}, status=401)
            from bot.utils.auth import create_access_token
            token = create_access_token({"sub": str(row[0]), "email": email})
            return web.json_response({"access_token": token, "user_id": row[0]})
    except Exception as e:
        return web.json_response({"error": str(e), "traceback": traceback.format_exc()}, status=500)
