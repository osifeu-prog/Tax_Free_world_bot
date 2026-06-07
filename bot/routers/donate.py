# -*- coding: utf-8 -*-
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from bot.keyboards.inline import back_to_main

router = Router()

WALLET_ADDRESS = "UQCd7XHWGj06cBLlWW_DZUN3TWMGr_oWoVy0G0LkC14gQklj"
GROUP_LINK = "https://t.me/+HIzvM8sEgh1kNWY0"
ADMIN_CHAT_ID = 224223270  # מזהה שלך לקבלת התראות

class DonateWizard(StatesGroup):
    waiting_for_proof = State()

@router.message(Command("donate"))
async def cmd_donate(msg: Message, state: FSMContext):
    # הודעה 1: הסבר
    await msg.answer(
        "❤️ <b>תמכו בפרויקט  הורדת יוקר המחיה בישראל</b>\n\n"
        "הבוט הזה חינמי לחלוטין, ואנו שואפים להרחיב את השירות לכל אזרח.\n"
        "תרומתכם תסייע לנו לפתח כלים נוספים, להפיץ את הבשורה, ולהוזיל עלויות למשפחות.",
        parse_mode="HTML"
    )
    # הודעה 2: כתובת הארנק (מופרדת להעתקה קלה)
    await msg.answer(
        f"📤 <b>שלחו TON לכתובת:</b>\n\n"
        f"<code>{WALLET_ADDRESS}</code>\n\n"
        f"לחצו על הכתובת כדי להעתיק.",
        parse_mode="HTML"
    )
    # הודעה 3: כפתור "שלחתי תרומה"
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ שלחתי תרומה! הצטרף לקבוצה", callback_data="sent_donation")],
        [InlineKeyboardButton(text="🔙 חזרה", callback_data="start")],
    ])
    await msg.answer(
        "🔐 <b>לאחר שליחת התרומה:</b>\n"
        "לחצו על הכפתור למטה, העלו צילום מסך/קבלה, ונאשר את הצטרפותכם לקבוצת התורמים.",
        parse_mode="HTML",
        reply_markup=kb
    )

@router.callback_query(F.data == "sent_donation")
async def ask_for_proof(call: CallbackQuery, state: FSMContext):
    await state.set_state(DonateWizard.waiting_for_proof)
    await call.message.answer(
        "📎 <b>העלו צילום מסך/קבלה של ההעברה:</b>\n\n"
        "שלחו תמונה או קובץ, ונבדוק אותו.\n"
        "(ההוכחה נשלחת לאדמין לאימות.)",
        parse_mode="HTML"
    )
    await call.answer()

@router.message(DonateWizard.waiting_for_proof, F.photo | F.document)
async def receive_proof(msg: Message, state: FSMContext):
    # שליחת ההוכחה לאדמין
    await msg.bot.send_message(
        ADMIN_CHAT_ID,
        f"📥 <b>הוכחת תרומה התקבלה!</b>\n"
        f"מאת: {msg.from_user.first_name} (ID: {msg.from_user.id})\n"
        f"בדוק את הקובץ ואשר.",
        parse_mode="HTML"
    )
    if msg.photo:
        await msg.bot.send_photo(ADMIN_CHAT_ID, msg.photo[-1].file_id)
    elif msg.document:
        await msg.bot.send_document(ADMIN_CHAT_ID, msg.document.file_id)
    await msg.answer(
        "✅ <b>ההוכחה נשלחה לאימות!</b>\n\n"
        "לאחר האימות, תקבלו קישור לקבוצת התורמים.\n"
        "בינתיים, אתם מוזמנים להמשיך להשתמש בבוט.",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔙 חזרה לתפריט", callback_data="start")]
        ])
    )
    await state.clear()

