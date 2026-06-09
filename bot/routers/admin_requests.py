from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from bot.database.session import async_session
from bot.database.models import Admin, AdminRequest
from bot.config import settings
from sqlalchemy import select, update
import json

router = Router()

def is_admin(user_id: int) -> bool:
    return str(user_id) in (json.loads(settings.admin_ids) or "")

@router.message(Command("requestadmin"))
async def cmd_requestadmin(msg: Message):
    if is_admin(msg.from_user.id):
        await msg.answer("??? ??? ????.")
        return
    async with async_session() as session:
        existing = (await session.execute(select(AdminRequest).where(AdminRequest.telegram_id == msg.from_user.id, AdminRequest.status == "pending"))).scalar_one_or_none()
        if existing:
            await msg.answer("?? ?? ??? ???? ??????.")
            return
        req = AdminRequest(telegram_id=msg.from_user.id, username=msg.from_user.username, reason="???? ?????? ?????")
        session.add(req)
        await session.commit()
        await msg.answer("? ????? ??????? ????? ?????. ??????? ????? ????.")
        # ????? ??????? (???????)
        for admin_id in json.loads(json.loads(settings.admin_ids)):
            try:
                await msg.bot.send_message(admin_id, f"?? ???? ????: @{msg.from_user.username} (ID: {msg.from_user.id}) ???? ?????? ?????.")
            except:
                pass

@router.message(Command("approve"))
async def cmd_approve(msg: Message):
    if not is_admin(msg.from_user.id):
        await msg.answer("?? ?????? ??????.")
        return
    parts = msg.text.split()
    if len(parts) < 2:
        await msg.answer("?????: /approve <telegram_id>")
        return
    target_id = int(parts[1])
    async with async_session() as session:
        await session.execute(update(AdminRequest).where(AdminRequest.telegram_id == target_id, AdminRequest.status == "pending").values(status="approved"))
        await session.execute(update(AdminRequest).where(AdminRequest.telegram_id == target_id).values(negotiations=AdminRequest.negotiations + "\n????."))
        await session.commit()
        await msg.answer("? ????? ?????. ???? ?? ?????? ?-admin ?? /addadmin.")

@router.message(Command("deny"))
async def cmd_deny(msg: Message):
    if not is_admin(msg.from_user.id):
        await msg.answer("?? ?????? ??????.")
        return
    parts = msg.text.split()
    if len(parts) < 2:
        await msg.answer("?????: /deny <telegram_id>")
        return
    target_id = int(parts[1])
    async with async_session() as session:
        await session.execute(update(AdminRequest).where(AdminRequest.telegram_id == target_id, AdminRequest.status == "pending").values(status="denied"))
        await session.commit()
        await msg.answer("? ????? ?????.")
        await msg.bot.send_message(target_id, "????? ??????? ????? ?????.")

@router.message(Command("negotiations"))
async def cmd_negotiations(msg: Message):
    if not is_admin(msg.from_user.id):
        await msg.answer("?? ?????? ??????.")
        return
    async with async_session() as session:
        reqs = (await session.execute(select(AdminRequest).where(AdminRequest.status == "pending"))).scalars().all()
        if not reqs:
            await msg.answer("??? ????? ???????.")
            return
        for req in reqs:
            await msg.answer(f"?? ID: {req.telegram_id} | @{req.username}\n?????: {req.negotiations or '???'}")

