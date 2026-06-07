import asyncio, logging, os
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand, BotCommandScopeDefault
from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from passlib.context import CryptContext
from sqlalchemy import select

from bot.config import settings
from bot.database.session import async_session, engine
from bot.database.models import Base, User
from bot.utils.auth import create_access_token

# ---------- Telegram bot setup ----------
bot = Bot(token=settings.bot_token)
dp = Dispatcher(storage=MemoryStorage())

# ---------- FastAPI app ----------
app = FastAPI()


@app.on_event("startup")
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logging.info("Database tables ready")
app.mount("/landing", StaticFiles(directory="public/landing"), name="landing")

# ---------- Email auth inline ----------
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class RegisterRequest(BaseModel):
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

email_router = APIRouter()

@email_router.post("/auth/register")
async def register(data: RegisterRequest):
    async with async_session() as session:
        stmt = select(User).where(User.email == data.email)
        if (await session.execute(stmt)).scalar_one_or_none():
            raise HTTPException(400, "Email already registered")
        user = User(email=data.email, password_hash=pwd_context.hash(data.password), language="he")
        session.add(user)
        await session.commit()
        token = create_access_token({"sub": str(user.id), "email": data.email})
        return {"access_token": token, "user_id": user.id}

@email_router.post("/auth/login")
async def login(data: LoginRequest):
    async with async_session() as session:
        stmt = select(User).where(User.email == data.email)
        user = (await session.execute(stmt)).scalar_one_or_none()
        if not user or not pwd_context.verify(data.password, user.password_hash):
            raise HTTPException(401, "Invalid credentials")
        token = create_access_token({"sub": str(user.id), "email": data.email})
        return {"access_token": token, "user_id": user.id}

app.include_router(email_router, prefix="/api")

# ---------- Startup: create tables ----------
@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logging.info("Database tables created/verified")

# ---------- Import other routers (bot commands, etc.) ----------
import bot.routers.start, bot.routers.help, bot.routers.export  # and other routers
# Register them with the dispatcher (not shown here, keep existing setup)

async def set_commands():
    commands = [
        BotCommand(command="start", description="????"),
        # ... other commands
    ]
    await bot.set_my_commands(commands, scope=BotCommandScopeDefault())

async def main():
    await set_commands()
    # Include any other routers
    dp.include_router(...)  # keep your existing router inclusion
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())

