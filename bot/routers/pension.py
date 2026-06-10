from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from bot.services.pension_calc import calc_budgetary, calc_accumulating, estimate_tax

router = Router()
user_data = {}

@router.message(Command('pension'))
async def cmd_pension(msg: Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='🏢 ציבורי', callback_data='emp_public')],
        [InlineKeyboardButton(text='🏭 פרטי', callback_data='emp_private')],
        [InlineKeyboardButton(text='🤷 לא יודע', callback_data='emp_unknown')]
    ])
    await msg.answer('<b>📊 מחשבון פנסיה</b>\n\nאיפה אתה עובד?', parse_mode='HTML', reply_markup=kb)

@router.callback_query(F.data.startswith('emp_'))
async def emp_chosen(callback: CallbackQuery):
    emp = callback.data.split('_')[1]
    uid = callback.from_user.id
    user_data[uid] = {'emp': emp, 'step': 'age'}
    await callback.message.answer('🎂 מה גילך?')
    await callback.answer()

@router.message(lambda msg: msg.text and msg.text.isdigit())
async def steps(msg: Message):
    uid = msg.from_user.id
    if uid not in user_data: return
    d = user_data[uid]
    step = d['step']
    val = int(msg.text)
    if step == 'age':
        d['age_now'] = val
        d['step'] = 'salary'
        await msg.answer('💰 מה השכר שלך?')
    elif step == 'salary':
        d['salary_bruto'] = val
        d['step'] = 'retire'
        await msg.answer('👴 באיזה גיל תפרוש?')
    elif step == 'retire':
        d['retirement_age'] = val
        profile = user_data.pop(uid)
        result = calc_budgetary(profile) if profile['emp'] == 'public' else calc_accumulating(profile)
        tax = estimate_tax(result['monthly_pension'])
        await msg.answer(
            f'📊 <b>תוצאת פנסיה</b>\n━━━━━━━━━━\n'
            f'💰 קצבה: {result["monthly_pension"]:,.0f} \n'
            f'🧾 מס: {tax:,.0f} \n'
            f'💵 נטו: {result["monthly_pension"]-tax:,.0f} ',
            parse_mode='HTML'
        )