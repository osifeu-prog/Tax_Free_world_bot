from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
router = Router()


@router.callback_query(F.data.startswith('menu_'))
async def menu_handler(callback: CallbackQuery):
    action = callback.data[5:]  # budget, pension, academy, city, ref, donate
    commands = {
        'budget': '/budget',
        'pension': '/pension',
        'academy': '/academy',
        'city': '/city',
        'ref': '/ref',
        'donate': '/donate'
    }
    cmd = commands.get(action, '/start')
    await callback.message.answer(f'{cmd}')
    await callback.answer()

@router.callback_query(F.data == 'open_miniapp')
async def miniapp_handler(callback: CallbackQuery):
    await callback.message.answer('/miniapp')
    await callback.answer()

@router.callback_query(F.data == 'cmd_help')
async def help_handler(callback: CallbackQuery):
    await callback.message.answer('/help')
    await callback.answer()

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
