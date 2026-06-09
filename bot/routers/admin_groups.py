import json
# -*- coding: utf-8 -*-
# bot/routers/admin_groups.py
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from bot.database.models import Admin, BotGroup
from bot.database.session import async_session
from sqlalchemy import select

router = Router()

@router.message(Command("addgroup"))
async def cmd_addgroup(msg: Message):
    # check admin
    async with async_session() as session:
        stmt = select(Admin).where(Admin.telegram_id == msg.from_user.id)
        admin = (await session.execute(stmt)).scalar_one_or_none()
        if not admin:
            await msg.answer("?? ?????? ??????.")
            return
    parts = msg.text.split()
    if len(parts) < 2:
        await msg.answer("?????: /addgroup <chat_id> <title>")
        return
    chat_id = int(parts[1])
    title = " ".join(parts[2:]) if len(parts) > 2 else "??? ??"
    async with async_session() as session:
        group = BotGroup(chat_id=chat_id, title=title)
        session.add(group)
        await session.commit()
        await msg.answer(f"? ????? {title} ?????.")
@router.message(Command("groups"))
async def cmd_groups(msg: Message):
    async with async_session() as session:
        stmt = select(Admin).where(Admin.telegram_id == msg.from_user.id)
        admin = (await session.execute(stmt)).scalar_one_or_none()
        if not admin:
            await msg.answer("?? ?????? ??????.")
            return
    async with async_session() as session:
        result = await session.execute(select(BotGroup))
        groups = result.scalars().all()
        if not groups:
            await msg.answer("??? ?????? ??????.")
            return
        lst = "\n".join(f"{g.chat_id} | {g.title}" for g in groups)
        await msg.answer(f"?? <b>??????:</b>\n{lst}", parse_mode="HTML")



