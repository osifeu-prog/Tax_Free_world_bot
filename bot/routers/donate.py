from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

router = Router()
WALLET = "UQCr743gEr_nqV_0SBkSp3CtYS_15R3LDLBvLmKeEv7XdGvp"
ADMIN_GROUP = -1002265834536  # ← שימי כאן את ה-ID של קבוצת האדמינים

class DonateForm(StatesGroup):
    waiting_for_screenshot = State()
    waiting_for_amount = State()
    waiting_for_reason = State()

@router.message(Command('donate'))
async def cmd_donate(msg: Message):
    text = (
        "💖 <b>תמכו בנו!</b>\n\n"
        "TON Israel היא קהילה חופשית ללא מימון ממשלתי.\n"
        "התרומה שלך עוזרת לנו להמשיך לפתח.\n\n"
        f"👛 ארנק TON:\n<code>{WALLET}</code>\n\n"
        "📸 <b>איך לתרום?</b>\n"
        "1️⃣ העבר סכום לארנק שלמעלה.\n"
        "2️⃣ שמור צילום מסך של ההעברה.\n"
        "3️⃣ לחץ על הכפתור למטה וצרף את צילום המסך.\n\n"
        "🙏 לאחר האימות תקבל נקודות!"
    )
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='📤 שלח אישור תרומה', callback_data='donate_screenshot')]
    ])
    await msg.answer(text, parse_mode='HTML', reply_markup=kb)

@router.callback_query(F.data == 'donate_screenshot')
async def donate_screenshot(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        "📸 <b>שלח צילום מסך של ההעברה</b>\n\n"
        "העלה תמונה (לא קובץ) של אישור ההעברה.\n"
        "אחרי התמונה תשלח את הסכום והסיבה."
    )
    await state.set_state(DonateForm.waiting_for_screenshot)
    await callback.answer()

@router.message(DonateForm.waiting_for_screenshot, F.photo)
async def receive_screenshot(msg: Message, state: FSMContext):
    file_id = msg.photo[-1].file_id
    await state.update_data(screenshot=file_id, user_id=msg.from_user.id)
    await msg.answer("💰 <b>איזה סכום תרמת?</b>\n\nכתוב מספר בלבד (למשל: 50)")
    await state.set_state(DonateForm.waiting_for_amount)

@router.message(DonateForm.waiting_for_amount)
async def receive_amount(msg: Message, state: FSMContext):
    try:
        amount = float(msg.text.strip())
    except:
        await msg.answer("⚠️ כתוב מספר בלבד (למשל: 50)")
        return
    await state.update_data(amount=amount)
    await msg.answer("💬 <b>מה גרם לך לתרום?</b>\n\nכתוב בקצרה:")
    await state.set_state(DonateForm.waiting_for_reason)

@router.message(DonateForm.waiting_for_reason)
async def receive_reason(msg: Message, state: FSMContext, bot):
    reason = msg.text
    data = await state.get_data()
    await state.clear()
    
    caption = (
        f"💖 <b>תרומה חדשה!</b>\n\n"
        f"👤 משתמש: {msg.from_user.mention_html(msg.from_user.first_name)}\n"
        f"💰 סכום: {data['amount']} \n"
        f"💬 סיבה: {reason}\n\n"
        f"<i>אדמין, אשר/י או דחה/י:</i>"
    )
    
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='✅ אשר', callback_data=f"approve_{msg.from_user.id}_{data['amount']}"),
         InlineKeyboardButton(text='❌ דחה', callback_data=f"reject_{msg.from_user.id}")]
    ])
    
    await bot.send_photo(ADMIN_GROUP, data['screenshot'], caption=caption, reply_markup=kb)
    await msg.answer(
        "✅ <b>תודה רבה!</b>\n\n"
        "צילום המסך נשלח לאימות.\n"
        "כשהאדמין יאשר, תקבל נקודות!"
    )

@router.callback_query(F.data.startswith('approve_'))
async def approve_donation(callback: CallbackQuery):
    parts = callback.data.split('_')
    user_id = int(parts[1])
    amount = float(parts[2])
    
    from sqlalchemy import text as sa_text
    from bot.database.session import engine
    async with engine.begin() as conn:
        await conn.run_sync(lambda c: c.execute(sa_text("INSERT INTO donations (user_id, amount) VALUES (:uid, :amt)"), {"uid": user_id, "amt": amount}))
        await conn.run_sync(lambda c: c.execute(sa_text("UPDATE users SET points = COALESCE(points, 0) + :pts WHERE telegram_id = :uid"), {"pts": amount, "uid": user_id}))
    
    await callback.bot.send_message(user_id, f"🎉 <b>תרומתך אושרה!</b>\n\n💰 {amount} \n⭐️ קיבלת {amount} נקודות!")
    await callback.message.edit_caption(f"{callback.message.caption}\n\n✅ <b>אושר!</b>")
    await callback.answer("✅ אושר")

@router.callback_query(F.data.startswith('reject_'))
async def reject_donation(callback: CallbackQuery):
    user_id = int(callback.data.split('_')[1])
    await callback.bot.send_message(user_id, "❌ <b>תרומתך לא אושרה.</b>\n\nאם יש בעיה, צור קשר עם האדמין.")
    await callback.message.edit_caption(f"{callback.message.caption}\n\n❌ <b>נדחה</b>")
    await callback.answer("❌ נדחה")