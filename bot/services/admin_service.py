from sqlalchemy import select, delete
from bot.database.session import async_session
from bot.database.models import Admin
import bcrypt

async def add_admin(telegram_id: int, role: str, password: str):
    async with async_session() as session:
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        admin = Admin(telegram_id=telegram_id, role=role, password_hash=hashed)
        session.add(admin)
        await session.commit()
        return admin

async def get_admin(telegram_id: int):
    async with async_session() as session:
        result = await session.execute(select(Admin).where(Admin.telegram_id == telegram_id))
        return result.scalar_one_or_none()

async def verify_password(telegram_id: int, password: str) -> bool:
    admin = await get_admin(telegram_id)
    if not admin:
        return False
    return bcrypt.checkpw(password.encode(), admin.password_hash.encode())

async def set_password(telegram_id: int, old_password: str, new_password: str) -> bool:
    if not await verify_password(telegram_id, old_password):
        return False
    async with async_session() as session:
        admin = await session.get(Admin, telegram_id)
        admin.password_hash = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
        await session.commit()
        return True

async def remove_admin(telegram_id: int):
    async with async_session() as session:
        await session.execute(delete(Admin).where(Admin.telegram_id == telegram_id))
        await session.commit()
