from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from bot.database.session import async_session
from bot.database.models import Course, UserProgress
from sqlalchemy import select
import json

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
    await msg.answer("<b>🎓 האקדמיה של TON Israel</b>\n\nבחר קורס:", parse_mode="HTML", reply_markup=kb)

@router.callback_query(lambda c: c.data and c.data.startswith("course_start_"))
async def course_start(callback: CallbackQuery):
    course_id = int(callback.data.split("_")[-1])
    user_id = callback.from_user.id
    async with async_session() as session:
        stmt = select(Course).where(Course.id == course_id)
        course = (await session.execute(stmt)).scalar_one_or_none()
        if not course:
            await callback.answer("❌ הקורס לא נמצא.", show_alert=True)
            return
        # מעקב התקדמות
        progress_stmt = select(UserProgress).where(
            UserProgress.telegram_id == user_id,
            UserProgress.course_id == course_id
        )
        progress = (await session.execute(progress_stmt)).scalar_one_or_none()
        if not progress:
            progress = UserProgress(telegram_id=user_id, course_id=course_id, completed_lessons="[]")
            session.add(progress)
            await session.commit()
        text = f"📖 <b>{course.title}</b>\n\n{course.description}\n\n🟢 התחלת את הקורס!"
        await callback.message.answer(text, parse_mode="HTML")
        await callback.answer()
