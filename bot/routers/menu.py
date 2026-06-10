from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from bot.routers.dashboard_simple import home

router = Router()

@router.message(Command("menu"))
async def cmd_menu(msg: Message):
    await home(msg)
