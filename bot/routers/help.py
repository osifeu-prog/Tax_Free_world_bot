from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup
from aiogram.filters import Command
from bot.keyboards.inline import back_to_main

router = Router()

HELP_TEXT = '''
📖 <b>פקודות הבוט  TON Israel</b>

💰 <b>חיסכון:</b>
/start, /compare, /wallet, /why, /business

🏠 <b>ניהול כלכלת הבית:</b>
/budget, /profile, /addexpense, /expenses, /setincome, /delexpense

📚 <b>אקדמיה:</b>
/crypto, /cbdc, /decentral, /socio, /anti, /edu, /faq

👥 <b>קהילה:</b>
/ref, /stats, /top, /tip, /contact, /id, /daily, /mydata

🛠️ <b>ניהול:</b>
/admin, /debug, /miniapp, /keyboard, /hide, /export
'''

@router.message(Command("help"))
async def cmd_help(msg: Message):
    await msg.answer(HELP_TEXT, parse_mode="HTML")

@router.callback_query(F.data == "help")
async def help_cb(call: CallbackQuery):
    await call.message.edit_text(HELP_TEXT, parse_mode="HTML", reply_markup=back_to_main())
    await call.answer()
