from aiohttp import web
import json
from passlib.context import CryptContext
from bot.database.models import User
from bot.database.session import async_session
from bot.utils.auth import create_access_token
from sqlalchemy import select

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def register(request):
    data = await request.json()
    email = data.get("email")
    password = data.get("password")
    if not email or not password:
        return web.json_response({"error": "Missing email/password"}, status=400)
    async with async_session() as session:
        stmt = select(User).where(User.email == email)
        existing = (await session.execute(stmt)).scalar_one_or_none()
        if existing:
            return web.json_response({"error": "Email already registered"}, status=400)
        user = User(email=email, password_hash=pwd_context.hash(password), language="he")
        session.add(user)
        await session.commit()
        token = create_access_token({"sub": str(user.id), "email": email})
        return web.json_response({"access_token": token, "user_id": user.id})

async def login(request):
    data = await request.json()
    email = data.get("email")
    password = data.get("password")
    if not email or not password:
        return web.json_response({"error": "Missing email/password"}, status=400)
    async with async_session() as session:
        stmt = select(User).where(User.email == email)
        user = (await session.execute(stmt)).scalar_one_or_none()
        if not user or not pwd_context.verify(password, user.password_hash):
            return web.json_response({"error": "Invalid credentials"}, status=401)
        token = create_access_token({"sub": str(user.id), "email": email})
        return web.json_response({"access_token": token, "user_id": user.id})
