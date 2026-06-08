from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from bot.services.translation_service import translator
from bot.database.session import async_session
from bot.database.models import User
from sqlalchemy import select

router = Router()

async def get_user_lang(telegram_id: int) -> str:
    async with async_session() as session:
        stmt = select(User).where(User.telegram_id == telegram_id)
        user = (await session.execute(stmt)).scalar_one_or_none()
        return user.language if user and user.language else "he"

@router.message(Command("menu"))
async def cmd_menu(msg: Message):
    lang = await get_user_lang(msg.from_user.id)
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=translator.t(lang, "savings"), callback_data="menu_savings")],
        [InlineKeyboardButton(text=translator.t(lang, "household"), callback_data="menu_household")],
        [InlineKeyboardButton(text=translator.t(lang, "academy"), callback_data="menu_academy")],
        [InlineKeyboardButton(text=translator.t(lang, "community"), callback_data="menu_community")],
        [InlineKeyboardButton(text=translator.t(lang, "tools"), callback_data="menu_tools")],
        [InlineKeyboardButton(text=translator.t(lang, "permissions"), callback_data="menu_permissions")],
        [InlineKeyboardButton(text=translator.t(lang, "admin"), callback_data="menu_admin")],
        [InlineKeyboardButton(text=translator.t(lang, "profile"), callback_data="menu_profile")],
    ])
    await msg.answer(translator.t(lang, "menu_title"), reply_markup=kb, parse_mode="HTML")

# Callbacks for each category  send list of commands
@router.callback_query(lambda c: c.data == "menu_savings")
async def menu_savings(callback: CallbackQuery):
    lang = await get_user_lang(callback.from_user.id)
    await callback.message.answer("/start /compare /wallet /why /business /budget /profile /expenses /addexpense /setincome /delexpense")
    await callback.answer()

@router.callback_query(lambda c: c.data == "menu_household")
async def menu_household(callback: CallbackQuery):
    await callback.message.answer("/household /shopping /chore")
    await callback.answer()

@router.callback_query(lambda c: c.data == "menu_academy")
async def menu_academy(callback: CallbackQuery):
    await callback.message.answer("/academy /crypto /cbdc /decentral /socio /anti /edu /academy_extended /academy_nft /academy_dao /vision /spark")
    await callback.answer()

@router.callback_query(lambda c: c.data == "menu_community")
async def menu_community(callback: CallbackQuery):
    await callback.message.answer("/ref /qr /stats /top /tip /contact /faq /daily /mydata /gift")
    await callback.answer()

@router.callback_query(lambda c: c.data == "menu_tools")
async def menu_tools(callback: CallbackQuery):
    await callback.message.answer("/miniapp /keyboard /hide /ask /feedback /help /quiz /menu")
    await callback.answer()

@router.callback_query(lambda c: c.data == "menu_permissions")
async def menu_permissions(callback: CallbackQuery):
    await callback.message.answer("/requestadmin /addadmin /login /setpassword /removeadmin")
    await callback.answer()

@router.callback_query(lambda c: c.data == "menu_admin")
async def menu_admin(callback: CallbackQuery):
    await callback.message.answer("/admin /export /debug /addgroup /groups /report /setrole /seed_courses /seed_kg")
    await callback.answer()

@router.callback_query(lambda c: c.data == "menu_profile")
async def menu_profile(callback: CallbackQuery):
    await callback.message.answer("/myrole /mydata")
    await callback.answer()
