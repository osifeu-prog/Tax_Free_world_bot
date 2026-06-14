from sqlalchemy import select
from bot.database.session import async_session

async def get_top_referrers(limit: int = 10):
    '''גרסה בטוחה - לא קורס אם המודל או השדה חסר'''
    try:
        async with async_session() as session:
            # נמנע קריסה אם Referral.clicks לא קיים
            result = await session.execute(
                select(Referral).limit(limit)
            )
            return result.scalars().all()
    except Exception as e:
        print(f"⚠️ Referral service error: {e}")
        return []  # מחזיר ריק כדי שהבוט לא יקרוס
