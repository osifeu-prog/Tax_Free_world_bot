from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from bot.database.session import async_session
from bot.database.models import Course
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

router = Router()

@router.message(Command("academy"))
async def cmd_academy(msg: Message):
    async with async_session() as session:
        stmt = select(Course).where(Course.is_active == True).order_by(Course.order_num)
        courses = (await session.execute(stmt)).scalars().all()
    
    if not courses:
        await msg.answer("📚 עדיין אין קורסים. בקרוב יתווספו!")
        return

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"📖 {c.title}", callback_data=f"course_start_{c.id}")]
        for c in courses
    ])

    await msg.answer(
        "<b>🎓 האקדמיה של TON Israel</b>\n\nבחר קורס:", 
        parse_mode="HTML", 
        reply_markup=kb
    )
