from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from bot.database.session import async_session
from bot.database.models import Course, UserProgress
from sqlalchemy import select, update
import json

router = Router()

# שמור את הפקודה /academy (הקיימת) + הוסף callback
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

        # טען / צור מעקב התקדמות
        progress_stmt = select(UserProgress).where(
            UserProgress.telegram_id == user_id,
            UserProgress.course_id == course_id
        )
        progress = (await session.execute(progress_stmt)).scalar_one_or_none()
        if not progress:
            progress = UserProgress(telegram_id=user_id, course_id=course_id, completed_lessons="[]")
            session.add(progress)
            await session.commit()

        # הצג תוכן (לעת עתה  description; בהמשך נחלק לשיעורים)
        text = f"📖 <b>{course.title}</b>\n\n{course.description}\n\n🟢 התחלת את הקורס!"
        await callback.message.answer(text, parse_mode="HTML")
        await callback.answer()
