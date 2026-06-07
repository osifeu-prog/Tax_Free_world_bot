from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from sqlalchemy import select
from bot.database.models import AdminRequest
from bot.database.session import async_session
from bot.config import settings
from bot.services.points_service import get_points

router = Router()

@router.message(Command("requestadmin"))
async def cmd_request_admin(msg: Message):
    user_id = msg.from_user.id
    # בדיקת נקודות (דוגמה: צריך 500 נקודות)
    points = await get_points(user_id)
    if points < 500:
        await msg.answer(
            f"⛔ כדי לבקש הרשאת ניהול, עליך לצבור לפחות 500 נקודות.\n"
            f"יש לך כרגע {points} נקודות.\n"
            f"שחק ב‑/gift, הפץ את הבוט, וצבור נקודות!"
        )
        return
    # בדיקה שלא קיימת בקשה פתוחה
    async with async_session() as session:
        result = await session.execute(
            select(AdminRequest).where(
                AdminRequest.telegram_id == user_id,
                AdminRequest.status == "pending"
            )
        )
        if result.scalar_one_or_none():
            await msg.answer("⏳ כבר יש לך בקשה פתוחה. אנא המתן לאישור.")
            return
        # שמירת הבקשה
        req = AdminRequest(telegram_id=user_id)
        session.add(req)
        await session.commit()
        req_id = req.id
    # שליחת הבקשה לאדמין
    super_admin_id = settings.admin_ids[0]
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ אשר", callback_data=f"approve_req_{req_id}"),
         InlineKeyboardButton(text="❌ דחה", callback_data=f"reject_req_{req_id}")]
    ])
    await msg.bot.send_message(
        super_admin_id,
        f"📥 <b>בקשת הרשאה חדשה!</b>\n"
        f"משתמש: {msg.from_user.first_name} (ID: {user_id})\n"
        f"נקודות: {points}\n"
        f"בקשה #{req_id}",
        parse_mode="HTML",
        reply_markup=kb
    )
    await msg.answer("✅ בקשתך נשלחה למנהל. תקבל הודעה כשהיא תטופל.")

# callback לאישור/דחייה
from aiogram import F
from aiogram.types import CallbackQuery
from bot.services.admin_service import add_admin
import secrets, string

@router.callback_query(F.data.startswith("approve_req_"))
async def approve_request(call: CallbackQuery):
    req_id = int(call.data.split("_")[-1])
    async with async_session() as session:
        req = await session.get(AdminRequest, req_id)
        if not req:
            await call.answer("הבקשה לא נמצאה.", show_alert=True)
            return
        req.status = "approved"
        # יצירת סיסמה אקראית
        password = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(8))
        await add_admin(req.telegram_id, "admin", password)
        await session.commit()
    # הודעה למשתמש
    await call.bot.send_message(
        req.telegram_id,
        f"🎉 <b>בקשתך אושרה!</b>\n\n"
        f"הסיסמה שלך: <code>{password}</code>\n"
        f"החלף אותה בהקדם: /setpassword {password} <סיסמה חדשה>",
        parse_mode="HTML"
    )
    await call.message.edit_text(f"✅ בקשה #{req_id} אושרה.")
    await call.answer("אושר.")

@router.callback_query(F.data.startswith("reject_req_"))
async def reject_request(call: CallbackQuery):
    req_id = int(call.data.split("_")[-1])
    async with async_session() as session:
        req = await session.get(AdminRequest, req_id)
        if not req:
            await call.answer("הבקשה לא נמצאה.", show_alert=True)
            return
        req.status = "rejected"
        await session.commit()
    await call.bot.send_message(req.telegram_id, "❌ בקשתך להרשאת ניהול נדחתה.")
    await call.message.edit_text(f"❌ בקשה #{req_id} נדחתה.")
    await call.answer("נדחה.")
