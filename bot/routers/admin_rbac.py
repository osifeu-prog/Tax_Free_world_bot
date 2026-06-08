from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from bot.database.session import async_session
from bot.database.models import UserRole
from sqlalchemy import select
import json
from bot.config import settings

router = Router()

@router.message(Command("setrole"))
async def cmd_setrole(msg: Message):
    # בדיקת אדמין
    try:
        admin_ids = json.loads(settings.admin_ids)
    except:
        admin_ids = [int(x.strip()) for x in settings.admin_ids.split(",") if x.strip()]
    if msg.from_user.id not in admin_ids:
        await msg.answer("⛔ רק מנהלים מורשים.")
        return
    parts = msg.text.split()
    if len(parts) < 3:
        await msg.answer("שימוש: /setrole <telegram_id> <role>\nתפקידים: citizen, entrepreneur, leader, expert, fighter, builder")
        return
    target_id = int(parts[1])
    role = parts[2].lower()
    async with async_session() as session:
        stmt = select(UserRole).where(UserRole.telegram_id == target_id)
        user_role = (await session.execute(stmt)).scalar_one_or_none()
        if user_role:
            user_role.role = role
        else:
            user_role = UserRole(telegram_id=target_id, role=role)
            session.add(user_role)
        await session.commit()
        await msg.answer(f"✅ התפקיד של {target_id} עודכן ל‑{role}")

@router.message(Command("myrole"))
async def cmd_myrole(msg: Message):
    async with async_session() as session:
        stmt = select(UserRole).where(UserRole.telegram_id == msg.from_user.id)
        user_role = (await session.execute(stmt)).scalar_one_or_none()
        role = user_role.role if user_role else "citizen"
        await msg.answer(f"🎭 התפקיד שלך: {role}")
