# -*- coding: utf-8 -*-
from sqlalchemy import select
from bot.database.models import UserMemory
from bot.database.session import async_session
import datetime

async def save_user_memory(telegram_id: int, command: str, params: str, result: str):
    async with async_session() as session:
        mem = await session.get(UserMemory, telegram_id)
        if not mem:
            mem = UserMemory(telegram_id=telegram_id, last_command=command, last_params=params, last_result=result)
            session.add(mem)
        else:
            mem.last_command = command
            mem.last_params = params
            mem.last_result = result
            mem.updated_at = datetime.datetime.utcnow()
        await session.commit()

async def get_user_memory(telegram_id: int):
    async with async_session() as session:
        result = await session.execute(
            select(UserMemory).where(UserMemory.telegram_id == telegram_id)
        )
        return result.scalar_one_or_none()

