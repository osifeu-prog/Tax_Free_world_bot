from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
router = Router()

@router.message(Command('menu'))
async def cmd_menu(msg: Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='💰 חיסכון', callback_data='go_budget'), InlineKeyboardButton(text='📊 פנסיה', callback_data='go_pension')],
        [InlineKeyboardButton(text='🎓 אקדמיה', callback_data='go_academy'), InlineKeyboardButton(text='🏙️ TON City', callback_data='go_city')],
        [InlineKeyboardButton(text='💖 תרומה', callback_data='go_donate'), InlineKeyboardButton(text='🔗 הפניה', callback_data='go_ref')],
        [InlineKeyboardButton(text='📱 מחשבון ויזואלי', callback_data='open_miniapp'), InlineKeyboardButton(text='❔ עזרה', callback_data='go_help')]
    ])
    await msg.answer('📋 <b>תפריט ראשי</b>', parse_mode='HTML', reply_markup=kb)

@router.callback_query(F.data.startswith('go_'))
async def menu_click(callback: CallbackQuery):
    cmd = callback.data[3:]
    await callback.message.answer(f'/{cmd}')
    await callback.answer()

@router.callback_query(F.data == 'open_miniapp')
async def miniapp_click(callback: CallbackQuery):
    await callback.message.answer('/miniapp')
    await callback.answer()
