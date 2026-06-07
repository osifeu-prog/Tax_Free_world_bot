import asyncio
from bot.database.session import engine
from sqlalchemy import text

async def main():
    async with engine.connect() as c:
        r = await c.execute(text('SELECT count(*) FROM users'))
        print('Users:', await r.scalar())
        r = await c.execute(text('SELECT count(*) FROM referrals'))
        print('Referrals:', await r.scalar())
        r = await c.execute(text('SELECT count(*) FROM command_logs'))
        print('Commands:', await r.scalar())

asyncio.run(main())
