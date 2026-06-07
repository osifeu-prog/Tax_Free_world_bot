from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from bot.keyboards.inline import back_to_main

router = Router()

HELP_TEXT = '''
📖 <b>כל הפקודות  TON Israel</b>

💰 <b>חיסכון:</b>
/start, /compare, /wallet, /why, /business

🏠 <b>ניהול כלכלת הבית:</b>
/budget, /profile, /addexpense, /expenses, /setincome, /delexpense

📚 <b>אקדמיה:</b>
/crypto, /cbdc, /decentral, /socio, /anti, /edu, /faq, /academy_extended, /academy_nft, /academy_dao

👥 <b>קהילה:</b>
/ref, /stats, /top, /tip, /contact, /id, /daily, /mydata, /gift

🛠️ <b>כלים:</b>
/miniapp, /keyboard, /hide, /ask, /feedback, /help, /quiz

🔐 <b>ניהול הרשאות:</b>
/addadmin, /login, /setpassword, /removeadmin

🔒 <b>אדמין (רק למנהלים):</b>
/admin, /export, /debug
'''

@router.message(Command("help"))
async def cmd_help(msg: Message):
    await msg.answer(HELP_TEXT, parse_mode="HTML")

@router.callback_query(F.data == "help")
async def help_cb(call: CallbackQuery):
    await call.message.edit_text(HELP_TEXT, parse_mode="HTML", reply_markup=back_to_main())
    await call.answer()
