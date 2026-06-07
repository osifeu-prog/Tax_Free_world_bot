import asyncio, random
from datetime import date
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from bot.services.points_service import add_points, get_user
from bot.database.session import async_session
from bot.database.models import User
from sqlalchemy import select

router = Router()

PRIZES = [(0, "כלום... נסה שוב!"), (10, "10 נקודות!"), (20, "20 נקודות!"), (50, "50 נקודות!"), (100, "100 נקודות! 🎉"), (200, "200 נקודות! 🌟")]

@router.message(Command("gift"))
async def cmd_gift(msg: Message):
    async with async_session() as session:
        user = await session.get(User, msg.from_user.id)
        if not user:
            await msg.answer("תחילה עליך לשלוח /start כדי להירשם.")
            return
        today = date.today().isoformat()
        if user.last_gift_date == today:
            if user.gift_shares_today >= 5:
                # reset shares and allow another try
                user.gift_shares_today = 0
                await session.commit()
            else:
                await msg.answer(
                    f"🎁 כבר קיבלת מתנה היום.\n"
                    f"שתף את הבוט 5 פעמים (לחץ /ref ושתף) כדי לקבל ניסיון נוסף!\n"
                    f"שיתופים היום: {user.gift_shares_today}/5",
                    parse_mode="HTML"
                )
                return
        # שליחת אנימציית 🎰
        dice = await msg.answer_dice(emoji="🎰")
        prize = random.choices(PRIZES, weights=[30,25,20,15,7,3], k=1)[0]
        points, text = prize
        if points > 0:
            total = await add_points(msg.from_user.id, points)
            result = f"🎁 {text}\nיש לך עכשיו {total} נקודות!"
        else:
            result = f"😕 {text}"
        await asyncio.sleep(3)
        # שליחת הודעה חדשה עם התוצאה (לא לערוך את הקוביה)
        await msg.answer(result)
        # עדכון תאריך
        user.last_gift_date = today
        await session.commit()
