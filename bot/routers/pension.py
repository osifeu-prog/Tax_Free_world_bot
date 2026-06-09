from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from bot.services.pension_calc import calc_budgetary, calc_accumulating, estimate_tax

router = Router()
user_data = {}

@router.message(Command('pension'))
async def cmd_pension(msg: Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='🏢 שכיר (ציבורי)', callback_data='pension_public')],
        [InlineKeyboardButton(text='🏭 שכיר (פרטי)', callback_data='pension_private')],
        [InlineKeyboardButton(text='🤷 לא יודע', callback_data='pension_unknown')]
    ])
    await msg.answer('<b>📊 מחשבון פנסיה</b>\n\nאיפה אתה עובד?', parse_mode='HTML', reply_markup=kb)

@router.callback_query(F.data.startswith('pension_'))
async def pension_start(callback: CallbackQuery):
    emp = callback.data.split('_')[1]
    uid = callback.from_user.id
    user_data[uid] = {'emp': emp, 'step': 'age'}
    await callback.message.answer('מה גילך? (הכנס מספר)')
    await callback.answer()

@router.message(lambda msg: msg.text and msg.text.isdigit())
async def pension_steps(msg: Message):
    uid = msg.from_user.id
    if uid not in user_data: return
    step = user_data[uid]['step']
    val = int(msg.text)
    if step == 'age':
        user_data[uid]['age'] = val
        user_data[uid]['step'] = 'salary'
        await msg.answer('מה השכר החודשי שלך?')
    elif step == 'salary':
        user_data[uid]['salary'] = val
        user_data[uid]['step'] = 'retire'
        await msg.answer('באיזה גיל תפרוש?')
    elif step == 'retire':
        user_data[uid]['retire'] = val
        d = user_data.pop(uid)
        result = calc_budgetary(d) if d['emp'] == 'public' else calc_accumulating(d)
        tax = estimate_tax(result['monthly_pension'])
        await msg.answer(
            f'<b>📊 תוצאת פנסיה</b>\n━━━━━━━━━━\n💰 קצבה חודשית: {result["monthly_pension"]:,.0f} \n🧾 מס: {tax:,.0f} \n💵 נטו: {result["monthly_pension"]-tax:,.0f} ',
            parse_mode='HTML'
        )