import asyncio
from bot.database.session import engine
from bot.database.models import Base

async def main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ DB initialized")

asyncio.run(main())
