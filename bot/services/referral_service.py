# -*- coding: utf-8 -*-
import random, string
from sqlalchemy import select, func
from bot.database.models import Referral, User, CommandLog
from bot.database.session import async_session

def generate_code(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

async def get_or_create_ref_code(user_id):
    async with async_session() as session:
        result = await session.execute(select(Referral).where(Referral.inviter_id == user_id))
        ref = result.scalar_one_or_none()
        if not ref:
            ref = Referral(inviter_id=user_id, code=generate_code())
            session.add(ref)
            await session.commit()
            await session.refresh(ref)
        return ref.code

async def get_ref_stats():
    async with async_session() as session:
        users = await session.scalar(select(func.count(User.id)))
        refs = await session.scalar(select(func.count(Referral.id)))
        compares = await session.scalar(select(func.count(CommandLog.id)).where(CommandLog.command == "compare"))
        return users or 0, refs or 0, compares or 0

async def get_top_referrers(limit=5):
    async with async_session() as session:
        result = await session.execute(select(Referral).order_by(Referral.clicks.desc()).limit(limit))
        refs = result.scalars().all()
        lines = [f"{i}. {('🌟 ' if r.clicks >= 5 else '')}<code>{r.code}</code>  {r.clicks} מצטרפים" for i, r in enumerate(refs, 1)]
        return "\n".join(lines) if lines else "אין עדיין."

# ⬇️ פונקציה חדשה  רישום משתמש
async def register_user(telegram_id: int, language: str = "he"):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.telegram_id == telegram_id))
        user = result.scalar_one_or_none()
        if not user:
            user = User(telegram_id=telegram_id, language=language)
            session.add(user)
            await session.commit()
            await session.refresh(user)
        return user

# ⬇️ פונקציה חדשה  רישום פקודה
async def log_command(user_id: int, command: str, params: str = ""):
    async with async_session() as session:
        log = CommandLog(user_id=user_id, command=command, params=params)
        session.add(log)
        await session.commit()

