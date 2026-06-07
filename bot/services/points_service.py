from sqlalchemy import select
from bot.database.models import User
from bot.database.session import async_session

async def add_points(telegram_id: int, amount: int):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.telegram_id == telegram_id))
        user = result.scalar_one_or_none()
        if user:
            user.points = (user.points or 0) + amount
            await session.commit()
            return user.points
        return 0

async def get_points(telegram_id: int) -> int:
    async with async_session() as session:
        result = await session.execute(select(User.points).where(User.telegram_id == telegram_id))
        pts = result.scalar_one_or_none()
        return pts or 0

async def get_user(telegram_id: int):
    async with async_session() as session:
        return await session.get(User, telegram_id)

async def get_top_points(limit=5):
    async with async_session() as session:
        result = await session.execute(
            select(User.telegram_id, User.points).order_by(User.points.desc()).limit(limit)
        )
        return [(row.telegram_id, row.points) for row in result if row.points]
