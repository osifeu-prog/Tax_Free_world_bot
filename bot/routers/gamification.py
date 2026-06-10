from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from bot.database.session import async_session
from bot.database.models import User
from sqlalchemy import select
import datetime, random

router = Router()

DAILY_BONUS = 10
REF_BONUS = 50

async def get_user(uid):
    async with async_session() as s:
        u = (await s.execute(select(User).where(User.telegram_id == uid))).scalar_one_or_none()
        if not u:
            u = User(telegram_id=uid, points=0)
            s.add(u)
            await s.commit()
        return u

@router.message(Command('daily'))
async def daily_bonus(msg: Message):
    u = await get_user(msg.from_user.id)
    if u.last_gift_date and u.last_gift_date.date() == datetime.date.today():
        await msg.answer('⏳ כבר קיבלת בונוס היום. תחזור מחר!')
        return
    u.points = (u.points or 0) + DAILY_BONUS
    u.last_gift_date = datetime.datetime.utcnow()
    async with async_session() as s:
        await s.merge(u)
        await s.commit()
    await msg.answer(f'🎁 קיבלת {DAILY_BONUS} נקודות! סה"כ: {u.points} נקודות.')

@router.message(Command('points'))
async def show_points(msg: Message):
    u = await get_user(msg.from_user.id)
    await msg.answer(f'💰 יש לך {u.points or 0} נקודות.')

@router.message(Command('ref'))
async def referral(msg: Message):
    u = await get_user(msg.from_user.id)
    ref_link = f"https://t.me/Tax_Free_world_bot?start=ref{msg.from_user.id}"
    await msg.answer(
        f'🔗 <b>קוד הפניה</b>\n\nשתף את הקישור:\n{ref_link}\n\n'
        f'כשחבר מצטרף, תקבל {REF_BONUS} נקודות.\n'
        f'יש לך {u.points or 0} נקודות.',
        parse_mode='HTML',
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='🔗 שתף', switch_inline_query=f'הצטרף ל-TON Israel! {ref_link}')]
        ])
    )

# לוח מובילים
@router.message(Command('top'))
async def leaderboard(msg: Message):
    async with async_session() as s:
        top = (await s.execute(
            select(User).order_by(User.points.desc()).limit(10)
        )).scalars().all()
    if not top:
        await msg.answer('🏆 אין עדיין מובילים. היה הראשון!')
        return
    board = '\n'.join([f'{i+1}. {u.telegram_id}  {u.points or 0} נקודות' for i, u in enumerate(top)])
    await msg.answer(f'<b>🏆 לוח מובילים</b>\n\n{board}', parse_mode='HTML')