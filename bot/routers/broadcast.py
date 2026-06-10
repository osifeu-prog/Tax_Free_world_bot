from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from sqlalchemy import text
from bot.database.session import engine
import asyncio

router = Router()

RED_BUTTON_TEXT = "🔴 לחץ עליי! (אין סיכוי שזה עושה משהו)"

async def send_red_button(bot, user_id: int):
    try:
        await bot.send_message(
            user_id,
            "⏰ עברו 6 שעות ועדיין לא לחצת על הכפתור האדום!\n\nהגיע הזמן לגלות שזה לא עושה כלום 🔴",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text=RED_BUTTON_TEXT, callback_data="useless_red_button")]
            ])
        )
    except Exception:
        pass

async def broadcast_inactive(bot, hours: int = 6):
    async with engine.begin() as conn:
        rows = await conn.run_sync(
            lambda c: c.execute(text("""
                SELECT u.telegram_id FROM users u
                WHERE u.telegram_id NOT IN (
                    SELECT user_id FROM useless_log WHERE action='red_button_pressed'
                )
                AND u.created_at < datetime('now', :hours)
            """), {"hours": f"-{hours} hours"}).fetchall()
        )
    for row in rows:
        await send_red_button(bot, row[0])
        await asyncio.sleep(0.05)

@router.message(Command('broadcast_red'))
async def cmd_broadcast_red(msg: Message):
    if msg.from_user.id != 224223270:
        await msg.answer("⛔ אדמין בלבד")
        return
    await msg.answer("🔴 שולח כפתור אדום למי שלא לחץ...")
    await broadcast_inactive(msg.bot)
    await msg.answer("✅ סיימתי")

@router.callback_query(F.data == "useless_red_button")
async def red_button_pressed(callback: CallbackQuery):
    from bot.services.useless_logger import log_useless_action
    await log_useless_action(callback.from_user.id, "red_button_pressed")
    await callback.answer("🔴 כלום לא קרה. בדיוק כפי שהובטח.", show_alert=True)