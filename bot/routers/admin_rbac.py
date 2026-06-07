from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from bot.config import settings
from bot.services.admin_service import add_admin, verify_password, set_password, remove_admin

router = Router()

SUPER_ADMINS = settings.admin_ids

@router.message(Command("addadmin"))
async def cmd_addadmin(msg: Message):
    if msg.from_user.id not in SUPER_ADMINS:
        await msg.answer("⛔ רק מנהל-על יכול להוסיף מנהלים.")
        return
    parts = msg.text.split(maxsplit=3)
    if len(parts) < 4:
        await msg.answer("שימוש: <code>/addadmin user_id role password</code>")
        return
    user_id = int(parts[1])
    role = parts[2]
    password = parts[3]
    await add_admin(user_id, role, password)
    await msg.answer(f"✅ המנהל {user_id} נוסף בהצלחה.")

@router.message(Command("login"))
async def cmd_login(msg: Message):
    password = msg.text.split(maxsplit=1)[1] if len(msg.text.split()) > 1 else ""
    if not password:
        await msg.answer("שימוש: <code>/login password</code>")
        return
    if await verify_password(msg.from_user.id, password):
        await msg.answer("✅ התחברת בהצלחה לאזור האדמין.")
    else:
        await msg.answer("⛔ סיסמה שגויה.")

@router.message(Command("setpassword"))
async def cmd_setpassword(msg: Message):
    parts = msg.text.split(maxsplit=2)
    if len(parts) < 3:
        await msg.answer("שימוש: <code>/setpassword old new</code>")
        return
    old = parts[1]
    new = parts[2]
    if await set_password(msg.from_user.id, old, new):
        await msg.answer("✅ הסיסמה שונתה.")
    else:
        await msg.answer("⛔ סיסמה ישנה שגויה.")

@router.message(Command("removeadmin"))
async def cmd_removeadmin(msg: Message):
    if msg.from_user.id not in SUPER_ADMINS:
        await msg.answer("⛔ רק מנהל-על יכול להסיר מנהלים.")
        return
    parts = msg.text.split()
    if len(parts) < 2:
        await msg.answer("שימוש: <code>/removeadmin user_id</code>")
        return
    user_id = int(parts[1])
    await remove_admin(user_id)
    await msg.answer(f"✅ המנהל {user_id} הוסר.")
