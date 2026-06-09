# -*- coding: utf-8 -*-
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from passlib.context import CryptContext
from bot.database.models import User
from bot.database.session import async_session
from bot.utils.auth import create_access_token
from sqlalchemy import select

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class RegisterRequest(BaseModel):
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/auth/register")
async def register(data: RegisterRequest):
    async with async_session() as session:
        stmt = select(User).where(User.email == data.email)
        existing = (await session.execute(stmt)).scalar_one_or_none()
        if existing:
            raise HTTPException(400, "Email already registered")
        user = User(email=data.email, password_hash=pwd_context.hash(data.password), language="he")
        session.add(user)
        await session.commit()
        token = create_access_token({"sub": str(user.id), "email": data.email})
        return {"access_token": token, "user_id": user.id}

@router.post("/auth/login")
async def login(data: LoginRequest):
    async with async_session() as session:
        stmt = select(User).where(User.email == data.email)
        user = (await session.execute(stmt)).scalar_one_or_none()
        if not user or not pwd_context.verify(data.password, user.password_hash):
            raise HTTPException(401, "Invalid credentials")
        token = create_access_token({"sub": str(user.id), "email": data.email})
        return {"access_token": token, "user_id": user.id}

