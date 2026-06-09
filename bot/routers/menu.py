from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
router = Router()

@router.message(Command('menu'))
async def cmd_menu(msg: Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='💰 חיסכון', callback_data='menu_budget'),
         InlineKeyboardButton(text='📊 פנסיה', callback_data='menu_pension')],
        [InlineKeyboardButton(text='🎓 אקדמיה', callback_data='menu_academy'),
         InlineKeyboardButton(text='🏙️ TON City', callback_data='menu_city')],
        [InlineKeyboardButton(text='🔗 הפניה', callback_data='menu_ref'),
         InlineKeyboardButton(text='💖 תרומה', callback_data='menu_donate')],
        [InlineKeyboardButton(text='📱 מחשבון ויזואלי', callback_data='open_miniapp'),
         InlineKeyboardButton(text='❔ עזרה', callback_data='cmd_help')]
    ])
    await msg.answer('📋 <b>תפריט ראשי TON Israel</b>', parse_mode='HTML', reply_markup=kb)
