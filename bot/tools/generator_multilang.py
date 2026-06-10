import os, json
from pathlib import Path

SUPPORTED_LANGS = ["he", "en", "yi", "es", "fr"]

BASE_TEXTS = {
    "title": {"he": "פקודה חדשה", "en": "New Command", "yi": "נע באפעל", "es": "Nuevo comando", "fr": "Nouvelle commande"},
    "description": {"he": "פקודה חדשה נוצרה אוטומטית.", "en": "A new command was generated automatically.", "yi": "א נע באפעל איז אויטאמאטיש געשאפן געווארן.", "es": "Un nuevo comando fue generado automáticamente.", "fr": "Une nouvelle commande a été générée automatiquement."},
    "button_ok": {"he": "אישור", "en": "OK", "yi": "יא", "es": "Aceptar", "fr": "OK"},
    "button_cancel": {"he": "ביטול", "en": "Cancel", "yi": "ניין", "es": "Cancelar", "fr": "Annuler"}
}

def generate_command(name: str, include_fsm: bool = False, include_api: bool = False):
    base = Path(f"bot/routers/{name}")
    base.mkdir(parents=True, exist_ok=True)
    texts = {lang: {k: BASE_TEXTS[k][lang] for k in BASE_TEXTS} for lang in SUPPORTED_LANGS}
    (base / "texts.json").write_text(json.dumps(texts, indent=2, ensure_ascii=False), encoding="utf-8")
    (base / "keyboard.py").write_text(f'''from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import json
from pathlib import Path
TEXTS = json.loads(Path(__file__).with_name("texts.json").read_text(encoding="utf-8"))
def get_keyboard(lang: str):
    t = TEXTS.get(lang, TEXTS["he"])
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t["button_ok"], callback_data="{name}_ok")],
        [InlineKeyboardButton(text=t["button_cancel"], callback_data="{name}_cancel")]
    ])''', encoding="utf-8")
    (base / "logic.py").write_text(f'''async def process_ok(user_id: int):
    return f"User {{user_id}} pressed OK in {name}"
async def process_cancel(user_id: int):
    return f"User {{user_id}} canceled {name}"''', encoding="utf-8")
    handler_extra = ""
    if include_fsm:
        handler_extra = '''
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

class {name}States(StatesGroup):
    step1 = State()
    step2 = State()
    confirm = State()
'''
    handler_code = f'''from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from .keyboard import get_keyboard, TEXTS
from .logic import process_ok, process_cancel
from bot.database.session import async_session
from bot.database.models import User
from sqlalchemy import select
{handler_extra}
router = Router()
async def get_lang(uid):
    async with async_session() as s:
        u = (await s.execute(select(User).where(User.telegram_id == uid))).scalar_one_or_none()
        return u.language if u else "he"
@router.message(Command("{name}"))
async def cmd_{name}(msg: Message):
    lang = await get_lang(msg.from_user.id)
    t = TEXTS.get(lang, TEXTS["he"])
    await msg.answer(f"<b>{{t['title']}}</b>\\n\\n{{t['description']}}", parse_mode="HTML", reply_markup=get_keyboard(lang))
@router.callback_query(F.data.startswith("{name}_"))
async def callback_{name}(cb: CallbackQuery):
    action = cb.data.split("_")[1]
    uid = cb.from_user.id
    if action == "ok":
        result = await process_ok(uid)
    else:
        result = await process_cancel(uid)
    await cb.answer(result, show_alert=True)'''
    (base / "handler.py").write_text(handler_code, encoding="utf-8")
    return f"Command '{name}' generated"